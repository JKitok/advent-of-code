import os
import copy
import numpy as np


def run(grid):
    start = np.where(grid == "S")
    start_i1 = start[0][0]
    start_i2 = start[1][0]
    end = np.where(grid == "E")
    end_i1 = end[0][0]
    end_i2 = end[1][0]
    costs = np.zeros_like(grid, dtype=int)
    visited = np.zeros_like(grid, dtype=bool)
    directions = np.zeros_like(grid, dtype=np.complex64)
    num_steps = np.zeros_like(grid, dtype=int)
    costs.fill(1e9)
    directions.fill(0 + 1j)
    costs[start_i1, start_i2] = 0
    while not visited[end_i1, end_i2]:
        masked_cost = np.where(visited, 1e9, costs)
        i1, i2 = np.unravel_index(np.argmin(masked_cost), costs.shape)
        cost = costs[i1, i2]
        direction = directions[i1, i2]
        num_step = num_steps[i1, i2]
        coord = i1 + i2 * 1j
        visited[i1, i2] = True
        for m, additional_cost in zip([1, 1j, -1j, -1], [0, 1000, 1000, 2000]):
            new_direction = direction * m
            new_coord = coord + new_direction
            new_i1 = int(np.round(new_coord.real))
            new_i2 = int(np.round(new_coord.imag))
            new_cost = cost + additional_cost + 1
            if grid[new_i1, new_i2] == "#":
                continue
            elif costs[new_i1, new_i2] == new_cost:
                num_steps[new_i1, new_i2] += num_step
            elif costs[new_i1, new_i2] > new_cost:
                costs[new_i1, new_i2] = new_cost
                directions[new_i1, new_i2] = new_direction
                num_steps[new_i1, new_i2] = num_step + 1

    print(f"Part 1: {costs[end_i1, end_i2]}")
    print(f"Part 2: {num_steps[end_i1, end_i2]}")


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "example.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    grid = np.array([list(line) for line in lines], dtype=str)
    run(grid)
