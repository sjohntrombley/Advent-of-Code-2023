with open('03_input.txt') as f:
    schematic = f.read().strip().split('\n')

potential_gears = {}
for row, line in enumerate(schematic):
    in_num = False
    num_start = None
    for col, c in enumerate(line):
        if in_num and (not c.isdigit() or col == len(line)-1):
            if c.isdigit():
                col += 1
            num = int(line[num_start:col])
            if row > 0:
                for col1 in range(max(0, num_start-1), min(col+1, len(line))):
                    if schematic[row-1][col1] == '*':
                        if (row-1, col1) in potential_gears:
                            potential_gears[(row-1, col1)].append(num)
                        else:
                            potential_gears[(row-1, col1)] = [num]
            if num_start > 0 and line[num_start-1] == '*':
                if (row, num_start-1) in potential_gears:
                    potential_gears[(row, num_start-1)].append(num)
                else:
                    potential_gears[(row, num_start-1)] = [num]
            if c == '*':
                if (row, col) in potential_gears:
                    potential_gears[(row, col)].append(num)
                else:
                    potential_gears[(row, col)] = [num]
            if row < len(schematic)-1:
                for col1 in range(max(0, num_start-1), min(col+1, len(line))):
                    if schematic[row+1][col1] == '*':
                        if (row+1, col1) in potential_gears:
                            potential_gears[(row+1, col1)].append(num)
                        else:
                            potential_gears[(row+1, col1)] = [num]
            in_num = False
        elif not in_num and c.isdigit():
            num_start = col
            in_num = True
print(sum(pg[0]*pg[1] for pg in potential_gears.values() if len(pg) == 2))


