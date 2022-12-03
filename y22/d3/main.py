import os
import re

from dataclasses import dataclass

import numpy as np


def priority(char: str):
    if char.isupper():
        return 27 + ord(char) - ord("A")
    else:
        return 1 + ord(char) - ord("a")


def part1(entries):
    sum_ = 0
    for line in entries:
        N = len(line)
        assert N % 2 == 0
        first, second = line[: N // 2], line[N // 2 :]
        in_both = set(first) & set(second)
        sum_ += priority(list(in_both)[0])
    return sum_


def part2(entries):
    sum_ = 0
    for i in range(0, len(entries), 3):
        in_all = list(set(entries[i]) & set(entries[i + 1]) & set(entries[i + 2]))
        assert len(in_all) == 1
        sum_ += priority(in_all[0])
    return sum_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
