import os
import re

from dataclasses import dataclass

import numpy as np


def simulate(fishes, days):
    num_count = np.array([np.sum(fishes == val) for val in range(10)]).astype(np.uint64)

    for i in range(days):
        # Spawn new fishes
        num_count[9] = num_count[0]
        # Reset counter for existing fishes
        num_count[7] += num_count[0]
        # Remove counters for day
        num_count[0:-1] = num_count[1:]

    return np.sum(num_count[:-1])


def part1(fishes):
    return simulate(fishes, 80)


def part2(fishes):
    return simulate(fishes, 256)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]

    fishes = np.fromstring(lines[0], sep=",").astype(np.uint64)

    print(f"Part 1: {part1(fishes)}")
    print(f"Part 2: {part2(fishes)}")
