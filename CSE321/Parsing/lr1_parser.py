class LR1Parser:
    def __init__(self, action_table, goto_table, productions, start_symbol):
        self.action_table = action_table
        self.goto_table = goto_table
        self.productions = productions
        self.start_symbol = start_symbol

    def parse(self, input_tokens):
        stack = [0]
        pointer = 0
        
        print("%-20s %-20s %s" % ('STACK', 'INPUT', 'ACTION'))
        
        while True:
            state = stack[-1]
            current_token = input_tokens[pointer]
            
            print("%-20s %-20s" % (' '.join(map(str, stack)), ' '.join(input_tokens[pointer:])), end=" ")
            
            if (state, current_token) not in self.action_table:
                print("Error: No action")
                return False
            
            action = self.action_table[(state, current_token)]
            
            if action[0] == "shift":
                next_state = action[1]
                stack.append(current_token)
                stack.append(next_state)
                pointer += 1
                print(f"SHIFT {next_state}")
                
            elif action[0] == "reduce":
                prod_no = action[1]
                lhs, rhs = self.productions[prod_no]
                if rhs != ['ε']:
                    for _ in range(len(rhs) * 2):
                        stack.pop()
                    top_state = stack[-1]
                    stack.append(lhs)
                    if (top_state, lhs) not in self.goto_table:
                        print("Error: No goto!")
                        return False
                    goto_state = self.goto_table[(top_state, lhs)]
                    stack.append(goto_state)
                    print(f"REDUCE {prod_no}: {lhs} -> {' '.join(rhs)}")
                    
            elif action[0] == "accept":
                print("ACCEPTED!")
                return True

# Productions
productions = {
    1: ("E", ["E", "+", "T"]),
    2: ("E", ["T"]),
    3: ("T", ["T", "*", "F"]),
    4: ("T", ["F"]),
    5: ("F", ["(", "E", ")"]),
    6: ("F", ["id"])
}

# Action Table
action_table = {
    (0, 'id'): ("shift", 5), (0, '('): ("shift", 4),
    (1, '+'): ("shift", 6), (1, '$'): ("accept",),
    (2, '+'): ("reduce", 2), (2, '*'): ("shift", 7), (2, ')'): ("reduce", 2), (2, '$'): ("reduce", 2),
    (3, '+'): ("reduce", 4), (3, '*'): ("reduce", 4), (3, ')'): ("reduce", 4), (3, '$'): ("reduce", 4),
    (5, '+'): ("reduce", 6), (5, '*'): ("reduce", 6), (5, ')'): ("reduce", 6), (5, '$'): ("reduce", 6),
}

# Goto Table
goto_table = {
    (0, 'E'): 1, (0, 'T'): 2, (0, 'F'): 3,
}

parser = LR1Parser(action_table, goto_table, productions, "E")
tokens = ["id", "+", "id", "$"]
result = parser.parse(tokens)
print("Result:", "Valid" if result else "Invalid")