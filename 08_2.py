from math import gcd

with open('08_input.txt') as f:
    dir_str, map_str = f.read().strip().split('\n\n')

directions = [0 if c == 'L' else 1 for c in dir_str]
loc_graph = {src: (ldest[1:-1], rdest[:-1]) for src, _, ldest, rdest in (line.split() for line in map_str.split('\n'))}

step = 0
dir_len = len(directions)
src_list = [src for src in loc_graph if src[-1] == 'A']
all_pre_cycle_dests = None
all_cycle_start = None
all_cycle_len = None
all_cycle_dests = None
for src in src_list:
    step = 0
    history = {}
    while (src, step%dir_len) not in history:
        history[(src, step%dir_len)] = step
        src = loc_graph[src][directions[step % dir_len]]
        step += 1
    cycle_start = history[(src, step%dir_len)]
    cycle_len = step - cycle_start
    pre_cycle_dests = {step for (src, _), step in history.items() if src[-1] == 'Z' and step < cycle_start}
    cycle_dests = {step%cycle_len for (src, _), step in history.items() if src[-1] == 'Z' and step >= cycle_start}
    if all_pre_cycle_dests is None:
        all_pre_cycle_dests = pre_cycle_dests
        all_cycle_start = cycle_start
        all_cycle_len = cycle_len
        all_cycle_dests = cycle_dests
    else:
        if all_cycle_start < cycle_start:
            all_pre_cycle_dests |= (
                {
                    n*all_cycle_len + step
                    for step in all_cycle_dests
                    for n in range(all_cycle_start//all_cycle_len, cycle_start//all_cycle_len + 1)
                }
                - {
                    all_cycle_start - all_cycle_start%all_cycle_len + step
                    for step in all_cycle_dests
                    if step < all_cycle_start%all_cycle_len
                }
                - {
                    cycle_start - cycle_start%all_cycle_len + step
                    for step in all_cycle_dests
                    if step >= cycle_start%all_cycle_len
                }
            )
            all_cycle_start = cycle_start
        elif cycle_start < all_cycle_start:
            pre_cycle_dests |= (
                {
                    n*cycle_len + step
                    for step in cycle_dests
                    for n in range(cycle_start//cycle_len, all_cycle_start//cycle_len + 1)
                }
                - {
                    cycle_start - cycle_start%cycle_len + step
                    for step in cycle_dests
                    if step < cycle_start%cycle_len
                }
                - {
                    all_cycle_start - all_cycle_start%cycle_len + step
                    for step in cycle_dests
                    if step >= all_cycle_start%cycle_len
                }
            )
        all_pre_cycle_dests &= pre_cycle_dests

        new_cycle_len = all_cycle_len * cycle_len // gcd(all_cycle_len, cycle_len)
        all_cycle_dests = {
            new_step
            for step in all_cycle_dests
            for n in range(new_cycle_len//all_cycle_len)
            if (new_step := n*all_cycle_len + step) % cycle_len in cycle_dests
        }
        all_cycle_len = new_cycle_len
if len(all_pre_cycle_dests) > 0:
    print(min(all_pre_cycle_dests))
else:
    print(min(
        all_cycle_start - all_cycle_start%all_cycle_len + step
        + (0 if step >= all_cycle_start%all_cycle_len else all_cycle_len)
        for step in all_cycle_dests
    ))







#while any(src[-1] != 'Z' for src in src_list):
#    src_list = [loc_graph[src][directions[step % dir_len]] for src in src_list]
#    step += 1
#print(step)
