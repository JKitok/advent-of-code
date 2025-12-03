import os
import copy

import numpy as np


def part1(lines):
    sum_ = 0
    for line in lines:
        arr = np.array(list(map(int, line)))
        max = np.argmax(arr[:-1])
        v = 10 * arr[max] + np.max(arr[max + 1 :])
        sum_ += v
    return sum_


def part2(lines):
    sum_ = 0
    for line in lines:
        arr = np.array(list(map(int, line)))
        N = 12
        idx = -1
        v = 0
        while N > 0:
            end = None if N == 1 else -(N - 1)
            max = np.argmax(arr[idx + 1 : end])
            idx = idx + 1 + max
            N -= 1
            v = 10 * v + arr[idx]
        sum_ += v
    return sum_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    print(f"Part 1: {part1(copy.deepcopy(lines))}")
    print(f"Part 2: {part2(copy.deepcopy(lines))}")
