import os
import re
import math

from itertools import cycle


def part1(instructions, map_):
    instr = cycle(instructions)
    steps = 0
    loc = "AAA"
    while loc != "ZZZ":
        i = next(instr)
        loc = map_[loc][i]
        steps += 1
    return steps


def part2(instructions, map_):
    instr = cycle(instructions)
    steps = 0
    nodes = [n for n in map_.keys() if n.endswith("A")]
    ends = [0] * len(nodes)
    while any((e == 0 for e in ends)):
        i = next(instr)
        nodes = [map_[n][i] for n in nodes]
        steps += 1
        for i, node in enumerate(nodes):
            if ends[i] == 0 and node.endswith("Z"):
                ends[i] = steps
    return math.lcm(*ends)


def parse(map_lines):
    map_ = {}
    for line in map_lines:
        a, b, c = re.match(
            r"([A-Z1-9]+) \= \(([A-Z1-9]+), ([A-Z1-9]+)\)", line
        ).groups()
        map_[a] = {"L": b, "R": c}
    return map_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    instructions, _, *map_lines = lines
    map_ = parse(map_lines)

    print(f"Part 1: {part1(instructions, map_)}")
    print(f"Part 2: {part2(instructions, map_)}")
