from itertools import combinations, groupby

with open('12_input.txt') as f:
    rows = []
    for line in f:
        row, group_sizes = line.split(' ')
        rows.append((row, [int(s) for s in group_sizes.split(',')]))

possible_count = 0
for row, group_sizes in rows:
    unknown_count = row.count('?')
    unknown_damage_count = sum(group_sizes) - row.count('#')
    for possible_damaged in combinations(range(unknown_count), unknown_damage_count):
        possible_row = row
        i = 0
        for d in possible_damaged:
            possible_row = possible_row.replace('?', '.', d-i).replace('?', '#', 1)
            i = d + 1
        possible_row = possible_row.replace('?', '.')
        if [len(list(g)) for k, g in groupby(possible_row) if k == '#'] == group_sizes:
            possible_count += 1
print(possible_count)


