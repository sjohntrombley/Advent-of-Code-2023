import re

fnns = {
    'zero': 0, 'one': 10, 'two': 20, 'three': 30, 'four': 40,
    'five': 50, 'six': 60, 'seven': 70, 'eight': 80, 'nine': 90
}
rnns = {s[::-1]: n//10 for s, n in fnns.items()}

fre = re.compile(r'\d|zero|one|two|three|four|five|six|seven|eight|nine')
rre = re.compile(r'\d|orez|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin')
s = 0
with open('01_input.txt') as f:
    for l in f:
        n = fre.search(l)[0]
        if n.isdigit():
            s += int(n)*10
        else:
            s += fnns[n]

        n = rre.search(l[::-1])[0]
        if n.isdigit():
            s += int(n)
        else:
            s += rnns[n]

print(s)
