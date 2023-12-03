import os
import re

from dataclasses import dataclass

import numpy as np


def check_neighbors(lines, i, j, n):
    for ii in [i - 1, i, i + 1]:
        for jj in range(j - 1, j + n + 1):
            s = lines[ii][jj]
            if s != "." and not s.isdigit():
                return True
    return False


def part1(lines):
    sum_ = 0
    i = 1
    j = 1
    while True:
        if i >= len(lines) - 1:
            return sum_
        if j >= len(lines[0]) - 1:
            i += 1
            j = 1
            continue

        if not lines[i][j].isdigit():
            j += 1
            continue
        else:
            n = 0
            while lines[i][j + n].isdigit():
                n += 1
            num = int(lines[i][j : j + n])
            # Check neighbors
            if check_neighbors(lines, i, j, n):
                sum_ += num
            j += n + 1

    return sum_


def find_number(lines, ii, jj):
    a = 0
    b = 0
    while lines[ii][jj - a].isdigit():
        a += 1
    while lines[ii][jj + b].isdigit():
        b += 1
    num = int(lines[ii][jj - a + 1 : jj + b])
    return num, jj + b


def part2(lines):
    sum_ = 0
    i = 1
    j = 1
    while True:
        if i >= len(lines) - 1:
            return sum_
        if j >= len(lines[0]) - 1:
            i += 1
            j = 1
            continue

        if lines[i][j] != "*":
            j += 1
            continue
        else:
            nums = []
            for ii in [i - 1, i, i + 1]:
                jj = j - 1
                while jj <= j + 1:
                    if not lines[ii][jj].isdigit():
                        jj += 1
                    else:
                        num, jj = find_number(lines, ii, jj)
                        nums.append(num)

            if len(nums) == 2:
                ratio = nums[0] * nums[1]
                sum_ += ratio
            j += 1


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = ["." + v.strip() + "." for v in lines]
    # Do some padding
    empty_line = "." * len(lines[0])
    lines = [empty_line, *lines, empty_line]
    print(lines)

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
