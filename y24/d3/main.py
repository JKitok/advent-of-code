import os
import copy
import re


def part1(lines):
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    res = 0
    for line in lines:
        all_ = re.findall(pattern, line)
        for group in all_:
            res += int(group[0]) * int(group[1])
    return res


def part2(lines):
    pattern = re.compile(r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\))")
    res = 0
    enabled = True
    for line in lines:
        all_ = re.findall(pattern, line)
        for group in all_:
            if group[0] == "do()":
                enabled = True
            elif group[0] == "don't()":
                enabled = False
            else:
                assert group[0].startswith("mul")
                if enabled:
                    res += int(group[1]) * int(group[2])
    return res


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    print(f"Part 1: {part1(copy.deepcopy(lines))}")
    print(f"Part 2: {part2(copy.deepcopy(lines))}")
