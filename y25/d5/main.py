import os


def part1(groups, indices):
    cnt = 0
    for i in indices:
        for lower, upper in groups:
            if lower <= i <= upper:
                cnt += 1
                break
    return cnt


def part2(groups):
    combined_two_groups = True
    while combined_two_groups:
        combined_two_groups = False
        for i, (lower_1, upper_1) in enumerate(groups):
            if combined_two_groups:
                break
            for i2, (lower_2, upper_2) in enumerate(groups[i + 1 :]):
                j = i + i2 + 1
                if lower_2 <= upper_1 <= upper_2 or lower_1 <= upper_2 <= upper_1:
                    groups = [
                        *groups[:i],
                        *groups[i + 1 : j],
                        *groups[j + 1 :],
                        (min(lower_1, lower_2), max(upper_1, upper_2)),
                    ]
                    combined_two_groups = True
                    break

    return sum((v2 - v1 + 1) for (v1, v2) in groups)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    groups = lines[: lines.index("")]
    groups = [list(map(int, v.split("-"))) for v in groups]
    indices = [*map(int, lines[lines.index("") + 1 :])]
    print(f"Part 1: {part1(groups, indices)}")
    print(f"Part 2: {part2(groups)}")
