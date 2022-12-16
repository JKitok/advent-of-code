import os
import re

from dataclasses import dataclass

import numpy as np


def parse(lines):
    sensors = np.zeros((len(lines), 2), dtype=int)
    beacons = np.zeros_like(sensors)
    for i, line in enumerate(lines):
        s, b = re.findall("x=(-?\d+), y=(-?\d+)", line)
        sensors[i, :] = list(map(int, s))
        beacons[i, :] = list(map(int, b))
    return sensors, beacons


def part1(sensors, beacons, y=2000000):
    distances = np.sum(np.abs(sensors - beacons), axis=1)
    xmin = np.min(sensors[:, 0])
    xmax = np.max(sensors[:, 0])
    cnt = 0
    for step, x in zip([-1, 1], [xmin, xmin + 1]):
        print(x)
        while True:
            xy = np.tile(np.array([x, y], dtype=int), (len(distances), 1))
            ds = np.sum(np.abs(sensors - xy), axis=1)
            db = np.sum(np.abs(beacons - xy), axis=1)
            if np.any(db == 0):
                pass
            elif np.any(ds <= distances):
                cnt += 1
            elif x < xmin or x > xmax:
                break
            x += step
    return cnt


def part2(sensors, beacons, min_=0, max_=4_000_000):
    distances = np.sum(np.abs(sensors - beacons), axis=1)
    for x in range(min_, max_ + 1):
        y = 0
        if x % 10_000 == 0:
            print(x)
        while True:
            xy = np.tile(np.array([x, y], dtype=int), (len(distances), 1))
            ds = np.sum(np.abs(sensors - xy), axis=1)
            idx = np.nonzero(ds <= distances)[0]
            if len(idx) == 0:
                return x * 4000000 + y
            dx = np.abs(sensors[idx[0], 0] - x)
            d = distances[idx[0]]
            y = sensors[idx[0], 1] + (d - dx) + 1
            if y > max_:
                break


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    sensors, beacons = parse(lines)

    # print(f"Part 1: {part1(sensors, beacons)}")
    print(f"Part 2: {part2(sensors, beacons)}")
