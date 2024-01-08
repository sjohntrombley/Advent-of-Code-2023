from collections import deque

with open('17_input.txt') as f:
    map_ = [list(map(int, line.strip())) for line in f]

# mins[r][c][0] is the minimum heat loss when the next move is horizontal and mins[r][c][1] is the minimum heat loss
# when the next move is vertical
mins = [[[None, None] for _ in row] for row in map_]
mins[0][0] = [0, 0]
to_visit = deque()
to_visit_set = set()
for c in range(1, 4):
    mins[0][c][1] = sum(map_[0][1:c+1])
    to_visit.append((0, c, 1))
    to_visit_set.add((0, c, 1))
for r in range(1, 4):
    mins[r][0][0] = sum(row[0] for row in map_[1:r+1])
    to_visit.append((r, 0, 0))
    to_visit_set.add((r, 0, 0))

while to_visit:
    r, c, d = to_visit.popleft()
    to_visit_set.remove((r, c, d))
    # next move is horizontal
    if d == 0:
        for o in range(1, 4):
            nc = c + o
            if nc < len(map_[r]):
                nv = mins[r][c][0] + sum(map_[r][c+1:nc+1])
                if mins[r][nc][1] is None or nv < mins[r][nc][1]:
                    mins[r][nc][1] = nv
                    if (r, nc, 1) not in to_visit_set:
                        to_visit.append((r, nc, 1))
                        to_visit_set.add((r, nc, 1))
            nc = c - o
            if nc >= 0:
                nv = mins[r][c][0] + sum(map_[r][nc:c])
                if mins[r][nc][1] is None or nv < mins[r][nc][1]:
                    mins[r][nc][1] = nv
                    if (r, nc, 1) not in to_visit_set:
                        to_visit.append((r, nc, 1))
                        to_visit_set.add((r, nc, 1))
    else:
        for o in range(1, 4):
            nr = r + o
            if nr < len(map_):
                nv = mins[r][c][1] + sum(row[c] for row in map_[r+1:nr+1])
                if mins[nr][c][0] is None or nv < mins[nr][c][0]:
                    mins[nr][c][0] = nv
                    if (nr, c, 0) not in to_visit_set:
                        to_visit.append((nr, c, 0))
                        to_visit_set.add((nr, c, 0))
            nr = r - o
            if nr >= 0:
                nv = mins[r][c][1] + sum(row[c] for row in map_[nr:r])
                if mins[nr][c][0] is None or nv < mins[nr][c][0]:
                    mins[nr][c][0] = nv
                    if (nr, c, 0) not in to_visit_set:
                        to_visit.append((nr, c, 0))
                        to_visit_set.add((nr, c, 0))

print(min(mins[-1][-1]))