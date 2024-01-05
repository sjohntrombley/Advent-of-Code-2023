from itertools import groupby
from math import comb

with open('12_input.txt') as f:
    rows = []
    for line in f:
        row, group_sizes = line.split(' ')
        rows.append(('?'.join([row]*5), [int(s) for s in group_sizes.split(',')]*5))
#rows = [
#    ('???.###????.###????.###????.###????.###', [1, 1, 3]*5),
#    ('.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.', [1, 1, 3]*5),
#    ('?#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#?', [1, 3, 1, 6]*5),
#    ('????.#...#...?????.#...#...?????.#...#...?????.#...#...?????.#...#...', [4, 1, 1]*5),
#    ('????.######..#####.?????.######..#####.?????.######..#####.?????.######..#####.?????.######..#####.', [1, 6, 5]*5),
#    ('?###??????????###??????????###??????????###??????????###????????', [3, 2, 1]*5),
#]
with open('12_1_arrangement_counts.txt') as f:
    arr_counts = [int(s) for s in f]
#if len(rows) != len(arr_counts):
#    raise "no matcherino"

def count_arrangements(row: list[tuple[str, int]], group_sizes: list[int]):
    # trivial case for convenience
    if not row and not group_sizes:
        return 1
    # copy the arguments so the recursion doesn't break, the shallow copy is fine because the elements of both lists
    # should be immutable
    row = row[:]
    group_sizes = group_sizes[:]
    damaged_count = sum(n for k, n in row if k == '#')
    unknown_count = sum(n for k, n in row if k == '?')
    # If the number of damaged springs is too great or the number of unknown springs is insufficient to account for the
    # group sizes, this combination is impossible
    if not (0 <= sum(group_sizes)-damaged_count <= unknown_count):
        return 0
    # match the beginning of the row with the group sizes until we either come across a series of undamaged springs
    # followed by a series of unknown springs or discover this combination is impossible
    while row and row[0][0] != '?':
        # remove leading undamaged springs
        if row[0][0] == '.':
            row.pop(0)
        # handle rows starting with undamaged springs
        if row and row[0][0] == '#':
            # if there are still more damaged springs, but we're out of groups, this arrangement is impossible
            if not group_sizes:
                return 0
            # otherwise we eat series from row until either a series of damaged springs as long as the first group is
            # created or this arrangement is proven impossible
            while True:
                # if the series of damaged springs is longer than the first group, this configuration is impossible
                if row[0][1] > group_sizes[0]:
                    return 0
                if row[0][1] == group_sizes[0]:
                    # if the next group is unknown, the first spring must be undamaged
                    if len(row) > 1 and row[1][0] == '?':
                        if row[1][1] == 1:
                            row.pop(1)
                        else:
                            row[1] = ('?', row[1][1]-1)
                    row.pop(0)
                    group_sizes.pop(0)
                    break
                # if there isn't another group in the row or the next group is undamaged, this arrangement is impossible
                if len(row) == 1 or row[1][0] == '.':
                    return 0
                remaining_damaged = group_sizes[0] - row[0][1]
                if remaining_damaged < row[1][1]:
                    # If there's only one extra unknown spring after the group of damaged springs, it must be undamaged
                    if row[1][1] - remaining_damaged == 1:
                        row.pop(1)
                    else:
                        row[1] = ('?', row[1][1]-remaining_damaged-1)
                    row.pop(0)
                    group_sizes.pop(0)
                    break
                if remaining_damaged == row[1][1]:
                    # if the series of unknown springs is followed by a series of damaged springs, this arrangement is
                    # impossible
                    if len(row)>2 and row[2][0] == '#':
                        return 0
                    del row[:3]
                    group_sizes.pop(0)
                    break
                # if the series of damaged springs plus the following series of unknown springs at the start of the row
                # isn't long enough to account for the first group and there is no following series or the following
                # series is comprised of undamaged springs, then this arrangement is impossible
                if len(row) < 3 or row[2][0] == '.':
                    return 0
                group_sizes[0] -= row[0][1] + row[1][1]
                del row[:2]

    # if the entire row has been consumed then either groups is also empty, so there is one possible arrangement, or
    # there are still groups of damaged springs, in which case there are no possible arrangements.
    if not row:
        if group_sizes:
            return 0
        return 1
    # Handle the case where the series of unknown springs is the entire row
    if len(row) == 1:
        groups_min = max(0, sum(group_sizes) + len(group_sizes) - 1)
        # if we cannot fit the groups into the unknown series, there are no possible arrangements.
        if groups_min > row[0][1]:
            return 0
        free_undamaged_count = row[0][1] - groups_min
        return comb(len(group_sizes) + free_undamaged_count, free_undamaged_count)
    # Handle the case where the series of unknown springs is followed by a series of undamaged springs
    if row[1][0] == '.':
        i = 0
        min_len = 0
        arr_count = 0
        while min_len <= row[0][1]:
            free_uds_count = row[0][1] - min_len
            arr_count += comb(i+free_uds_count, free_uds_count) * count_arrangements(row[2:], group_sizes[i:])
            i += 1
            if i > len(group_sizes):
                break
            min_len = sum(group_sizes[:i]) + i - 1
        return arr_count
    # Handle the case where there series of unknown springs is followed by a series of damaged springs, which is
    # followed by either nothing or a series of undamaged springs
    if len(row) == 2 or row[2][0] == '.':
        i = 0
        arr_count = 0
        while True:
            # find the first i such that group_sizes[i] >= row[1][1]
            while i < len(group_sizes) and group_sizes[i] < row[1][1]:
                i += 1
            # we've run out of groups large enough for the series of damaged springs
            if i >= len(group_sizes):
                return arr_count
            adjusted_uk_size = row[0][1] + row[1][1] - group_sizes[i]
            min_len = sum(group_sizes[:i]) + i
            if i > 0:
                min_len -= 1
                adjusted_uk_size -= 1
            if min_len > adjusted_uk_size:
                return arr_count
            free_ud_count = adjusted_uk_size - min_len
            arr_count += comb(i+free_ud_count, free_ud_count) * count_arrangements(row[3:], group_sizes[i+1:])
            i += 1

    # Handle the case where the series of unknown springs is followed by a series of damaged springs, which is followed
    # by a series of unknown springs
    i = 0
    arr_count = 0
    while True:
        while i < len(group_sizes) and group_sizes[i] < row[1][1]:
            i += 1
        if i >= len(group_sizes):
            return arr_count
        min_len = max(0, sum(group_sizes[:i]) + i - 1)  # do the if statement thing
        if min_len+1 > row[0][1]:
            return arr_count
        j_ub = row[0][1] - min_len
        if i == 0:
            j_ub += 1
        j_ub = min(j_ub, group_sizes[i]-row[1][1]+1)
        for j in range(j_ub):
            free_ud_count = row[0][1] - min_len - j
            if i > 0:
                free_ud_count -= 1
            arr_count += (
                    comb(i+free_ud_count, free_ud_count)
                    * count_arrangements(row[1:], [group_sizes[i]-j] + group_sizes[i+1:])
            )
        i += 1


ans = 0
for i, ((row, group_sizes), expected_arr_count) in enumerate(zip(rows, arr_counts)):
    row = [(k, sum(1 for _ in g)) for k, g in groupby(row)]
    arr_count = count_arrangements(row, group_sizes)
    ans += arr_count
    print(i)
print()
print(ans)


