from collections import deque

with open('10_input.txt') as f:
    diagram = f.read().strip().split('\n')

for i, row in enumerate(diagram):
    j = row.find('S')
    if j != -1:
        break
to_visit = deque()
visited = {(i, j)}
if i > 0 and diagram[i-1][j] in '7|F':
    to_visit.append((i-1, j, 1))
if i < len(diagram)-1 and diagram[i+1][j] in 'J|L':
    to_visit.append((i+1, j, 1))
if j > 0 and diagram[i][j-1] in 'L-F':
    to_visit.append((i, j-1, 1))
if j < len(diagram[i])-1 and diagram[i][j+1] in 'J-7':
    to_visit.append((i, j+1, 1))
while to_visit:
    i, j, dist = to_visit.popleft()
    visited.add((i, j))
    pipe = diagram[i][j]
    if pipe in 'J|L' and (i-1, j) not in visited:
        to_visit.append((i-1, j, dist+1))
    if pipe in '7|F' and (i+1, j) not in visited:
        to_visit.append((i+1, j, dist+1))
    if pipe in 'J-7' and (i, j-1) not in visited:
        to_visit.append((i, j-1, dist+1))
    if pipe in 'L-F' and (i, j+1) not in visited:
        to_visit.append((i, j+1, dist+1))
print(dist)


