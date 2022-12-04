import os
import re

from dataclasses import dataclass

import numpy as np


def part1(entries):
    count = 0
    for a1, a2, b1, b2 in entries:
        if a1 <= b1 and a2 >= b2:
            count += 1
        elif b1 <= a1 and b2 >= a2:
            count += 1
    return count


def part2(entries):
    count = 0
    for a1, a2, b1, b2 in entries:
        if a2 < b1:
            count += 1
        elif b2 < a1:
            count += 1
    return len(entries) - count


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    entries = [list(map(int, v.replace("-", ",").split(","))) for v in lines]
    print(f"Part 1: {part1(entries)}")
    print(f"Part 2: {part2(entries)}")
