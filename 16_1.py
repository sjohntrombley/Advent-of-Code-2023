from collections import deque

with open('16_input.txt') as f:
    contraption = f.read().strip().split('\n')

visited = [[set() for _ in row] for row in contraption]
to_visit = deque([(0, 0, 0, 1)])
while to_visit:
    r, c, rd, cd = to_visit.popleft()
    visited[r][c].add((rd, cd))
    type_ = contraption[r][c]
    if rd == 0 and type_ == '|':
        for rd in (-1, 1):
            nr = r + rd
            if 0 <= nr < len(contraption) and (rd, 0) not in visited[nr][c]:
                to_visit.append((nr, c, rd, 0))
    elif cd == 0 and type_ == '-':
        for cd in (-1, 1):
            nc = c + cd
            if 0 <= nc < len(contraption[r]) and (0, cd) not in visited[r][nc]:
                to_visit.append((r, nc, 0, cd))
    else:
        if type_ == '/':
            rd, cd = -cd, -rd
        elif type_ == '\\':
            rd, cd = cd, rd
        nr, nc = r+rd, c+cd
        if 0<=nr<len(contraption) and 0<=nc<len(contraption[nr]) and (rd, cd) not in visited[nr][nc]:
            to_visit.append((nr, nc, rd, cd))

print(sum(len(v)>0 for row in visited for v in row))