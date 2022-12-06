import os
import re
import copy

from typing import Tuple


def parse_instruction(in_: str) -> Tuple[int]:
    res = re.match("move (\d+) from (\d+) to (\d+)", in_)
    return list(map(int, res.groups()))


def parse_stacks(lines):
    *crates, last_row = lines
    stacks = [[]]
    for i in (i for i in range(1, 10) if str(i) in last_row):
        idx = last_row.index(str(i))
        stack = [line[idx] for line in reversed(crates)]
        stack = [v for v in stack if v != " "]
        stacks.append(stack)
    return stacks


def part1(stacks, instructions):
    for instr in instructions:
        nr, src, dest = instr
        for i in range(nr):
            stacks[dest].append(stacks[src].pop())

    return "".join((stack[-1] for stack in stacks[1:]))


def part2(stacks, instructions):
    for instr in instructions:
        nr, src, dest = instr
        stacks[dest].extend([v for v in stacks[src][-nr:]])
        stacks[src] = [v for v in stacks[src][:-nr]]

    return "".join((stack[-1] for stack in stacks[1:]))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    stacks_input = lines[: lines.index("")]
    instructions = lines[lines.index("") + 1 :]
    instructions = [parse_instruction(v) for v in instructions]
    stacks = parse_stacks(stacks_input)

    print(f"Part 1: {part1(copy.deepcopy(stacks), instructions)}")
    print(f"Part 2: {part2(copy.deepcopy(stacks), instructions)}")
