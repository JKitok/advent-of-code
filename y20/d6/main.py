import os
import re

from dataclasses import dataclass

import numpy as np


def parse_to_groups(lines):
    # Parse group of lines (that are separated by newline) into groups
    lines = [line.strip() for line in lines]
    groups = []
    while len(lines):
        try:
            next_ = lines.index("")
        except ValueError:
            next_ = len(lines)
        groups.append(lines[:next_])
        lines = lines[next_ + 1 :]
    return groups


def part1(lines):
    groups = parse_to_groups(lines)
    counts = []
    for group in groups:
        counts.append(len(set("".join(group))))
    return sum(counts)


def part2(lines):
    groups = parse_to_groups(lines)
    counts = []
    for group in groups:
        answers = group[0]
        for line in group[1:]:
            answers = [a for a in answers if a in line]
        counts.append(len(answers))
    return sum(counts)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
