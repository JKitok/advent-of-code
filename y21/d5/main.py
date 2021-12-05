import os
import re

from dataclasses import dataclass

import numpy as np


@dataclass
class Entry:
    x1: int
    y1: int
    x2: int
    y2: int

    @classmethod
    def from_line(cls, text):
        match = re.match(r"(\d+),(\d+)\s->\s(\d+),(\d+)", text)
        x1, y1, x2, y2 = (int(v) for v in match.groups())
        if y2 < y1:
            x1, y1, x2, y2 = x2, y2, x1, y1
        if x2 < x1:
            x1, y1, x2, y2 = x2, y2, x1, y1
        return cls(x1, y1, x2, y2)


def test_entry_create():
    assert Entry.from_line("0,9 -> 5,9") == Entry(0, 9, 5, 9)


def create_map(entries):
    max_x = max((e.x2 for e in entries))
    max_y = max((e.y2 for e in entries))
    map_ = np.zeros((max_x + 1, max_y + 1))
    for entry in entries:
        # Straight case
        if entry.x1 == entry.x2 or entry.y1 == entry.y2:
            map_[entry.x1 : entry.x2 + 1, entry.y1 : entry.y2 + 1] += 1
        # Diagonal case
        else:
            yfactor = 1 if entry.y2 >= entry.y1 else -1
            for i in range(0, entry.x2 - entry.x1 + 1):
                map_[entry.x1 + i, entry.y1 + yfactor * i] += 1
    return map_


def part1(entries):
    entries = [e for e in entries if (e.x1 == e.x2 or e.y1 == e.y2)]
    map_ = create_map(entries)
    print(np.sum(map_ > 1))


def part2(entries):
    map_ = create_map(entries)
    print(np.sum(map_ > 1))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    entries = [Entry.from_line(line) for line in lines]
    part1(entries)
    part2(entries)
