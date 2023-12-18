from bisect import insort, bisect

with open('05_input.txt') as f:
    input_ = f.read().strip().split('\n\n')
seeds = [int(seed) for seed in input_[0].split()[1:]]
maps = {}
for map_ in input_[1:]:
    map_rows = map_.split('\n')
    source_name, _, dest_name = map_rows[0].split()[0].split('-')
    maps[source_name] = (dest_name, [], {})
    for row in map_rows[1:]:
        dest_range_start, source_range_start, range_length = [int(n) for n in row.split()]
        insort(maps[source_name][1], source_range_start)
        maps[source_name][2][source_range_start] = (source_range_start+range_length-1, dest_range_start-source_range_start)

min_location = None
for seed in seeds:
    num = seed
    src = 'seed'
    while src != 'location':
        dest, src_range_starts, range_map = maps[src]
        i = bisect(src_range_starts, num)-1
        if i > -1:
            range_max, offset = range_map[src_range_starts[i]]
            if num <= range_max:
                num += offset
        src = dest
    if min_location is None or num < min_location:
        min_location = num
print(min_location)




