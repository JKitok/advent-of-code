import os
import numpy as np
from queue import Queue


def get_next_region(visited):
    all_i, all_j = np.where(~visited)
    if len(all_i) > 0:
        return all_i[0], all_j[0]


def part1(grid):
    visited = np.zeros_like(grid, dtype=bool)
    total = 0
    while (c := get_next_region(visited)) is not None:
        type_ = grid[c]
        q = Queue()
        q.put(c)
        area = 0
        perimeter = 0
        while not q.empty():
            i, j = q.get()
            if visited[i, j]:
                continue
            visited[i, j] = True
            area += 1
            for ii, jj in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                if 0 <= i + ii < grid.shape[0] and 0 <= j + jj < grid.shape[1]:
                    if grid[i + ii, j + jj] == type_:
                        if not visited[i + ii, j + jj]:
                            q.put((i + ii, j + jj))
                    else:
                        perimeter += 1
                else:
                    perimeter += 1
        total += area * perimeter
    return total


def part2(grid):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    grid = np.array([list(line) for line in lines], dtype=str)
    print(f"Part 1: {part1(grid)}")
    print(f"Part 2: {part2(grid)}")
