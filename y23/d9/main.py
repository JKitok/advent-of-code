import os
import re

from dataclasses import dataclass

import numpy as np


def run(numbers):
    sum_1 = 0
    sum_2 = 0
    for nums in numbers:
        diffs = [nums]
        while nums.any():
            nums = np.diff(nums)
            diffs.append(nums)
        v1 = 0
        v2 = 0
        for arr in reversed(diffs):
            v1 = v1 + arr[-1]
            v2 = arr[0] - v2
        sum_1 += v1
        sum_2 += v2
    return sum_1, sum_2


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    numbers = [np.fromstring(l, sep=" ").astype(np.int64) for l in lines]
    p1, p2 = run(numbers)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
