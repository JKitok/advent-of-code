import os
import re

from dataclasses import dataclass

import numpy as np


def part1(array):
    # Expand rows
    indices = np.where(np.sum(array, 1) == 0)
    for idx in reversed(*indices):
        array = np.insert(array, idx, np.zeros((1, array.shape[1])), axis=0)
    # Expand columns
    indices = np.where(np.sum(array, 0) == 0)
    for idx in reversed(*indices):
        array = np.insert(array, idx, np.zeros((1, array.shape[0])), axis=1)
    # Calculate pairwise distances
    locations = np.where(array > 0)
    sum_ = 0
    for i in range(len(locations[0]) - 1):
        for j in range(i, len(locations[0])):
            sum_ += abs(locations[0][i] - locations[0][j]) + abs(
                locations[1][i] - locations[1][j]
            )
    return sum_


def part2(array):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip().replace("#", "1").replace(".", "0") for v in lines]
    lines = [list(v) for v in lines]
    arr = np.array(lines, dtype=np.int64)

    print(f"Part 1: {part1(arr)}")
    print(f"Part 2: {part2(arr)}")
