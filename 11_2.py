from bisect import bisect
from itertools import combinations

with open('11_input.txt') as f:
    image = f.read().strip().split('\n')

empty_rows = []
for i, row in enumerate(image):
    if all(c == '.' for c in row):
        empty_rows.append(i)

empty_cols = []
for j in range(len(image[0])):
    if all(image[i][j] == '.' for i in range(len(image))):
        empty_cols.append(j)

galaxies = [
    (999999*bisect(empty_rows, i) + i, 999999*bisect(empty_cols, j) + j)
    for i, row in enumerate(image) for j, c in enumerate(row) if c == '#']
print(sum(abs(i-k) + abs(j-l) for (i, j), (k, l) in combinations(galaxies, 2)))