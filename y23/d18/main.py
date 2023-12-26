import os
import re

STEPS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
NUM_TO_STEP = {"0": "R", "1": "D", "2": "L", "3": "U"}


def get_area(points):
    # Using the shoelace formula, trapezoid formula assuming points[0]==points[-1]
    A = 0
    for (x1, y1), (x2, y2) in zip(points[:-1], points[1:]):
        A += (y1 + y2) * (x1 - x2)
    return 0.5 * A


def calculate_num_boundary_cubes(points):
    N = 0
    for (x1, y1), (x2, y2) in zip(points[:-1], points[1:]):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        N += dx + dy
    return N


def calculate_volume(points):
    A = get_area(points)
    if A < 0:
        A = -A
        points = [*reversed(points)]
    n_ext_points = calculate_num_boundary_cubes(points)
    # Picks theorem gives internal points
    n_interior_points = A + 1 - n_ext_points / 2
    return int(round(n_interior_points + n_ext_points))


def part1(lines):
    x, y = 0, 0
    points = [(x, y)]
    for d, t, _ in lines:
        dx, dy = STEPS[d]
        x += int(t) * dx
        y += int(t) * dy
        points.append((x, y))
    return calculate_volume(points)


def part2(lines):
    x, y = 0, 0
    points = [(x, y)]
    for *_, hex_ in lines:
        dx, dy = STEPS[NUM_TO_STEP[hex_[5]]]
        t = int(hex_[0:5], 16)
        x += t * dx
        y += t * dy
        points.append((x, y))
    return calculate_volume(points)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    data = [re.match(r"([A-Z]) (\d+) \(\#(.*)\)", l).groups() for l in lines]

    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
