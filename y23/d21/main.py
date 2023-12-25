import os
from tqdm import tqdm
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


def fix(num):
    v = np.int64(str(num).replace("2", "1").replace("3", "1").replace("4", "1"))
    return v


def part2(array, N=10):
    res = np.where(array == "S")
    x0 = res[0][0]
    x1 = res[1][0]
    nums = np.zeros_like(array, dtype=np.int64)
    nums[x0, x1] = 1
    mask = np.zeros_like(array, dtype=np.bool_)
    mask[np.where(array == ".")] = 1
    mask[x0, x1] = 1
    for i in tqdm(range(N)):
        new_nums = np.zeros_like(nums)
        new_nums[1:, :] += nums[:-1, :]
        new_nums[:-1, :] += nums[1:, :]
        new_nums[:, 1:] += nums[:, :-1]
        new_nums[:, :-1] += nums[:, 1:]
        new_nums[0, :] += 10 * nums[-1, :]
        new_nums[-1, :] += 10 * nums[0, :]
        new_nums[:, 0] = 10 * nums[:, -1]
        new_nums[:, -1] = 10 * nums[:, 0]
        new_nums = np.multiply(mask, new_nums)
        indices = np.where(new_nums > 0)
        for i, j in zip(indices[0], indices[1]):
            new_nums[i, j] = fix(new_nums[i, j])
        print(nums)
        nums = new_nums

    N = 0
    non_zero = np.where(nums > 0)
    for i, j in zip(indices[0], indices[1]):
        val = nums[i, j]
        while val > 0:
            is_val = val % 10
            if is_val:
                N += 1
            val //= 10

    return N


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "example.txt")) as fp:
        lines = fp.readlines()

    lines = [list(v.strip()) for v in lines]
    arr = np.array(lines, dtype=np.str_)
    # print(f"Part 1: {part1(arr)}")
    print(f"Part 2: {part2(arr)}")
