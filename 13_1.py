with open('13_input.txt') as f:
    patterns = [p.split('\n') for p in f.read().strip().split('\n\n')]

ans = 0
for pattern in patterns:
    found = False
    mul = 100
    for _ in range(2):
        for i in range(len(pattern)-1):
            if all(pattern[i-j] == pattern[i+j+1] for j in range(min(i+1, len(pattern)-i-1))):
                ans += mul * (i+1)
                found = True
                break
        if found:
            break
        pattern = [''.join(c) for c in zip(*pattern)]
        mul = 1
print(ans)
