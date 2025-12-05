import os
import copy
import numpy as np


def part1(array):
    sum_ = 0
    for i in range(1, array.shape[0] - 1):
        for j in range(1, array.shape[1] - 1):
            if array[i, j] == 0:
                continue
            if np.sum(array[i - 1 : i + 2, j - 1 : j + 2].flatten()) - array[i, j] < 4:
                sum_ += 1
    return sum_


def part2(array):
    original_rolls = np.sum(np.sum(array))
    current_rolls = 1e9
    new_rolls = original_rolls
    while new_rolls < current_rolls:
        current_rolls = new_rolls
        new_array = np.copy(array)
        for i in range(1, array.shape[0] - 1):
            for j in range(1, array.shape[1] - 1):
                if array[i, j] == 0:
                    continue
                if (
                    np.sum(array[i - 1 : i + 2, j - 1 : j + 2].flatten()) - array[i, j]
                    < 4
                ):
                    new_array[i, j] = 0
        array = new_array
        new_rolls = np.sum(np.sum(array))
    return original_rolls - new_rolls


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = [line.strip() for line in fp if line.strip()]

    array = np.array([[1 if c == "@" else 0 for c in line] for line in lines])
    padded = np.pad(array, pad_width=1, mode="constant", constant_values=0)
    print(f"Part 1: {part1(copy.deepcopy(padded))}")
    print(f"Part 2: {part2(copy.deepcopy(padded))}")
