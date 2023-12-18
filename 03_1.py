with open('03_input.txt') as f:
    schematic = f.read().split('\n')

pn_sum = 0
for row, line in enumerate(schematic):
    in_num = False
    num_start = None
    for col, c in enumerate(line):
        if in_num and (not c.isdigit() or col == len(line)-1):
            if c.isdigit() and col == len(line)-1:
                col += 1
            if (
                    not c.isdigit() and c != '.'
                    or row > 0 and any(not x.isdigit() and x != '.'
                                       for x in schematic[row-1][max(0, num_start-1):min(len(line), col+1)])
                    or num_start > 0 and line[num_start-1] != '.'
                    or row < len(schematic)-1 and any(
                        not x.isdigit() and x != '.'
                        for x in schematic[row+1][max(0, num_start-1):min(len(line), col+1)])
                    ):
                pn_sum += int(line[num_start:col])
            in_num = False
        elif not in_num and c.isdigit():
            num_start = col
            in_num = True
print(pn_sum)


