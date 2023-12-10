import os
import copy

from dataclasses import dataclass

import numpy as np


def max_9(v):
    if isinstance(v, int):
        return v % 10
    else:
        return v


def print_grid(lines):
    print("")
    for line in lines:
        print("".join((str(max_9(v)) for v in line)))
    print("")


def find_start(lines):
    x, y = np.where(lines == "S")
    return x[0], y[0]


def find_start_direction(lines, x, y, first=True):
    for x1, y1, valid in [
        (x - 1, y, ["-", "L", "F"]),
        (x + 1, y, ["-", "J", "\\"]),
        (x, y - 1, ["|", "F", "\\"]),
        (x, y + 1, ["|", "J", "L"]),
    ]:
        if not 0 <= x1 < len(lines[0]):
            continue
        if not 0 <= y1 < len(lines):
            continue
        v = lines[y1][x1]
        if v != "." and v in valid:
            if first:
                return x1 - x, y1 - y
            else:
                first = True


def find_next_direction(dx, dy, s):
    if s == "-" or s == "|":
        return dx, dy
    elif s == "\\":
        return dy, dx
    elif s == "J":
        return -dy, -dx
    elif s == "L":
        return dy, dx
    elif s == "F":
        return -dy, -dx
    else:
        raise ValueError(s)


def traverse_pipe(array, start_x, start_y, first, func):
    x, y = start_x, start_y
    dx, dy = find_start_direction(array, x, y, first)
    s = lines[y + dy][x + dx]
    continue_ = True
    while not s == "S" and continue_:
        x += dx
        y += dy
        continue_ = func(x, y, dx, dy, s)
        dx, dy = find_next_direction(dx, dy, s)
        s = lines[y + dy][x + dx]


class MarkDistance:
    def __init__(self, grid):
        self.step = 1
        self.grid = np.zeros_like(grid, dtype=np.int64)

    def __call__(self, x, y, dx, dy, s):
        self.grid[y][x] = self.step
        self.step += 1
        return True


def part1(array):
    y, x = find_start(array)
    dist1 = MarkDistance(array)
    dist2 = MarkDistance(array)
    traverse_pipe(array, x, y, first=True, func=dist1)
    traverse_pipe(array, x, y, first=False, func=dist2)
    return np.max(np.minimum(dist1.grid, dist2.grid))


def part2(array):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "example.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip().replace("7", "\\") for v in lines]
    lines = [list(v) for v in lines]
    arr = np.array(lines, dtype=np.str_)

    print(f"Part 1: {part1(arr)}")
    print(f"Part 2: {part2(arr)}")
