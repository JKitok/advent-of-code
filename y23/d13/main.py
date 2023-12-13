import os
import re

from dataclasses import dataclass

import numpy as np


def run(patterns, value=0):
    sum_ = 0
    for pattern in patterns:
        found = False
        for axis in [0, 1]:
            if not found:
                if axis == 1:
                    pattern = pattern.T
                for idx in range(1, pattern.shape[0]):
                    size = min(idx, pattern.shape[0] - idx)
                    if (
                        np.sum(
                            np.sum(
                                np.abs(
                                    np.flipud(pattern[idx - size : idx, :])
                                    - pattern[idx : idx + size, :]
                                )
                            )
                        )
                        == value
                    ):
                        found = True
                        sum_ += (1 - axis) * 100 * idx + axis * idx
                        break
        assert found
    return sum_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip().replace("#", "1").replace(".", "0") for v in lines]
    patterns = []
    while "" in lines:
        idx = lines.index("")
        matrix = lines[:idx]
        patterns.append(np.array([list(v) for v in matrix], dtype=np.int64))
        lines = lines[idx + 1 :]
    patterns.append(np.array([list(v) for v in lines], dtype=np.int64))
    print(f"Part 1: {run(patterns, value=0)}")
    print(f"Part 2: {run(patterns, value=1)}")
