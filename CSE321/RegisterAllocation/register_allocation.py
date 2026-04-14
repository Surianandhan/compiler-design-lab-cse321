import re
from collections import defaultdict

var_pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')

def parse_instruction(line):
    line = line.strip()
    defs = set()
    uses = set()
    
    if not line:
        return {'text': line, 'defs': defs, 'uses': uses}
    if line.endswith(':'):
        return {'text': line, 'defs': defs, 'uses': uses}
    
    if '=' in line:
        lhs, rhs = line.split('=', 1)
        lhs = lhs.strip()
        if var_pattern.match(lhs):
            defs.add(lhs)
        for tok in var_pattern.findall(rhs):
            if not tok.isdigit():
                if tok != lhs:
                    uses.add(tok)
    else:
        for tok in var_pattern.findall(line):
            if not tok.isdigit():
                uses.add(tok)
    
    return {'text': line, 'defs': defs, 'uses': uses}

def liveness_analysis(tac_lines):
    instrs = [parse_instruction(l) for l in tac_lines]
    n = len(instrs)
    IN = [set() for _ in range(n)]
    OUT = [set() for _ in range(n)]
    
    changed = True
    while changed:
        changed = False
        for i in range(n-1, -1, -1):
            old_in = IN[i].copy()
            old_out = OUT[i].copy()
            
            succs = []
            line = instrs[i]['text']
            if line.startswith('goto '):
                label = line.split('goto', 1)[1].strip()
                target = None
                for j, l in enumerate(tac_lines):
                    if l.strip() == label + ':':
                        target = j
                        break
                if target is not None:
                    succs.append(target)
            elif line.startswith('return'):
                succs = []
            else:
                if i+1 < n:
                    succs.append(i+1)
            
            new_out = set()
            for s in succs:
                new_out |= IN[s]
            OUT[i] = new_out
            IN[i] = instrs[i]['uses'] | (OUT[i] - instrs[i]['defs'])
            
            if old_in != IN[i] or old_out != OUT[i]:
                changed = True
    
    return instrs, IN, OUT

def build_interference_graph(instrs, IN, OUT):
    nodes = set()
    for ins in instrs:
        nodes |= ins['defs'] | ins['uses']
    nodes = {v for v in nodes if v}
    
    adj = {v: set() for v in nodes}
    n = len(instrs)
    
    for i in range(n):
        defs = instrs[i]['defs']
        live_out = OUT[i]
        for d in defs:
            for v in live_out:
                if v != d:
                    adj[d].add(v)
                    adj[v].add(d)
    
    return adj

def color_graph(adj, K):
    adj_copy = {v: set(neis) for v, neis in adj.items()}
    stack = []
    potential_spills = set()
    
    while adj_copy:
        low_deg_nodes = [v for v, neis in adj_copy.items() if len(neis) < K]
        if low_deg_nodes:
            node = low_deg_nodes[0]
            stack.append((node, adj_copy[node].copy()))
            for nb in adj_copy[node]:
                adj_copy[nb].remove(node)
            del adj_copy[node]
        else:
            node = max(adj_copy.keys(), key=lambda x: len(adj_copy[x]))
            potential_spills.add(node)
            stack.append((node, adj_copy[node].copy()))
            for nb in adj_copy[node]:
                adj_copy[nb].remove(node)
            del adj_copy[node]
    
    colors = {}
    spills = set()
    
    while stack:
        node, neighbors_at_removal = stack.pop()
        used_colors = set(colors.get(nb) for nb in neighbors_at_removal if nb in colors)
        assigned = None
        for c in range(K):
            if c not in used_colors:
                assigned = c
                break
        if assigned is None:
            spills.add(node)
        else:
            colors[node] = assigned
    
    return colors, spills, potential_spills

def show_results(tac_lines, instrs, IN, OUT, adj, colors, spills, potential_spills):
    print("\nProgram (TAC):")
    for i, l in enumerate(tac_lines):
        print(f"{i:2d}: {l}")
    
    print("\nLiveness (IN / OUT):")
    for i in range(len(instrs)):
        print(f"{i:2d}: IN={sorted(IN[i])}, OUT={sorted(OUT[i])}")
    
    print("\nInterference Graph (adjacency lists):")
    for v in sorted(adj.keys()):
        print(f"{v}: {sorted(adj[v])}")
    
    n_val = max(colors.values()) if colors else 0
    print(f"\nRegister assignment (colors -> r0..r{n_val}):")
    if colors:
        for v in sorted(adj.keys()):
            if v in colors:
                print(f"{v}: r{colors[v]}")
            else:
                print(f"{v}: spilled")
    else:
        print(" (no variables)")
    
    if spills:
        print("\nSpills suggested:", sorted(spills))
    else:
        print("\nNo spills required under chosen register count.")
    
    print("\nPotential spill candidates (heuristic):", sorted(potential_spills))

if __name__ == "__main__":
    tac_program = [
        "a = b + c",
        "d = a + e",
        "b = d + f",
        "g = a + b",
        "h = g + i",
        "return h"
    ]
    K = 3
    
    instrs, IN, OUT = liveness_analysis(tac_program)
    adj = build_interference_graph(instrs, IN, OUT)
    colors, spills, potential_spills = color_graph(adj, K)
    show_results(tac_program, instrs, IN, OUT, adj, colors, spills, potential_spills)