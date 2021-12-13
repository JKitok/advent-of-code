import os
import re

import numpy as np


def fold_y(matrix, value):
    matrix1 = matrix[:value, :]
    matrix2 = np.flipud(matrix[value + 1 :, :])
    assert matrix1.shape == matrix2.shape
    return matrix1 + matrix2


def fold_x(matrix, value):
    matrix1 = matrix[:, :value]
    matrix2 = np.fliplr(matrix[:, value + 1 :])
    assert matrix1.shape == matrix2.shape
    return matrix1 + matrix2


def perform_fold(matrix, instruction):
    axis, val = re.match(r"^fold along ([xy])=(\d+)$", instruction).groups()
    if axis == "y":
        matrix = fold_y(matrix, int(val))
    elif axis == "x":
        matrix = fold_x(matrix, int(val))
    else:
        raise ValueError()
    return matrix


def part1(matrix, instructions):
    i = instructions[0]
    matrix = perform_fold(matrix, i)
    return np.sum(np.sum(matrix > 0))


def part2(matrix, instructions):
    for i in instructions:
        matrix = perform_fold(matrix, i)

    with open("output.txt", "w") as f:
        for line in matrix:
            for v in line:
                f.write("XX" if int(v) else "  ")
            f.write("\n")


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    split = lines.index("")
    coordinate_text = lines[:split]
    instructions = lines[split + 1 :]
    values = [tuple(map(int, l.split(","))) for l in coordinate_text]
    max_x = max(v[1] for v in values)
    max_y = max(v[0] for v in values)

    matrix = np.zeros((max_x + 1, max_y + 1))
    for y, x in values:
        matrix[x, y] = 1

    print(f"Part 1: {part1(matrix, instructions)}")
    print(f"Part 2: {part2(matrix, instructions)}")
