import os
import numpy as np
from collections import defaultdict

# Precalculate all pairs to check
part1_pairs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
part2_pairs = []
for i in range(-21, 22):
    for j in range(-21, 22):
        if 2 <= abs(i) + abs(j) <= 20:
            part2_pairs.append((i, j))


def run(grid, pairs, to_save):
    distances = np.zeros_like(grid, dtype=int)
    distances.fill(-1)
    end_row, end_col = np.where(grid == "E")
    row = end_row[0]
    col = end_col[0]
    start_row, start_col = np.where(grid == "S")
    start_row = start_row[0]
    start_col = start_col[0]
    dist = 0
    distances[row, col] = dist
    saved = defaultdict(int)
    while True:
        # Check if we can make any shortcuts
        for dr, dc in pairs:
            new_row = row + dr
            new_col = col + dc
            try:
                if (new_dist := distances[new_row, new_col]) != -1:
                    time_saved = dist - new_dist - (abs(dr) + abs(dc))
                    if time_saved >= to_save:
                        saved[time_saved] += 1
            except IndexError:
                pass

        if distances[start_row, start_col] != -1:
            break

        # Find the next step of the route
        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_row = row + dr
            new_col = col + dc
            if (
                grid[new_row, new_col] in (".", "S")
                and distances[new_row, new_col] == -1
            ):
                row = new_row
                col = new_col
                dist += 1
                distances[row, col] = dist
                break
        else:
            raise ValueError()

    for k, v in saved.items():
        print(f"{k} seconds: {v}")

    return sum((v for (k, v) in saved.items() if k >= 100))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "example.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    grid = np.array([list(line) for line in lines], dtype=str)
    print(f"Part 1: {run(grid, pairs=part1_pairs, to_save=2)}")
    print(f"Part 2: {run(grid, pairs=part2_pairs, to_save=50)}")
