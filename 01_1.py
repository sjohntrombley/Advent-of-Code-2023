s = 0
with open('01_input.txt') as f:
    for l in f:
        for c in l:
            if c.isdigit():
                s += 10*int(c)
                break
        for c in reversed(l):
            if c.isdigit():
                s += int(c)
                break
print(s)
