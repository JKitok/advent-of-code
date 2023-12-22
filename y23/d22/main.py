import os
from collections import defaultdict
from tqdm import tqdm
from functools import cache

import numpy as np


def calculate_coords(line):
    edge_a, edge_b = line.split("~")
    a = np.array(tuple(map(int, edge_a.split(","))))
    b = np.array(tuple(map(int, edge_b.split(","))))
    diff = b - a
    coords = list()
    for idx in [0, 1, 2]:
        for mp in range(diff[idx]):
            zeros = np.zeros_like(a)
            zeros[idx] = 1
            coords.append(a + mp * zeros)
    coords.append(b)
    return coords


class Cube:
    idx = 0

    def __init__(self, line):
        self.id = Cube.idx
        Cube.idx += 1
        self.settled = False
        self.coords = calculate_coords(line)


def run(cubes):
    supports = defaultdict(lambda: [])
    supported_by = defaultdict(lambda: [])

    floor = {}
    floor_id = {}
    for cube in tqdm(cubes):
        while not cube.settled:
            moved_coords = [c + [0, 0, -1] for c in cube.coords]
            intersects = [floor.get((c[0], c[1]), 0) >= c[2] for c in moved_coords]
            if any(intersects):
                cube.settled = True
            else:
                cube.coords = moved_coords

        for idx, coord in enumerate(cube.coords):
            if intersects[idx]:
                support = floor_id.get((coord[0], coord[1]))
                if support is not None:
                    if support not in supported_by[cube.id]:
                        supported_by[cube.id].append(support)
                        supports[support].append(cube.id)

        for coord in cube.coords:
            floor[(coord[0], coord[1])] = coord[2]
            floor_id[(coord[0], coord[1])] = cube.id

    N = 0
    for cube in cubes:
        can_remove = not any(len(supported_by[i]) <= 1 for i in supports[cube.id])
        N += 1 if can_remove else 0
    return N, supports, supported_by


def part2(cubes, supports, supported_by):
    @cache
    def get_all_falls(idx, falling=None):
        falling = set(falling) if falling is not None else set()
        sup_by_this = set(supports[idx])
        if len(sup_by_this) == 0:
            return falling
        else:
            falling.add(idx)
            to_check = set()
            for i in sup_by_this:
                supports_standing = set(v for v in supported_by[i] if v not in falling)
                if len(supports_standing) == 0:
                    falling.add(i)
                    to_check.add(i)
            for i in to_check:
                falling.update(get_all_falls(i, frozenset(falling)))
            return falling

    num_fall = []
    for c in tqdm(cubes):
        num_fall.append(get_all_falls(c.id))

    N = 0
    for i in num_fall:
        if len(i) > 0:
            N += len(i) - 1
    return N


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    cubes = [Cube(line) for line in lines]
    cubes = sorted(cubes, key=lambda x: min(v[2] for v in x.coords))
    N, supports, supported_by = run(cubes)

    print(f"Part 1: {N}")
    print(f"Part 2: {part2(cubes, supports, supported_by)}")
