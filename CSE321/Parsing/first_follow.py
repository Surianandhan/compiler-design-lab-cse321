non_terms = ['E', 'I', 'A', 'T', 'O', 'M', 'F']
terms = ['+', '-', '*', '(', ')', 'n']
eps = 'e'
start = 'E'

prods = {
    'E': [['T', 'I'], [eps]],
    'I': [['A', 'T', 'I'], [eps]],
    'A': [['+'], ['-']],
    'T': [['F', 'O']],
    'O': [['M', 'F', 'O'], [eps]],
    'M': [['*']],
    'F': [['(', 'E', ')'], [eps]]
}

# Initialize FIRST sets
first = {t: {t} for t in terms}
first[eps] = {eps}
for nt in non_terms:
    first[nt] = set()

# Compute FIRST sets
changed = True
while changed:
    changed = False
    for nt in non_terms:
        for p in prods[nt]:
            curr = set()
            all_eps = True
            for s in p:
                if s in terms or s == eps:
                    curr.add(s)
                    all_eps = all_eps and (s == eps)
                    break
                else:
                    curr.update(first[s] - {eps})
                    if eps not in first[s]:
                        all_eps = False
                        break
            if all_eps:
                curr.add(eps)
            old = len(first[nt])
            first[nt].update(curr)
            if len(first[nt]) > old:
                changed = True

# Initialize FOLLOW sets
follow = {nt: set() for nt in non_terms}
follow[start].add('$')

# Compute FOLLOW sets
changed = True
while changed:
    changed = False
    for nt in non_terms:
        for p in prods[nt]:
            for i, s in enumerate(p):
                if s not in non_terms:
                    continue
                if i + 1 < len(p):
                    beta = p[i+1:]
                    first_beta = set()
                    beta_eps = True
                    for b in beta:
                        if b in terms:
                            first_beta.add(b)
                            beta_eps = False
                            break
                        else:
                            first_beta.update(first[b] - {eps})
                            if eps not in first[b]:
                                beta_eps = False
                                break
                    old = len(follow[s])
                    follow[s].update(first_beta)
                    if beta_eps:
                        follow[s].update(follow[nt])
                    if len(follow[s]) > old:
                        changed = True
                else:
                    old = len(follow[s])
                    follow[s].update(follow[nt])
                    if len(follow[s]) > old:
                        changed = True

print("FIRST:")
for nt in non_terms:
    print(f"{nt}: {first[nt]}")
print("\nFOLLOW:")
for nt in non_terms:
    print(f"{nt}: {follow[nt]}")