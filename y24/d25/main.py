import os
from itertools import groupby
import numpy as np


def part1(objects):
    locks = []
    keys = []
    for obj in objects:
        obj = [list(v) for v in obj]
        arr = np.array(obj, dtype=str)
        as_int = np.zeros_like(arr, dtype=int)
        as_int[arr == "#"] = 1
        if as_int[0, 0] == 1:
            locks.append(as_int)
        else:
            keys.append(as_int)

    N = 0
    for lock in locks:
        for key in keys:
            if not np.any((lock + key) > 1):
                N += 1
    return N


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    objects = [list(sub) for ele, sub in groupby(lines, key = bool) if ele]

    print(f"Part 1: {part1(objects)}")
