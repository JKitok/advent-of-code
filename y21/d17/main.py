import os
import re
from enum import Enum


class Result(Enum):
    INSIDE = 0
    MISSED = 1


def shoot(u, v, x1, x2, y1, y2):
    x, y = 0, 0
    y_max = 0
    while True:
        x += u
        y += v
        if u != 0:
            u += -1 if u > 0 else 1
        v -= 1

        if y > y_max:
            y_max = y
        if x1 <= x <= x2 and y1 <= y <= y2:
            return Result.INSIDE, y_max

        if x > x2 or u == 0 and y < y2:
            return Result.MISSED, y_max


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]

    params = re.match(
        r"^target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)$", lines[0]
    ).groups()
    x1, x2, y1, y2 = map(int, params)

    v_min = y1 - 5
    v_max = 300
    y_max = 0
    initial_velocities = []
    for u in range(1, x2 + 1):
        for v in range(v_min, v_max):
            res, y = shoot(u, v, x1, x2, y1, y2)
            if res == Result.INSIDE:
                if y > y_max:
                    y_max = y
                initial_velocities.append((u, v))

    print(f"Part 1: {y_max}")
    print(f"Part 2: {len(initial_velocities)}")
