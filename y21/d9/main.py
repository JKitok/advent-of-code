import os
import re

from dataclasses import dataclass

import numpy as np


def part1(matrix):
    sum_ = 0
    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            down = matrix[row - 1, col] if row > 0 else 10
            up = matrix[row + 1, col] if row < matrix.shape[0] - 1 else 10
            left = matrix[row, col - 1] if col > 0 else 10
            right = matrix[row, col + 1] if col < matrix.shape[1] - 1 else 10

            if all([matrix[row, col] - val < 0 for val in [left, right, up, down]]):
                sum_ += 1 + matrix[row, col]
    return sum_


@dataclass
class Point:
    x: int
    y: int

    def is_neighbor(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y) <= 1

    def __repr__(self):
        return f"P({self.x},{self.y})"


def part2(lines):
    matrix[matrix < 9] = 0
    basins = []

    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            p = Point(row, col)
            if matrix[row, col] == 9:
                continue
            for basin in basins:
                if any(p.is_neighbor(p2) for p2 in basin):
                    basin.append(p)
                    break
            else:
                basins.append([p])

    known_basins = []
    while len(basins):
        current = basins.pop()
        found = False
        for p in current:
            if not found:
                for basin in basins:
                    if any(p.is_neighbor(p2) for p2 in basin):
                        basin.extend(current)
                        found = True
                        break
        if not found:
            known_basins.append(current)

    for i, basin in enumerate(known_basins):
        for p in basin:
            matrix[p.x, p.y] = i

    sizes = sorted([len(b) for b in known_basins], reverse=True)
    return np.prod(sizes[:3])

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
