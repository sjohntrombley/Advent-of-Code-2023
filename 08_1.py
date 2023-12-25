with open('08_input.txt') as f:
    dir_str, map_str = f.read().strip().split('\n\n')

directions = [0 if c == 'L' else 1 for c in dir_str]
loc_graph = {src: (ldest[1:-1], rdest[:-1]) for src, _, ldest, rdest in (line.split() for line in map_str.split('\n'))}

step = 0
dir_len = len(directions)
src = 'AAA'
while src != 'ZZZ':
    src = loc_graph[src][directions[step % dir_len]]
    step += 1
print(step)
