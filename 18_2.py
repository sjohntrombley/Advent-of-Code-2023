#example_dig_plan = [
#    (0, int('70c71', 16)),
#    (1, int('0dc57', 16)),
#    (0, int('5713f', 16)),
#    (1, int('d2c08', 16)),
#    (0, int('59c68', 16)),
#    (1, int('411b9', 16)),
#    (2, int('8ceee', 16)),
#    (3, int('caa17', 16)),
#    (2, int('1b58a', 16)),
#    (1, int('caa17', 16)),
#    (2, int('7807d', 16)),
#    (3, int('a77fa', 16)),
#    (2, int('01523', 16)),
#    (3, int('7a21e', 16))
#]
example_dig_plan = [
    (2, 6),
    (3, 5),
    (0, 2),
    (3, 2),
    (2, 2),
    (3, 2),
    (0, 5),
    (1, 2),
    (0, 1),
    (1, 2),
    (2, 2),
    (1, 3),
    (0, 2),
    (1, 2)
]
dir_map = {'U': 3, 'R': 0, 'D': 1, 'L': 2}


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

    vertices = [(1, 1)]
    for direction, length in dig_plan:
        vertices.append((
            vertices[-1][0] + 2*(direction&1)*(1-(direction&2))*length,
            vertices[-1][1] + (direction&2)*(1-2*(direction&1))*length
        ))
    print([(r/2, c/2) for r, c in vertices])


if __name__ == '__main__':
    solve(example_dig_plan)
