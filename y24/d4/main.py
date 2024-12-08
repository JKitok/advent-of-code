import os
import numpy as np


def part1(grid):
    SEARCH_ARR = np.array(["X", "M", "A", "S"])
    REVERSED_ARR = SEARCH_ARR[::-1]
    N = len(SEARCH_ARR)
    # Vertical search
    num = 0
    for i in range(0, grid.shape[0] - (N - 1)):
        for j in range(0, grid.shape[1]):
            if (SEARCH_ARR == grid[i : i + N, j]).all():
                num += 1
            elif (REVERSED_ARR == grid[i : i + N, j]).all():
                num += 1
    # Horizontal search
    for j in range(0, grid.shape[1] - (N - 1)):
        for i in range(0, grid.shape[0]):
            if (SEARCH_ARR == grid[i, j : j + N]).all():
                num += 1
            elif (REVERSED_ARR == grid[i, j : j + N]).all():
                num += 1
    # Diagonal search one way
    for i in range(0, grid.shape[0] - (N - 1)):
        for j in range(0, grid.shape[1] - (N - 1)):
            iv = [i, i + 1, i + 2, i + 3]
            jv = [j, j + 1, j + 2, j + 3]
            if (SEARCH_ARR == grid[iv, jv]).all():
                num += 1
            elif (REVERSED_ARR == grid[iv, jv]).all():
                num += 1
    # Diagonal search other way
    for i in range(N - 1, grid.shape[0]):
        for j in range(0, grid.shape[1] - (N - 1)):
            iv = [i, i - 1, i - 2, i - 3]
            jv = [j, j + 1, j + 2, j + 3]
            if (SEARCH_ARR == grid[iv, jv]).all():
                num += 1
            elif (REVERSED_ARR == grid[iv, jv]).all():
                num += 1
    return num


def part2(grid):
    search_arr = np.array(["M", "A", "S"])
    reversed_arr = search_arr[::-1]
    num = 0
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            # First diagonal
            iv = [i - 1, i, i + 1]
            jv = [j - 1, j, j + 1]
            if (search_arr == grid[iv, jv]).all() or (
                reversed_arr == grid[iv, jv]
            ).all():
                # Second diagonal
                iv = [i + 1, i, i - 1]
                jv = [j - 1, j, j + 1]
                if (search_arr == grid[iv, jv]).all() or (
                    reversed_arr == grid[iv, jv]
                ).all():
                    num += 1
    return num


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    grid = np.array([list(line) for line in lines])
    print(f"Part 1: {part1(grid)}")
    print(f"Part 2: {part2(grid)}")
