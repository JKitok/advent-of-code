import os
import re

from dataclasses import dataclass

import numpy as np


class Dir:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.dirs = {}
        self.files = {}

    def full_path(self):
        if self.parent is None:
            return self.name
        else:
            return self.parent.full_path() + self.name + "/"

    def size(self):
        return sum(d.size() for d in self.dirs.values()) + sum(self.files.values())


def part1(parent_dir):
    sum_ = 0
    for dir in parent_dir.dirs.values():
        size = dir.size()
        if size <= 100_000:
            sum_ += size
        sum_ += part1(dir)
    return sum_


def get_dir_sizes(dir, sizes):
    for d in dir.dirs.values():
        sizes[d.full_path()] = d.size()
        sizes = get_dir_sizes(d, sizes)
    return sizes


def part2(root_dir):
    needed = 30_000_000
    available = 70_000_000 - root_dir.size()
    sizes = get_dir_sizes(root_dir, {})
    sizes = dict(sorted(sizes.items(), key=lambda item: item[1]))
    for size in sizes.values():
        if size > needed - available:
            return size


def traverse(lines):
    root_dir = Dir("/")
    current_dir = None
    line = next(lines)

    while line is not None:
        if line == "$ cd /":
            current_dir = root_dir
            line = next(lines, None)
        elif line == "$ cd ..":
            current_dir = current_dir.parent
            line = next(lines, None)
        elif line.startswith("$ cd "):
            current_dir = current_dir.dirs[line[5:]]
            line = next(lines, None)
        elif line == "$ ls":
            while (line := next(lines, None)) is not None and not line.startswith("$"):
                if line.startswith("dir"):
                    name = line[4:]
                    current_dir.dirs[name] = Dir(name, parent=current_dir)
                else:
                    size, name = line.split(" ")
                    current_dir.files[name] = int(size)
    return root_dir


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    root_dir = traverse(iter(lines))

    # print(f"Part 1: {part1(root_dir)}")
    print(f"Part 2: {part2(root_dir)}")
