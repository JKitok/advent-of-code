import os
import re

from dataclasses import dataclass

import numpy as np


def parse_id(line):
    bin_ = line.replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0")
    return int(bin_, 2)


def test_parse_id():
    assert parse_id("BFFFBBFRRR") == 567


def part1(lines):
    return max((parse_id(v) for v in lines))


def part2(lines):
    ids = sorted([parse_id(v) for v in lines])
    idx = np.where(np.diff(ids) > 1)[0][0]
    return ids[idx] + 1


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
