example_dig_plan = [
    (0, int('70c71', 16)),
    (1, int('0dc57', 16)),
    (0, int('5713f', 16)),
    (1, int('d2c08', 16)),
    (0, int('59c68', 16)),
    (1, int('411b9', 16)),
    (2, int('8ceee', 16)),
    (3, int('caa17', 16)),
    (2, int('1b58a', 16)),
    (1, int('caa17', 16)),
    (2, int('7807d', 16)),
    (3, int('a77fa', 16)),
    (2, int('01523', 16)),
    (3, int('7a21e', 16))
]
dir_map = {'U': 3, 'R': 0, 'D': 1, 'L': 2}


def read_input(file_name):
    with open(file_name) as f:
        lines = [line.split() for line in f]
    return [
        (int(color[7]), int(color[2:7], 16))
        for _, _, color in lines
    ]


def solve(dig_plan):
    # 1 if the loop is clockwise, -1 if the loop is counterclockwise
    loop_dir = sum(
        (src_edge[0] - dest_edge[0]) % 4 - 2
        for src_edge, dest_edge in zip(dig_plan, dig_plan[1:])
    ) // 3

    # generate the path along the center of the trench
    vertices = [(1, 1)]
    for direction, length in dig_plan:
        # (direction&1) is 1 if the direction is vertical and 0 if the direction is horizontal
        vertices.append((
            vertices[-1][0] + 2*(direction&1)*(1-(direction&2))*length,
            vertices[-1][1] + 2*(1-(direction&1))*(1-(direction&2))*length
        ))

    # expand the path to account for the width of the trench
    for i, ((d0, _), (d1, _)) in enumerate(zip(
            dig_plan[-1:] + dig_plan,
            dig_plan + dig_plan[:1]
    )):
        r, c = vertices[i]
        vertices[i] = (
            (
                r + loop_dir*(
                    # d&1 is 1 if d is U or D and 0 if d is L or R
                    # d&2 is 2 if d is L or U and 0 if d is R or D
                    (d1&1)*(d0&2) + (d0&1)*(d1&2) - 1
                )
            )//2,
            (c + loop_dir*(
                (d1&1)*(2-(d1&2)) + (d0&1)*(2-(d0&2)) - 1
            ))//2
        )

    # calculate volume
    volume = 0
    for (r0, c0), (r1, c1) in zip(vertices, vertices[1:]):
        # if r1-r0 is nonzero then c0==c1
        volume += (r1-r0)*c0

    print(volume)


if __name__ == '__main__':
    solve(read_input('18_input.txt'))
