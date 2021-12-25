import os

import numpy as np


def part1(floor):
    num = 0
    while True:
        old_floor = np.copy(floor)
        for val, axis in [[1, 1], [2, 0]]:
            cucumbers = (floor == val).reshape(floor.shape)
            is_empty = (floor == 0) & np.roll(cucumbers, 1, axis=axis)
            floor[np.roll(is_empty, -1, axis=axis)] = 0
            floor[is_empty] = val
        num += 1
        if np.array_equal(old_floor, floor):
            break
    return num


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.replace(".", "0").replace(">", "1").replace("v", "2") for v in lines]
    lines = [" ".join(v.strip()) for v in lines]
    data = np.fromstring(" ".join(lines), sep=" ").astype(int)
    data = data.reshape((len(lines), int(len(data) / len(lines))))

    print(f"Part 1: {part1(data)}")
