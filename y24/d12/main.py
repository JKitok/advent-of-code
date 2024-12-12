import os
import numpy as np
from queue import Queue


def get_next_region(visited):
    all_i, all_j = np.where(~visited)
    if len(all_i) > 0:
        return all_i[0], all_j[0]


def run(grid):
    visited = np.zeros_like(grid, dtype=bool)
    part1 = 0
    part2 = 0
    while (c := get_next_region(visited)) is not None:
        type_ = grid[c]
        q = Queue()
        q.put(c)
        area = 0
        perimeter = 0
        corners = 0
        while not q.empty():
            i, j = q.get()
            if visited[i, j]:
                continue
            visited[i, j] = True
            area += 1
            fence = []
            for ii, jj in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
                if not (0 <= i + ii < grid.shape[0] and 0 <= j + jj < grid.shape[1]):
                    perimeter += 1
                    fence.append(True)
                else:
                    if grid[i + ii, j + jj] == type_:
                        fence.append(False)
                        if not visited[i + ii, j + jj]:
                            q.put((i + ii, j + jj))
                    else:
                        perimeter += 1
                        fence.append(True)
            # Check for inner corners
            if (not fence[0]) and (not fence[1]):
                if grid[i + 1, j - 1] != type_:
                    corners += 1
            if (not fence[1]) and (not fence[2]):
                if grid[i - 1, j - 1] != type_:
                    corners += 1
            if (not fence[2]) and (not fence[3]):
                if grid[i - 1, j + 1] != type_:
                    corners += 1
            if (not fence[3]) and (not fence[0]):
                if grid[i + 1, j + 1] != type_:
                    corners += 1
            # Calculate outside corners
            lower_left_corner = 1 if (fence[0] and fence[1]) else 0
            upper_left_corner = 1 if (fence[1] and fence[2]) else 0
            upper_right_corner = 1 if (fence[2] and fence[3]) else 0
            lower_right_corner = 1 if (fence[3] and fence[0]) else 0
            corners += (
                lower_left_corner
                + upper_left_corner
                + upper_right_corner
                + lower_right_corner
            )
        part1 += area * perimeter
        # Number of corners equals number of sides
        part2 += area * corners
    return part1, part2


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    grid = np.array([list(line) for line in lines], dtype=str)
    part1, part2 = run(grid)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
