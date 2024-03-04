from collections import deque
from functools import reduce
from operator import and_
from itertools import count
from math import lcm


class Broadcaster:
    def __init__(self, dests):
        self.name = 'broadcaster'
        self.dests = dests

    def send(self, src, signal, depth):
        return [(self.name, signal, m, depth+1) for m in self.dests]

    def all_false(self):
        return True


class FlipFlop:
    def __init__(self, name, dests):
        self.name = name
        self.state = False
        self.dests = dests

    def send(self, src, signal, depth):
        if not signal:
            self.state = not self.state
            return [(self.name, self.state, m, depth+1) for m in self.dests]
        return []

    def all_false(self):
        return not self.state


class Conjunction:
    def __init__(self, name, dests):
        self.name = name
        self.src_states = {}
        self.dests = dests

    def send(self, src, signal, depth):
        self.src_states[src] = signal
        output = not all(self.src_states.values())
        return [(self.name, output, m, depth+1) for m in self.dests]

    def all_false(self):
        return not any(self.src_states.values())


def read_input(fn):
    modules = {}
    conj_names = set()
    with open(fn) as f:
        for line in f:
            module, dests = line.strip().split(' -> ')
            dests = dests.split(', ')
            if module == 'broadcaster':
                modules['broadcaster'] = Broadcaster(dests)
            elif module[0] == '%':
                modules[module[1:]] = FlipFlop(module[1:], dests)
            else:
                modules[module[1:]] = Conjunction(module[1:], dests)
                conj_names.add(module[1:])
    for src_name, src_module in modules.items():
        for dest_name in src_module.dests:
            if dest_name in conj_names:
                modules[dest_name].src_states[src_name] = False
    return modules


def solve(modules):
    group_input_dests = modules['broadcaster'].dests
    groups = {}
    for group_input in group_input_dests:
        mod = modules[group_input]
        groups[group_input] = {group_input} | set(mod.dests)
        to_visit = deque(mod.dests)
        while to_visit:
            mod_name = to_visit.popleft()
            if mod_name in modules:
                mod = modules[mod_name]
                dest_set = set(mod.dests)
                to_visit.extend(dest_set - groups[group_input])
                groups[group_input] |= dest_set
    overlap_set = reduce(and_, groups.values())
    # overlap set should be
    if len(overlap_set) != 2 or 'rx' not in overlap_set:
        raise ValueError()
    final_conj = modules[(overlap_set - {'rx'}).pop()]
    # The node that leads to rx should be a conjunction
    if not isinstance(final_conj, Conjunction):
        raise ValueError()
    final_conj_src_set = set(final_conj.src_states)
    # Every group should contain exactly 1 module that sends a signal
    # to final_conj
    if not all(
        len(g & final_conj_src_set) == 1
        for g in groups.values()
    ):
        raise ValueError()
    histories = []
    for group_in in groups:
        groups[group_in] -= overlap_set
        group_out = (groups[group_in] & final_conj_src_set).pop()
        group_history = []
        for press in count():
            signal_queue = deque([('broadcaster', False, group_in, 0)])
            while signal_queue:
                src_name, signal, dest_name, depth = signal_queue.popleft()
                mod = modules[dest_name]
                if dest_name == group_out:
                    out_signal = mod.send(src_name, signal, depth)[0][1]
                    if (
                        not group_history
                        or group_history[-1][0] != out_signal
                    ):
                        group_history.append((out_signal, press, depth+1))
                else:
                    signal_queue.extend(mod.send(src_name, signal, depth))
            if all(modules[n].all_false() for n in groups[group_in] if isinstance(modules[n], FlipFlop)):
                break
        histories.append(group_history)
    print(histories)
    cycle_lens = [h[-2][1]+1 for h in histories]
    print()
    print(lcm(*cycle_lens))


if __name__ == '__main__':
    solve(read_input('20_input.txt'))
