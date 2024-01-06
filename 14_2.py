#platform = [
#    list('O....#....'),
#    list('O.OO#....#'),
#    list('.....##...'),
#    list('OO.#O....O'),
#    list('.O.....O#.'),
#    list('O.#..O.#.#'),
#    list('..O..#O..O'),
#    list('.......O..'),
#    list('#....###..'),
#    list('#OO..#....')
#]
with open('14_input.txt') as f:
    platform = [list(r) for r in f.read().strip().split('\n')]


def spin_cycle(platform):
    for _ in range(4):
        for i in range(1, len(platform)):
            for j in range(len(platform[i])):
                if platform[i][j] == 'O':
                    platform[i][j] = '.'
                    for k in range(i-1, -2, -1):
                        if k==-1 or platform[k][j]!='.':
                            platform[k+1][j] = 'O'
                            break
        platform = [list(reversed(col)) for col in zip(*platform)]
    return platform


from time import perf_counter
start = perf_counter()
seen = {}
for cc in range(1_000_000_000):
    ps = '\n'.join(''.join(r) for r in platform)
    if ps in seen:
        break
    seen[ps] = cc
    platform = spin_cycle(platform)
if ps in seen:
    cycle_len = cc - seen[ps]
    for _ in range((1_000_000_000-seen[ps])%cycle_len):
        platform = spin_cycle(platform)
print(sum(d*r.count('O') for d, r in enumerate(reversed(platform), 1)))
print(perf_counter()-start)