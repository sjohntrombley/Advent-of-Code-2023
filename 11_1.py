from itertools import combinations

with open('11_input.txt') as f:
    image = f.read().strip().split('\n')

empty = []
for i, row in enumerate(image):
    if all(c == '.' for c in row):
        empty.append(i)
for i in reversed(empty):
    image.insert(i, image[i])

empty = []
for j in range(len(image[0])):
    if all(image[i][j] == '.' for i in range(len(image))):
        empty.append(j)
for j in reversed(empty):
    image = [row[:j] + '.' + row[j:] for row in image]

galaxies = [(i, j) for i, row in enumerate(image) for j, c in enumerate(row) if c == '#']
print(sum(abs(i-k) + abs(j-l) for (i, j), (k, l) in combinations(galaxies, 2)))