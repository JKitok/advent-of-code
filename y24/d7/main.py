import os
import itertools

import numpy as np
import tqdm

ORIENTATIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_guard_position(grid):
    guard_idx = np.where(grid == "^")
    x1 = guard_idx[0][0]
    x2 = guard_idx[1][0]
    return x1, x2


def part1(grid):
    visited = np.zeros_like(grid, dtype=int)
    x1, x2 = get_guard_position(grid)
    direction_iter = itertools.cycle(ORIENTATIONS)
    direction = next(direction_iter)
    while True:
        visited[x1, x2] = 1
        new_x1 = x1 + direction[0]
        new_x2 = x2 + direction[1]
        if not ((0 <= new_x1 < grid.shape[0]) and (0 <= new_x2 < grid.shape[1])):
            break
        elif grid[new_x1, new_x2] != "#":
            x1, x2 = new_x1, new_x2
        else:
            direction = next(direction_iter)
    return np.sum(np.sum(visited))


def part2(grid):
    N = 0
    for obstacle_x1 in tqdm.tqdm(range(grid.shape[0])):
        for obstacle_x2 in range(grid.shape[1]):
            if grid[obstacle_x1, obstacle_x2] != ".":
                continue
            x1, x2 = get_guard_position(grid)
            direction_iter = itertools.cycle(ORIENTATIONS)
            direction = next(direction_iter)
            position_and_direction = set()
            while True:
                idx = (x1, x2, *direction)
                if idx in position_and_direction:
                    N += 1
                    break
                else:
                    position_and_direction.add(idx)
                new_x1 = x1 + direction[0]
                new_x2 = x2 + direction[1]

                if not (
                    (0 <= new_x1 < grid.shape[0]) and (0 <= new_x2 < grid.shape[1])
                ):
                    break
                elif grid[new_x1, new_x2] != "#" and (new_x1, new_x2) != (
                    obstacle_x1,
                    obstacle_x2,
                ):
                    x1, x2 = new_x1, new_x2
                else:
                    direction = next(direction_iter)
    return N


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    grid = np.array([list(line) for line in lines])

    print(f"Part 1: {part1(grid)}")
    print(f"Part 2: {part2(grid)}")
