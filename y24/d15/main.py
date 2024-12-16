import os
import numpy as np
import io


def print_grid(grid):
    # Use StringIO to capture the output of savetxt
    with io.StringIO() as output:
        np.savetxt(output, grid, delimiter="", fmt="%s")
        result = output.getvalue()  # Get the string value
    # Print the result
    print(result)


def get_next_available(grid, i1, i2, d1, d2):
    new_i1, new_i2 = i1 + d1, i2 + d2
    while True:
        if grid[new_i1, new_i2] == "#":
            return None
        elif grid[new_i1, new_i2] == ".":
            return new_i1, new_i2
        else:
            new_i1 += d1
            new_i2 += d2


def part1(grid, movement):
    index = np.where(grid == "@")
    i1 = index[0][0]
    i2 = index[1][0]
    i = 0
    for m in movement:
        d1, d2 = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}[m]
        if grid[i1 + d1, i2 + d2] == ".":
            grid[i1, i2] = "."
            grid[i1 + d1, i2 + d2] = "@"
            i1, i2 = i1 + d1, i2 + d2
        else:
            pos = get_next_available(grid, i1, i2, d1, d2)
            if pos is not None:
                grid[i1, i2] = "."
                grid[i1 + d1, i2 + d2] = "@"
                grid[pos[0], pos[1]] = "O"
                i1, i2 = i1 + d1, i2 + d2
    sum_ = 0
    for i1, i2 in zip(*np.where(grid == "O")):
        sum_ += 100 * i1 + i2
    return sum_


def part2(grid, movement):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    grid_txt = lines[: lines.index("")]
    grid = np.array([list(line) for line in grid_txt], dtype=str)
    movement_txt = lines[lines.index("") + 1 :]
    movement = "".join(movement_txt)
    print(f"Part 1: {part1(grid, movement)}")
    print(f"Part 2: {part2(grid, movement)}")
