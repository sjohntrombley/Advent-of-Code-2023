with open('15_input.txt') as f:
    init_seq = f.read().strip().split(',')

boxes = [{} for _ in range(256)]
for step in init_seq:
    if step[-1] == '-':
        op = '-'
        label = step[:-1]
    else:
        op = '='
        label = step[:-2]
        power = int(step[-1])
    hash_ = 0
    for c in label:
        hash_ = (hash_+ord(c)) * 17 % 256

    if op == '-':
        if label in boxes[hash_]:
            boxes[hash_].pop(label)
    else:
        boxes[hash_][label] = power

print(sum(bn*sn*p for bn, box in enumerate(boxes, 1) for sn, p in enumerate(box.values(), 1)))