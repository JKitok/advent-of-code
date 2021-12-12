import os
import re
import copy

from dataclasses import dataclass

import numpy as np


def run_step(matrix):
    matrix += 1
    rows, cols = np.where(matrix > 9)
    indices = [(r, c) for r, c in zip(rows, cols)]
    to_handle = copy.deepcopy(indices)
    while len(to_handle):
        row, col = to_handle.pop(0)
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x != 0 or y != 0:
                    nx = row + x
                    ny = col + y
                    if 0 <= nx < matrix.shape[0] and 0 <= ny < matrix.shape[1]:
                        matrix[nx, ny] += 1
                        if matrix[nx, ny] > 9 and (nx, ny) not in indices:
                            indices.append((nx, ny))
                            to_handle.append((nx, ny))
    matrix[matrix > 9] = 0
    return matrix, len(indices)

def part1(matrix):
    num_flashes = 0
    for i in range(100):
        matrix, n = run_step(matrix)
        num_flashes += n

    return num_flashes


def part2(matrix):
    step = 0
    while np.sum(np.sum(matrix)) > 0:
        matrix, _ = run_step(matrix)
        step += 1

    return step


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    comma_separated = [",".join(line) for line in lines]
    matrix = np.fromstring(",".join(comma_separated), sep=",").reshape(
        len(lines), len(lines[0])
    )

    print(f"Part 1: {part1(matrix)}")
    print(f"Part 2: {100 + part2(matrix)}")
