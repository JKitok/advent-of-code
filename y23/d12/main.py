import os
from functools import cache

from tqdm import tqdm


@cache
def possible_solutions(record, groups, current_group_count=0):
    if not record:
        return not groups and current_group_count == 0

    num_solutions = 0
    possible_values = ["#", "."] if record[0] == "?" else record[0]
    for c in possible_values:
        if c == "#":
            num_solutions += possible_solutions(
                record[1:], groups, current_group_count + 1
            )
        else:
            if current_group_count == 0:
                num_solutions += possible_solutions(
                    record[1:], groups, current_group_count
                )
            else:
                if groups and current_group_count == groups[0]:
                    num_solutions += possible_solutions(record[1:], groups[1:], 0)
                else:
                    continue
    return num_solutions


def part1(lines):
    sum_ = 0
    for line in lines:
        broken_record, groups = map(str.strip, line.split(" "))
        groups = tuple(int(v) for v in groups.split(","))
        sum_ += possible_solutions(broken_record + ".", groups)
    return sum_


def part2(lines):
    sum_ = 0
    for line in tqdm(lines):
        broken_record, groups = map(str.strip, line.split(" "))
        broken_record = "?".join([broken_record] * 5)
        groups = ",".join([groups] * 5)
        groups = tuple(int(v) for v in groups.split(","))
        sum_ += possible_solutions(broken_record + ".", groups)
    return sum_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
