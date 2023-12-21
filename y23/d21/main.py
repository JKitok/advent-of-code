import os
from queue import Queue
import numpy as np


def part1(array, N=64):
    res = np.where(array == "S")
    x0 = res[0][0]
    x1 = res[1][0]
    positions = set()
    positions.add((x0, x1))
    i = 0
    while i < N:
        new_set = set()
        for x0, x1 in positions:
            for dx0, dx1 in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x0n = x0 + dx0
                x1n = x1 + dx1
                if not 0 <= x0n < array.shape[0] or not 0 <= x1n < array.shape[1]:
                    continue
                if array[x0n, x1n] in [".", "S"]:
                    new_set.add((x0n, x1n))
        i += 1
        positions = new_set
    return len(positions)


def part2(array, N=6):
    res = np.where(array == "S")
    x0 = res[0][0]
    x1 = res[1][0]
    nums = np.zeros_like(array, dtype=np.int32)
    nums[x0, x1] = 1
    mask = np.zeros_like(array, dtype=np.bool8)
    mask[np.where(array == ".")] = 1
    mask[x0, x1] = 1
    i = 0
    while i < N:
        i += 1
        nums = (
            np.roll(nums, 1)
            + np.roll(nums, -1)
            + np.roll(nums, 1, axis=0)
            + np.roll(nums, -1, axis=0)
        )
        nums[np.where(mask == 0)] = 0
    return np.sum(nums)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "example.txt")) as fp:
        lines = fp.readlines()

    lines = [list(v.strip()) for v in lines]
    arr = np.array(lines, dtype=np.str_)
    # print(f"Part 1: {part1(arr)}")
    print(f"Part 2: {part2(arr)}")
