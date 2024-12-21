import os
import copy
from dataclasses import dataclass
import numpy as np


def fill(grid, lines):
    # Simulate
    for x, y in (l.split(",") for l in lines):
        grid[int(y), int(x)] = 1


def find_shortest_path(grid):
    FILL = 1_000_000_000
    visited = np.zeros_like(grid, dtype=bool)
    cost = np.zeros_like(grid)
    cost.fill(FILL)
    cost[0, 0] = 0
    end_y, end_x = grid.shape
    end_y -= 1
    end_x -= 1
    while not visited[end_y, end_x]:
        y, x = np.unravel_index(
            np.ma.argmin(np.ma.MaskedArray(cost, visited)), cost.shape
        )
        c = cost[y, x]
        if c == FILL:
            # Found no path
            return None
        for dx, dy in ((1, 0), (-1, 0), (0, -1), (0, 1)):
            new_y = y + dy
            new_x = x + dx
            if not (0 <= new_x < grid.shape[1]) or not (0 <= new_y < grid.shape[0]):
                continue
            if grid[new_y, new_x] == 1:
                continue
            if cost[new_y, new_x] > c + 1:
                cost[new_y, new_x] = c + 1
        visited[y, x] = True
    return cost[end_y, end_x]


def part1(size, lines, n):
    grid = np.zeros((size, size), dtype=int)
    fill(grid, lines[:n])
    return find_shortest_path(grid)


def part2(size, lines):
    start = 0
    end = len(lines)
    # Divide and conquer
    while end - start > 1:
        check = start + (end - start) // 2
        grid = np.zeros((size, size), dtype=int)
        fill(grid, lines[:check])
        if find_shortest_path(grid) is not None:
            start = check
        else:
            end = check
    return lines[start]


if __name__ == "__main__":
    if False:
        file = "example.txt"
        size = 7
        n = 12
    else:
        file = "input.txt"
        size = 71
        n = 1024
    with open(os.path.join(os.path.dirname(__file__), file)) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    print(f"Part 1: {part1(size, copy.deepcopy(lines), n)}")
    print(f"Part 2: {part2(size, copy.deepcopy(lines))}")
