import os
import re

from dataclasses import dataclass

import numpy as np

to_closed = {"(": ")", "[": "]", "{": "}", "<": ">"}
to_open = {v: k for k, v in to_closed.items()}


class IncorrectCharacter(ValueError):
    def __init__(self, c, expected):
        super().__init__(f"expected {expected} but found {c}")
        self.character = c
        self.expected = expected


def check_line(line):
    open_chars = []
    for c in line:
        if c in to_open.values():
            open_chars.append(c)
        else:
            if open_chars[-1] == to_open[c]:
                open_chars.pop(-1)
            else:
                raise IncorrectCharacter(c, to_closed[open_chars[-1]])

    return [to_closed[v] for v in reversed(open_chars)]


def part1(lines):
    sum_ = 0
    for line in lines:
        try:
            check_line(line)
        except IncorrectCharacter as e:
            sum_ += {")": 3, "]": 57, "}": 1197, ">": 25137}[e.character]

    return sum_


def part2(lines):
    scores = []
    for line in lines:
        try:
            remaining_chars = check_line(line)
            score = 0
            for c in remaining_chars:
                score = 5 * score + {")": 1, "]": 2, "}": 3, ">": 4}[c]
            scores.append(score)
        except IncorrectCharacter as e:
            pass
    return np.median(scores)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
