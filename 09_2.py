with open('09_input.txt') as f:
    value_histories = [[int(s) for s in line.split()] for line in f]

ans = 0
for history in value_histories:
    history.reverse()
    diffs = [history]
    while any(diffs[-1]):
        diffs.append([x-y for x, y in zip(diffs[-1], diffs[-1][1:])])
    diffs[-1].append(0)
    for i in range(len(diffs)-2, -1, -1):
        diffs[i].append(diffs[i][-1]-diffs[i+1][-1])
    ans += diffs[0][-1]
print(ans)
