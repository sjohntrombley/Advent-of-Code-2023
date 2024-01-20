import re


attr_map = {'x': 0, 'm': 1, 'a': 2, 's': 3}


def read_input(fn):
    with open(fn) as f:
        workflows, parts = f.read().split('\n\n')
    workflows = {
        wf_name: (
            [
                (attr_map[attr], cmp, int(n), dest)
                for attr, cmp, n, dest
                in re.findall(
                    r'([xmas])([<>])(\d+):([AR]|[a-z]+),',
                    cond_rules
                )
            ],
            def_rule
        )
        for wf_name, cond_rules, def_rule
        in re.findall(
            r'^([a-z]+)\{((?:[^},]+,)*)([a-z]+|[AR])}$',
            workflows,
            re.MULTILINE
        )
    }
    parts = [
        tuple(int(n) for n in t)
        for t
        in re.findall(
            r'^\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}$',
            parts,
            re.MULTILINE
        )
    ]
    return workflows, parts


def solve(workflows):
    count = 0
    to_visit = [(*workflows['in'], [1, 4001]*4)]
    while to_visit:
        cond_rules, def_rule, ranges = to_visit.pop()
        if not cond_rules:
            if def_rule == 'A':
                combination_count = 1
                for i in range(4):
                    combination_count *= ranges[2*i+1] - ranges[2*i]
                count += combination_count
            elif def_rule != 'R':
                to_visit.append((*workflows[def_rule], ranges))
        else:
            i, cmp, n, dest = cond_rules[0]
            if cmp == '<':
                # append the case where the condition is false
                if n > ranges[2*i]:
                    if n < ranges[2*i+1]:
                        right_ranges = ranges[:]
                        right_ranges[2*i] = n
                        to_visit.append(
                            (cond_rules[1:], def_rule, right_ranges)
                        )
                else:
                    to_visit.append((cond_rules[1:], def_rule, ranges))
                # append the case where the condition is true
                if n > ranges[2*i]:
                    if n < ranges[2*i+1]:
                        left_ranges = ranges[:]
                        left_ranges[2*i+1] = n
                        if dest == 'A':
                            combination_count = 1
                            for j in range(4):
                                combination_count *= (
                                    left_ranges[2*j+1] - left_ranges[2*j]
                                )
                            count += combination_count
                        elif dest != 'R':
                            to_visit.append((*workflows[dest], left_ranges))
                    else:
                        if dest == 'A':
                            combination_count = 1
                            for j in range(4):
                                combination_count *= (
                                    ranges[2*j+1] - ranges[2*j]
                                )
                            count += combination_count
                        elif dest != 'R':
                            to_visit.append((*workflows[dest], ranges))
            else:
                # append the case where the condition is false
                if n+1 > ranges[2*i]:
                    if n+1 < ranges[2*i+1]:
                        right_ranges = ranges[:]
                        right_ranges[2*i+1] = n+1
                        to_visit.append(
                            (cond_rules[1:], def_rule, right_ranges)
                        )
                    else:
                        to_visit.append((cond_rules[1:], def_rule, ranges))
                # append the case where the condition is true
                if n+1 > ranges[2*i]:
                    if n+1 < ranges[2*i+1]:
                        left_ranges = ranges[:]
                        left_ranges[2*i] = n+1
                        if dest == 'A':
                            combination_count = 1
                            for j in range(4):
                                combination_count *= (
                                        left_ranges[2*j+1] - left_ranges[2*j]
                                )
                            count += combination_count
                        elif dest != 'R':
                            to_visit.append((*workflows[dest], left_ranges))
                else:
                    if dest == 'A':
                        combination_count = 1
                        for j in range(4):
                            combination_count *= ranges[2*j+1] - ranges[2*j]
                        count += combination_count
                    elif dest != 'R':
                        to_visit.append((*workflows[dest], ranges))
    return count


if __name__ == '__main__':
    print(solve(read_input('19_input.txt')[0]))