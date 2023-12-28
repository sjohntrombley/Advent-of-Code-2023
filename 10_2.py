from collections import deque

with open('10_input.txt') as f:
    diagram = f.read().strip().split('\n')

for i, row in enumerate(diagram):
    j = row.find('S')
    if j != -1:
        break
si, sj = i, j
to_visit = deque()
loop = {(i, j)}
if i > 0 and diagram[i-1][j] in '7|F':
    to_visit.append((i-1, j))
if i < len(diagram)-1 and diagram[i+1][j] in 'J|L':
    to_visit.append((i+1, j))
if j > 0 and diagram[i][j-1] in 'L-F':
    to_visit.append((i, j-1))
if j < len(diagram[i])-1 and diagram[i][j+1] in 'J-7':
    to_visit.append((i, j+1))
while to_visit:
    i, j = to_visit.popleft()
    loop.add((i, j))
    pipe = diagram[i][j]
    if pipe in 'J|L' and (i-1, j) not in loop:
        to_visit.append((i-1, j))
    if pipe in '7|F' and (i+1, j) not in loop:
        to_visit.append((i+1, j))
    if pipe in 'J-7' and (i, j-1) not in loop:
        to_visit.append((i, j-1))
    if pipe in 'L-F' and (i, j+1) not in loop:
        to_visit.append((i, j+1))

if si > 0 and diagram[si-1][sj] in '7|F':
    if sj > 0 and diagram[si][sj-1] in 'L-F':
        diagram[si] = diagram[si].replace('S', 'J')
    elif sj < len(diagram[si])-1 and diagram[si][sj+1] in 'J-7':
        diagram[si] = diagram[si].replace('S', 'L')
    else:
        diagram[si] = diagram[si].replace('S', '|')
elif sj > 0 and diagram[si][sj-1] in 'L-F':
    if sj < len(diagram[si])-1 and diagram[si][sj+1] in 'J-7':
        diagram[si] = diagram[si].replace('S', '-')
    else:
        diagram[si] = diagram[si].replace('S', '7')
else:
    diagram[si] = diagram[si].replace('S', 'F')
inside_count = 0
for i, row in enumerate(diagram):
    inside = False
    pipe_end = None
    for j, c in enumerate(row):
        if (i, j) in loop:
            if c == 'F':
                pipe_end = 'J'
            elif c == 'L':
                pipe_end = '7'
            elif c == pipe_end or c == '|':
                inside = not inside
        elif inside:
            inside_count += 1
print(inside_count)
