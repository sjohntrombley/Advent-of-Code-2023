from bisect import insort, bisect

with open('05_input.txt') as f:
    input_ = f.read().strip().split('\n\n')
seeds = [int(seed) for seed in input_[0].split()[1:]]
src_ranges = [(s, s+l-1) for s, l in zip(seeds[::2], seeds[1::2])]
maps = {}
for map_ in input_[1:]:
    map_rows = map_.split('\n')
    source_name, _, dest_name = map_rows[0].split()[0].split('-')
    maps[source_name] = (dest_name, [], {})
    for row in map_rows[1:]:
        dest_range_start, source_range_start, range_length = [int(n) for n in row.split()]
        insort(maps[source_name][1], source_range_start)
        maps[source_name][2][source_range_start] = (source_range_start+range_length-1, dest_range_start-source_range_start)

src = 'seed'
while src != 'location':
    dest, src_range_starts, src_range_map = maps[src]
    dest_ranges = []
    while src_ranges:
        src_range_start, src_range_stop = src_ranges.pop()
        i = bisect(src_range_starts, src_range_start)-1
        if i == -1:
            if src_range_stop < src_range_starts[0]:
                dest_ranges.append((src_range_start, src_range_stop))
            else:
                dest_ranges.append((src_range_start, src_range_starts[0]-1))
                src_ranges.append((src_range_starts[0], src_range_stop))
        else:
            test_range_start = src_range_starts[i]
            test_range_stop, offset = src_range_map[test_range_start]
            if src_range_start <= test_range_stop:
                if src_range_stop <= test_range_stop:
                    dest_ranges.append((src_range_start+offset, src_range_stop+offset))
                else:
                    dest_ranges.append((src_range_start+offset, test_range_stop+offset))
                    src_ranges.append((test_range_stop+1, src_range_stop))
            elif i+1 == len(src_range_starts) or src_range_stop < src_range_starts[i+1]:
                dest_ranges.append((src_range_start, src_range_stop))
            else:
                next_range_start = src_range_start[i+1]
                dest_ranges.append((src_range_start, next_range_start-1))
                src_ranges.append((next_range_start, src_range_stop))
    dest_ranges.sort()
    src_ranges = [dest_ranges.pop()]
    while dest_ranges:
        test_range_start, test_range_stop = dest_ranges.pop()
        if test_range_stop >= src_ranges[-1][0]:
            src_ranges[-1] = (test_range_start, max(test_range_stop, src_ranges[-1][1]))
        else:
            src_ranges.append((test_range_start, test_range_stop))
    src = dest
print(src_ranges[-1][0])
