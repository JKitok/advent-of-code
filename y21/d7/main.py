import os
import re

from dataclasses import dataclass

import numpy as np


def part1(positions):
    position, cost = -1, 1e9
    for i in range(min(positions), max(positions)):
        new_cost = np.sum(np.abs(positions - i))
        if new_cost < cost:
            position = i
            cost = new_cost

    print(position, cost)


def part2(positions):
    max_ = np.max(positions)
    fuel_costs = np.array(range(max_)).astype(np.int64)

    def cost_func(i):
        return np.sum(fuel_costs[: i + 1])

    position, cost = -1, 1e9
    for i in range(min(positions), max(positions)):
        movement = np.abs(positions - i)
        costs = [cost_func(val) for val in movement]
        new_cost = sum(costs)
        if new_cost < cost:
            position = i
            cost = new_cost
    print(position, cost)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    positions = np.fromstring(lines[0], sep=",").astype(np.int64)

    part1(positions)
    part2(positions)
