class PeepholeOptimizer:
    
    def optimize(self, code):
        new_code = []
        i = 0
        
        while i < len(code):
            line = code[i].strip()
            
            # Check for redundant assignments
            if i + 1 < len(code):
                next_line = code[i + 1].strip()
                if self.is_redundant_pair(line, next_line):
                    i += 2
                    continue
            
            # Skip dead code after unconditional jump
            if line.startswith("goto"):
                new_code.append(line)
                i += 1
                while i < len(code) and not code[i].strip().endswith(":"):
                    i += 1
                continue
            
            # Simplify conditional jumps
            if i + 1 < len(code):
                next_line = code[i + 1].strip()
                if line.startswith("if") and next_line.startswith("goto"):
                    if line.split()[1] == next_line.split()[1]:
                        new_code.append(line)
                        i += 2
                        continue
            
            # Algebraic simplification
            simplified = self.simplify_algebra(line)
            if simplified != line:
                new_code.append(simplified)
                i += 1
                continue
            
            new_code.append(line)
            i += 1
        
        return new_code
    
    def is_redundant_pair(self, line1, line2):
        parts1 = line1.split()
        parts2 = line2.split()
        if len(parts1) >= 3 and len(parts2) >= 3 and parts1[1] == "=" and parts2[1] == "=":
            if parts1[2] == parts2[0] and parts2[2] == parts1[0]:
                return True
        return False
    
    def simplify_algebra(self, line):
        if "+ 0" in line:
            return line.replace(" + 0", "")
        if "- 0" in line:
            return line.replace(" - 0", "")
        if "* 1" in line:
            return line.replace(" * 1", "")
        if "* 0" in line:
            parts = line.split()
            return f"{parts[0]} = 0"
        return line

code = [
    "t1 = t2",
    "t2 = t1",
    "x = y + 0",
    "a = b * 1",
    "c = d * 0",
    "e = 0",
    "f = g - 0",
    "goto SKIP",
    "dead1 = 10",
    "dead2 = 20",
    "SKIP:",
    "if x > 0 goto END",
    "goto END",
    "END:",
    "result = final + 0",
    "temp = something * 1"
]

print("Before:")
for line in code:
    print(line)

optimizer = PeepholeOptimizer()
result = optimizer.optimize(code)

print("\nAfter:")
for line in result:
    print(line)