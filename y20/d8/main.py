import os
import re
import copy

from dataclasses import dataclass

import numpy as np


def execute(lines):
    executed_lines = np.zeros((len(lines))).astype(bool)
    accumulator = 0
    index = 0
    while index < len(lines) and not executed_lines[index]:
        assert index >= 0
        executed_lines[index] = True
        instruction, value = lines[index].split(" ", 2)
        if instruction == "nop":
            index += 1
        elif instruction == "acc":
            accumulator += int(value)
            index += 1
        elif instruction == "jmp":
            index += int(value)
        else:
            raise ValueError(instruction)
    return accumulator, index >= len(lines)


def part1(lines):
    accumulator, executed_correctly = execute(lines)
    return accumulator


def part2(lines):
    executed_correctly = False
    accumulator = 0
    for i, val in enumerate(lines):
        if not val.startswith("acc"):
            modified = copy.deepcopy(lines)
            if val.startswith("nop"):
                modified[i] = val.replace("nop", "jmp")
            elif val.startswith("jmp"):
                modified[i] = val.replace("jmp", "nop")
            accumulator, executed_correctly = execute(modified)

        if executed_correctly:
            break
    return accumulator


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
