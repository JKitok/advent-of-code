import os
import re

from enum import Enum
from dataclasses import dataclass

import numpy as np


class Sel(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


def from_char(c):
    return {
        "A": Sel.Rock,
        "B": Sel.Paper,
        "C": Sel.Scissors,
        "X": Sel.Rock,
        "Y": Sel.Paper,
        "Z": Sel.Scissors,
    }[c]


wins_against = {
    Sel.Paper: Sel.Rock,
    Sel.Rock: Sel.Scissors,
    Sel.Scissors: Sel.Paper,
}
loses_against = dict((k, v) for (v, k) in wins_against.items())


def outcome(opponents, your):
    if opponents == your:
        return 3
    elif wins_against[opponents] == your:
        return 0
    else:
        return 6


def part1(entries):
    sum_ = 0
    for a, b in lines:
        opponents = from_char(a)
        your = from_char(b)
        sum_ += your.value + outcome(opponents, your)
    return sum_


def part2(entries):
    sum_ = 0
    for a, b in lines:
        opponents = from_char(a)
        if b == "Y":
            your = opponents
        elif b == "X":
            your = wins_against[opponents]
        else:
            your = loses_against[opponents]
        sum_ += your.value + outcome(opponents, your)
    return sum_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip().split(" ") for v in lines]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
