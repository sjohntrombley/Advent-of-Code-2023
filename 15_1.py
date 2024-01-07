with open('15_input.txt') as f:
    init_seq = f.read().strip().split(',')
ans = 0
for step in init_seq:
    hash_ = 0
    for c in step:
        hash_ = (hash_+ord(c)) * 17 % 256
    ans += hash_
print(ans)
