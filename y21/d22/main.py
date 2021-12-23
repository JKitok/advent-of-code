import os
import re
from collections import namedtuple

import numpy as np

REGEX = r"(\d) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"


def part1(sequences):
    N = 50
    cubes = np.zeros((2 * N + 1, 2 * N + 1, 2 * N + 1), dtype=bool)
    for status, x1, x2, y1, y2, z1, z2 in sequences:
        if all((-50 <= v <= 50 for v in map(abs, (x1, x2, y1, y2, z1, z2)))):
            cubes[
                N + x1 : N + x2 + 1, N + y1 : N + y2 + 1, N + z1 : N + z2 + 1
            ] = status
    return np.sum(cubes)


Cube = namedtuple("Cube", ["status", "x1", "x2", "y1", "y2", "z1", "z2", "level"])


def part2(sequences):
    cubes = []
    for seq in sequences:
        new_cubes = [Cube(*seq, 1)]
        for cube in cubes:
            x1 = max(seq[1], cube.x1)
            x2 = min(seq[2], cube.x2)
            y1 = max(seq[3], cube.y1)
            y2 = min(seq[4], cube.y2)
            z1 = max(seq[5], cube.z1)
            z2 = min(seq[6], cube.z2)
            if x2 >= x1 and y2 >= y1 and z2 >= z1:
                new_cubes.append(Cube(seq[0], x1, x2, y1, y2, z1, z2, cube.level + 1))
        cubes.extend(new_cubes)
    num = 0
    for cube in cubes:
        V = (cube.x2 - cube.x1 + 1) * (cube.x2 - cube.x1 + 1) * (cube.z2 - cube.x1 + 1)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "example.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip().replace("on", "1").replace("off", "0") for v in lines]
    sequences = [map(int, re.match(REGEX, v).groups()) for v in lines]
    sequences = [list(v) for v in sequences]

    print(f"Part 1: {part1(sequences)}")
    print(f"Part 2: {part2(sequences)}")
