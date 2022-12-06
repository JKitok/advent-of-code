import os
import re

from dataclasses import dataclass

import numpy as np


def find_start(line: str, N):
    for i in range(N, len(line)):
        first_packet = len(set(line[i - N : i])) == N
        if first_packet:
            return i
    return None


def part1(entries):
    return find_start(entries[0], N=4)


def part2(entries):
    return find_start(entries[0], N=14)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
