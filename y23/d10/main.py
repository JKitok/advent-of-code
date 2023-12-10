import os
import copy

from dataclasses import dataclass

import numpy as np


def print_grid(lines):
    print("")
    for line in lines:
        print("".join((str(v) for v in line)))
    print("")


def find_start(lines):
    for y, line in enumerate(lines):
        try:
            x = line.index("S")
            return x, y
        except ValueError:
            continue


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


def traverse_pipe(lines, start_x, start_y, first):
    x, y = start_x, start_y
    dx, dy = find_start_direction(lines, x, y, first)
    step = 1
    s = lines[y + dy][x + dx]

    while not s == "S":
        x += dx
        y += dy
        lines[y][x] = step
        step += 1
        dx, dy = find_next_direction(dx, dy, s)
        s = lines[y + dy][x + dx]
    return lines


def find_min_grid(grid1, grid2):
    max_ = 0
    grid = copy.deepcopy(grid1)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if isinstance(grid[y][x], int):
                grid[y][x] = min(grid1[y][x], grid2[y][x])
                max_ = max(max_, grid[y][x])
    return grid, max_


def part1(lines):
    x, y = find_start(lines)
    line1 = traverse_pipe(copy.deepcopy(lines), x, y, first=True)
    line2 = traverse_pipe(copy.deepcopy(lines), x, y, first=False)
    grid, max_ = find_min_grid(line1, line2)
    # print_grid(grid)
    return max_


def part2(lines):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip().replace("7", "\\") for v in lines]
    lines = [list(v) for v in lines]

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
