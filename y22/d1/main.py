import os
import re

from dataclasses import dataclass

import numpy as np


def get_calories_count(entries):
    calories = []
    sum_ = 0
    for line in entries:
        if line:
            sum_ += int(line)
        else:
            calories.append(sum_)
            sum_ = 0
    calories.append(sum_)
    return calories


def part1(calories):
    return max(calories)


def part2(calories):
    return sum(sorted(calories, reverse=True)[:3])


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    calories = get_calories_count(lines)

    print(f"Part 1: {part1(calories)}")
    print(f"Part 2: {part2(calories)}")
