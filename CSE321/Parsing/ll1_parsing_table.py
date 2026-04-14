non_terminals = ['E', "E'", 'T', "T'", 'F']
terminals = ['id', '+', '*', '(', ')', '$']

productions = {
    'E': [['T', "E'"]],
    "E'": [['+', 'T', "E'"], ['ε']],
    'T': [['F', "T'"]],
    "T'": [['*', 'F', "T'"], ['ε']],
    'F': [['(', 'E', ')'], ['id']]
}

first_sets = {
    'E': ['(', 'id'],
    "E'": ['+', 'ε'],
    'T': ['(', 'id'],
    "T'": ['*', 'ε'],
    'F': ['(', 'id']
}

follow_sets = {
    'E': [')', '$'],
    "E'": [')', '$'],
    'T': ['+', ')', '$'],
    "T'": ['+', ')', '$'],
    'F': ['*', '+', ')', '$']
}

# Initialize parsing table
table = {}
for nt in non_terminals:
    table[nt] = {}
    for t in terminals:
        table[nt][t] = ''

# Fill parsing table
for nt in productions:
    for prod in productions[nt]:
        if prod[0] != 'ε':
            first_symbol = prod[0]
            if first_symbol in first_sets:
                first_list = first_sets[first_symbol]
            else:
                first_list = [first_symbol]
            for t in first_list:
                if t != 'ε':
                    table[nt][t] = prod
        else:
            for t in follow_sets[nt]:
                table[nt][t] = prod

print("LL(1) Parsing Table:")
print("Non-Terminal", end="")
for t in terminals:
    print(f"\t{t}", end="")
print()
for nt in non_terminals:
    print(nt, end="")
    for t in terminals:
        val = ' '.join(table[nt][t]) if table[nt][t] else ''
        print(f"\t{val}", end="")
    print()