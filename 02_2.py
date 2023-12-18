import re

games = {}
with open('02_input.txt') as f:
    for l in f:
        game_number, samples = re.fullmatch(r'Game ([1-9]\d*): (.+)\n?', l).groups()
        samples_list = []
        while samples:
            sample, samples = re.fullmatch(r'([^;]+)(?:; (.+))?', samples).groups()
            sample_dict = {}
            while sample:
                n, color, sample = re.fullmatch(r'([1-9]\d*) ([a-zA-Z]+)(?:, (.+))?', sample).groups()
                sample_dict[color] = int(n)
            samples_list.append(sample_dict)
        games[int(game_number)] = samples_list

ans = 0
for samples in games.values():
    power = 1
    if any('red' in sample for sample in samples):
        power *= max(sample['red'] for sample in samples if 'red' in sample)
    if any('green' in sample for sample in samples):
        power *= max(sample['green'] for sample in samples if 'green' in sample)
    if any('blue' in sample for sample in samples):
        power *= max(sample['blue'] for sample in samples if 'blue' in sample)
    ans += power
print(ans)