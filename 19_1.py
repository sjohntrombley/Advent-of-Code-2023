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


def solve(workflows, parts):
    total = 0
    for part in parts:
        wf = 'in'
        while wf not in 'AR':
            cond_rules, def_rule = workflows[wf]
            cond_match = False
            for i, cmp, n, dest in cond_rules:
                if cmp=='<' and part[i]<n or cmp=='>' and part[i]>n:
                    cond_match = True
                    wf = dest
                    break
            if not cond_match:
                wf = def_rule
        if wf == 'A':
            total += sum(part)
    print(total)


if __name__ == '__main__':
    print(solve(*read_input('19_input.txt')))