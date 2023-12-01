import os
import re

from dataclasses import dataclass

import numpy as np


def part1(lines):
    sum_ = 0
    for line in lines:
        first = next((v for v in line if v.isdigit()))
        last = next((v for v in reversed(line) if v.isdigit()))
        num = int(first + last)
        sum_ += num
    return sum_


NUMBERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def part2(lines):
    sum_ = 0
    for line in lines:
        forward_idxs = {}
        backward_idxs = {}
        for i, n in enumerate(NUMBERS):
            positions = [
                *[r.start(0) for r in re.finditer(n, line)],
                *[r.start(0) for r in re.finditer(str(i + 1), line)],
            ]
            forward_idxs[i + 1] = (
                min(positions) if len(positions) > 0 else len(lines) + 1
            )
            backward_idxs[i + 1] = max(positions) if len(positions) > 0 else -1
        forward_number = min(forward_idxs, key=forward_idxs.get)
        backward_number = max(backward_idxs, key=backward_idxs.get)
        N = forward_number * 10 + backward_number
        sum_ += N

    return sum_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
