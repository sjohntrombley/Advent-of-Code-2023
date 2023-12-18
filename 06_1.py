from math import sqrt, isqrt

ans = 1
with open('06_input.txt') as f:
    time_line, distance_line = f.read().strip().split('\n')
for time, distance in zip(map(int, time_line.split()[1:]), map(int, distance_line.split()[1:])):
    r2 = time**2 - 4*distance
    r = sqrt(r2)
    ways = int(time+r)//2 - int(time-r)//2
    if isqrt(r2)**2 == r2:
        ways -= 1
    ans *= ways
print(ans)





