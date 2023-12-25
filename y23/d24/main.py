import os
import itertools

from dataclasses import dataclass

import numpy as np


def find_intersection_point_3d(line1, line2, ignore_z=True):
    """
    Find the intersection point of two lines in 3D space defined by a point and a direction vector.

    Parameters:
    - line1: A tuple (x1, y1, z1, vx1, vy1, vz1) representing a line: x = x1 + t*vx1, y = y1 + t*vy1, z = z1 + t*vz1
    - line2: A tuple (x2, y2, z2, vx2, vy2, vz2) representing another line: x = x2 + t*vx2, y = y2 + t*vy2, z = z2 + t*vz2

    Returns:
    - If lines intersect: A tuple (x, y, z) representing the intersection point
    - If lines are parallel (no intersection): None
    """
    x1, y1, z1, vx1, vy1, vz1 = line1
    x2, y2, z2, vx2, vy2, vz2 = line2
    if ignore_z:
        z1 = 0
        z2 = 0
        vz1 = 0
        vz2 = 0

    # Check if lines are parallel (direction vectors are proportional)
    cross_product = (
        vy1 * vz2 - vz1 * vy2,
        vz1 * vx2 - vx1 * vz2,
        vx1 * vy2 - vy1 * vx2,
    )

    # Allow for a small tolerance to handle floating-point imprecision
    tolerance = 1e-10
    if all(-tolerance < coord < tolerance for coord in cross_product):
        # "Lines are parallel, no intersection.
        return None

    # Find the index of the non-zero component in the cross product
    non_zero_index = next(
        i for i, coord in enumerate(cross_product) if abs(coord) > tolerance
    )

    # Solve for parameters t1 and t2 based on the non-zero component
    if non_zero_index == 0:
        t1 = ((y2 - y1) * vz2 - (z2 - z1) * vy2) / cross_product[0]
    elif non_zero_index == 1:
        t1 = ((z2 - z1) * vx2 - (x2 - x1) * vz2) / cross_product[1]
    else:
        t1 = ((x2 - x1) * vy2 - (y2 - y1) * vx2) / cross_product[2]

    # Calculate intersection point
    x = x1 + t1 * vx1
    y = y1 + t1 * vy1
    z = z1 + t1 * vz1

    return x, y, z


def part1(paths, min_=200000000000000, max_=400000000000000):
    N = 0
    for p1, p2 in itertools.combinations(paths, 2):
        res = find_intersection_point_3d(p1, p2, ignore_z=True)
        if res:
            t1 = (res[0] - p1[0]) / p1[3]
            t2 = (res[0] - p2[0]) / p2[3]
            if t1 >= 0 and t2 >= 0:
                x, y, z = res
                if min_ <= x <= max_ and min_ <= y <= max_:
                    N += 1
    return N


def part2(lines):
    pass


def parse(lines):
    paths = []
    for line in lines:
        pos, vel = map(str.strip, line.split("@"))
        paths.append((*map(int, pos.split(",")), *map(int, vel.split(","))))
    return paths


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    paths = parse(lines)

    print(f"Part 1: {part1(paths)}")
    print(f"Part 2: {part2(lines)}")
