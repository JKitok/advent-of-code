import os
import re

from dataclasses import dataclass

import numpy as np

STEPS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def djikstra(matrix):
    visited = np.zeros_like(matrix, dtype=bool)
    risk = np.zeros_like(matrix, dtype=np.int64) + 1e9

    x, y = 0, 0
    risk[x, y] = 0

    while True:
        visited[x, y] = 1

        for i, j in STEPS:
            if 0 <= x + i < matrix.shape[0] and 0 <= y + j < matrix.shape[1]:
                if not visited[x + i, y + j]:
                    new_value = matrix[x + i, y + j] + risk[x, y]
                    if risk[x + i, y + j] > new_value:
                        risk[x + i, y + j] = new_value

        if visited[-1, -1]:
            break
        indices = np.nonzero(~visited)
        n = np.argmin(risk[indices])
        x = indices[0][n]
        y = indices[1][n]
    return risk[-1, -1]


def part1(matrix):
    return djikstra(matrix)


def part2(matrix):
    new_matrix = np.zeros((matrix.shape[0] * 5, matrix.shape[1] * 5))
    N, M = matrix.shape
    for i in range(5):
        for j in range(5):
            new_matrix[i * N : (i + 1) * N, j * M : (j + 1) * M] = matrix + (i + j)

    new_matrix[new_matrix > 9] -= 9

    return djikstra(new_matrix)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    comma_separated = [",".join(line) for line in lines]
    matrix = np.fromstring(",".join(comma_separated), sep=",").reshape(
        len(lines), len(lines[0])
    )

    print(f"Part 1: {part1(matrix)}")
    print(f"Part 2: {part2(matrix)}")
