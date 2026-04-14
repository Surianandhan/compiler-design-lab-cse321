# Create input file
with open("input.txt", "w") as f:
    f.write("a=b+c\n")
    f.write("d=b+c\n")
    f.write("e=a+d\n")
    f.write("f=b+c+d\n")
    f.write("g=e+f\n")

print("input.txt file created successfully!")

input_file = open("input.txt", "r")
output_file = open("output.txt", "w")

expressions = []
index = 0

for line in input_file:
    line = line.strip()
    parts = line.split("=")
    left_side = parts[0]
    right_side = parts[1]
    
    found_match = False
    
    for i in range(index):
        stored_right_side = expressions[i][1]
        if right_side == stored_right_side:
            found_match = True
            break
        elif stored_right_side in right_side:
            line = line.replace(stored_right_side, expressions[i][0])
    
    if not found_match:
        expressions.append([left_side, right_side])
        index += 1
    
    output_file.write(line + "\n")

input_file.close()
output_file.close()

print("Optimization complete! Check output.txt")