import re

point_total = 0
with open('04_input.txt') as f:
    for line in f:
        winning_numbers, my_numbers = re.fullmatch(r'Card +\d+: +(\d+(?: +\d+)*) \| +(\d+(?: +\d+)*)\n?', line).groups()
        matches = len({int(n) for n in winning_numbers.split()} & {int(n) for n in my_numbers.split()})
        if matches > 0:
            point_total += 2**(matches-1)
print(point_total)