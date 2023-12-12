import os
import re

from dataclasses import dataclass

import numpy as np


def run(array, expansion=1):
    row_indices = np.where(np.sum(array, 1) == 0)[0]
    col_indices = np.where(np.sum(array, 0) == 0)[0]
    # Calculate pairwise distances
    locations = np.where(array > 0)
    sum_ = 0
    for i in range(len(locations[0]) - 1):
        for j in range(i, len(locations[0])):
            x1 = locations[0][i]
            x2 = locations[0][j]
            y1 = locations[1][i]
            y2 = locations[1][j]

            dx = abs(x2 - x1) + expansion * np.sum(
                (min(x1, x2) < row_indices) & (row_indices < max(x1, x2))
            )
            dy = abs(y2 - y1) + expansion * np.sum(
                (min(y1, y2) < col_indices) & (col_indices < max(y1, y2))
            )
            sum_ += dx + dy
    return sum_


def part2(array):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip().replace("#", "1").replace(".", "0") for v in lines]
    lines = [list(v) for v in lines]
    arr = np.array(lines, dtype=np.int64)

    print(f"Part 1: {run(arr, expansion=1)}")
    print(f"Part 2: {run(arr, expansion=1000000 - 1)}")
