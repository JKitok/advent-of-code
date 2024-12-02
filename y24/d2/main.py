import os
import copy
from dataclasses import dataclass
import numpy as np


def is_safe(arr):
    diff = np.diff(arr)
    all_increasing = np.all(diff > 0)
    all_decreasing = np.all(diff < 0)
    all_diff_safe = np.all(np.abs(diff) <= 3)
    return all_diff_safe and (all_increasing or all_decreasing)


def part1(lines):
    N = 0
    for line in lines:
        arr = np.fromstring(line, dtype=int, sep=" ")
        N += is_safe(arr)
    return N


def part2(lines):
    N = 0
    for line in lines:
        arr = np.fromstring(line, dtype=int, sep=" ")
        if is_safe(arr):
            N += 1
        else:
            for i in range(len(arr)):
                if is_safe(np.delete(arr, i)):
                    N += 1
                    break
    return N


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    print(f"Part 1: {part1(copy.deepcopy(lines))}")
    print(f"Part 2: {part2(copy.deepcopy(lines))}")
