import os
import re

import numpy as np


def part1(l1, l2):
    diff = 0
    for v1, v2 in zip(l1, l2):
        diff += abs(v1 - v2)
    return diff


def part2(l1, l2):
    score = 0
    for v1 in l1:
        score += v1 * l2.count(v1)
    return score


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [l.strip() for l in lines]
    l1, l2 = [], []
    for line in lines:
        v1, v2 = line.split()
        l1.append(int(v1))
        l2.append(int(v2))
    l1.sort()
    l2.sort()

    print(f"Part 1: {part1(l1, l2)}")
    print(f"Part 2: {part2(l1, l2)}")
