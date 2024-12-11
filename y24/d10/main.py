import os
import numpy as np


def run(grid, allow_same_end_position):
    def search(grid, used_end_positions, i, j, expected_value):
        if not (0 <= i < grid.shape[0] and 0 <= j < grid.shape[1]):
            return 0
        if not grid[i, j] == expected_value:
            return 0
        if grid[i, j] == 9:
            if used_end_positions is None:
                return 1
            else:
                if used_end_positions[i, j] == 1:
                    return 0
                else:
                    used_end_positions[i, j] = 1
                    return 1
        else:
            return (
                search(grid, used_end_positions, i + 1, j, expected_value + 1)
                + search(grid, used_end_positions, i - 1, j, expected_value + 1)
                + search(grid, used_end_positions, i, j + 1, expected_value + 1)
                + search(grid, used_end_positions, i, j - 1, expected_value + 1)
            )

    def grid_search(grid, start_i, start_j, allow_same_end):
        used_end_positions = np.zeros_like(grid) if not allow_same_end else None
        return search(grid, used_end_positions, start_i, start_j, 0)

    return sum(
        grid_search(grid, i, j, allow_same_end_position)
        for i, j in zip(*np.where(grid == 0))
    )


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    grid = np.array([list(line) for line in lines], dtype=int)
    print(f"Part 1: {run(grid, allow_same_end_position=False)}")
    print(f"Part 2: {run(grid, allow_same_end_position=True)}")
