from collections import deque


class Broadcaster:
    def __init__(self, dests):
        self.name = 'broadcaster'
        self.dests = dests

    def send(self, src, signal):
        return [(self.name, signal, m) for m in self.dests]

    def all_false(self):
        return True


class FlipFlop:
    def __init__(self, name, dests):
        self.name = name
        self.state = False
        self.dests = dests

    def send(self, src, signal):
        if not signal:
            self.state = not self.state
            return [(self.name, self.state, m) for m in self.dests]
        return []

    def all_false(self):
        return not self.state


class Conjunction:
    def __init__(self, name, dests):
        self.name = name
        self.src_states = {}
        self.dests = dests

    def send(self, src, signal):
        self.src_states[src] = signal
        output = not all(self.src_states.values())
        return [(self.name, output, m) for m in self.dests]

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
    cycle_count = high_count = low_count = 0
    high_history, low_history = [0], [0]
    while cycle_count < 1000:
        pulse_queue = deque([('button', False, 'broadcaster')])
        while pulse_queue:
            src, signal, dest = pulse_queue.popleft()
            if signal:
                high_count += 1
            else:
                low_count += 1
            if dest in modules:
                pulse_queue.extend(modules[dest].send(src, signal))
        high_history.append(high_count)
        low_history.append(low_count)
        cycle_count += 1
        if all(mod.all_false() for mod in modules.values()):
            break
    print(
        (1000//cycle_count)**2*high_count*low_count
        + high_history[1000%cycle_count]*low_history[1000%cycle_count]
    )


if __name__ == '__main__':
    solve(read_input('20_input.txt'))
