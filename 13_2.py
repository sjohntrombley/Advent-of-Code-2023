with open('13_input.txt') as f:
     patterns = [p.split('\n') for p in f.read().strip().split('\n\n')]

ans = 0
for pattern in patterns:
    found = False
    mul = 100
    for _ in range(2):
        for i in range(1, len(pattern), 2):
            noMirror = False
            smudgeFound = False
            for j in range(i//2 + 1):
                diff = sum(x!=y for x, y in zip(pattern[j], pattern[i-j]))
                if diff>1 or diff==1 and smudgeFound:
                    noMirror = True
                    break
                if diff == 1:
                    smudgeFound = True
            if not noMirror and smudgeFound:
                found = True
                ans += (i+1)//2 * mul
                break
        if found:
            break
        for i in range(len(pattern)%2, len(pattern)-1, 2):
            noMirror = False
            smudgeFound = False
            for j in range((len(pattern)-i)//2):
                diff = sum(x != y for x, y in zip(pattern[i+j], pattern[-j-1]))
                if diff > 1 or diff == 1 and smudgeFound:
                    noMirror = True
                    break
                if diff == 1:
                    smudgeFound = True
            if not noMirror and smudgeFound:
                found = True
                ans += (i + len(pattern)) // 2 * mul
                break
        if found:
            break
        pattern = [''.join(c) for c in zip(*pattern)]
        mul = 1
print(ans)
