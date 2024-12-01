import os
import copy
from dataclasses import dataclass
import numpy as np


def part1(lines):
    pass


def part2(lines):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "example.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    print(f"Part 1: {part1(copy.deepcopy(lines))}")
    print(f"Part 2: {part2(copy.deepcopy(lines))}")
