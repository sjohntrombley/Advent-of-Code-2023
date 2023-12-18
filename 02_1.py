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
for game_number, samples in games.items():
    if all(
            sample.keys() <= {'red', 'green', 'blue'}
                and ('red' not in sample or sample['red'] <= 12)
                and ('green' not in sample or sample['green'] <= 13)
                and ('blue' not in sample or sample['blue'] <= 14)
            for sample in samples):
        ans += game_number
print(ans)