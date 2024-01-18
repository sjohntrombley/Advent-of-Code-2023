example_dig_plan = [
    (1, 6, '70c710'),
    (2, 5, '0dc571'),
    (3, 2, '5713f0'),
    (2, 2, 'd2c081'),
    (1, 2, '59c680'),
    (2, 2, '411b91'),
    (3, 5, '8ceee2'),
    (0, 2, 'caa173'),
    (3, 1, '1b58a2'),
    (0, 2, 'caa171'),
    (1, 2, '7807d2'),
    (0, 3, 'a77fa3'),
    (3, 2, '015232'),
    (0, 2, '7a21e3')
]
dir_map = {'U': 0, 'R': 1, 'D': 2, 'L': 3}


def read_input(file_name):
    with open(file_name) as f:
        lines = [line.split() for line in f]
    return [
        (dir_map[direction], int(length), color[2:8])
        for direction, length, color in lines
    ]


def solve(dig_plan):
    # 1 if the loop is clockwise, -1 if the loop is counterclockwise
    loop_dir = sum(
        (src_edge[0] - dest_edge[0]) % 4 - 2
        for src_edge, dest_edge in zip(dig_plan, dig_plan[1:])
    ) // 3

    # If there is no trench, dig_map[r][c] is 0.
    # If there is a horizontal trench, dig_map[r][c] is 1.
    # If there is a vertical trench and the lagoon is to the right of the trench, dig_map[r][c] is 1.
    # If there is a vertical trench and the lagoon is to the left of the trench, dig_map[r][c] is -1.
    dig_map = [[0]]
    map_width, map_height = 1, 1
    r, c = 0, 0
    for direction, length, _ in dig_plan:
        if direction == 0:
            r1 = r - length
            while r >= max(r1, 0):
                dig_map[r][c] = loop_dir
                r -= 1
            while r1 < 0:
                dig_map.insert(0, [0]*c + [loop_dir] + [0]*(map_width-c-1))
                map_height += 1
                r1 += 1
            r = r1
        elif direction == 2:
            r1 = r + length
            while r < min(r1+1, map_height):
                dig_map[r][c] = -loop_dir
                r += 1
            # replace with an extend
            while r1 >= map_height:
                dig_map.append([0]*c + [-loop_dir] + [0]*(map_width-c-1))
                map_height += 1
            r = r1
        elif direction == 1:
            c1 = c + length
            c += 1
            while c < min(c1+1, map_width):
                dig_map[r][c] = 1
                c += 1
            if c1 >= map_width:
                for i, row in enumerate(dig_map):
                    row.extend([int(i == r)]*(c1-map_width+1))
                map_width = c1 + 1
            c = c1
        else:
            c1 = c - length
            c -= 1
            while c >= max(c1, 0):
                dig_map[r][c] = 1
                c -= 1
            if c1 < 0:
                for i in range(len(dig_map)):
                    dig_map[i] = [int(i == r)]*-c1 + dig_map[i]
                map_width -= c1
                c = 0
            else:
                c = c1

    # compute the volume of the trench using the dig_map
    volume = 0
    for row in dig_map:
        inside = False
        for c in range(map_width):
            if row[c] == 0:
                volume += inside
            else:
                volume += 1
                if row[c] == 1:
                    inside = True
                else:
                    inside = False

    print(volume)


if __name__ == '__main__':
    solve(read_input('18_input.txt'))
