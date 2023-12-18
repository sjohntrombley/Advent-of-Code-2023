from math import sqrt, isqrt

with open('06_input.txt') as f:
    time_line, distance_line = f.read().strip().split('\n')
time = int(''.join(time_line.split()[1:]))
distance = int(''.join(distance_line.split()[1:]))
print(time)
print(distance)
r2 = time**2 - 4*distance
r = sqrt(r2)
ways = int(time+r)//2 - int(time-r)//2
if isqrt(r2)**2 == r2:
    ways -= 1
print(ways)





