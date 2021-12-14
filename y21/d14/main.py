import os
import re
import collections
from dataclasses import dataclass

import numpy as np


def run_step(template, rules):
    new = []
    for first, second in zip(template[:-1], template[1:]):
        new.append(first)
        c = rules[first + second]
        if c is not None:
            new.append(c)
    new.append(template[-1])
    return "".join(new)


def part1(template, rules):
    for i in range(10):
        template = run_step(template, rules)

    c = collections.Counter(template)
    counts = c.most_common()
    return counts[0][1] - counts[-1][1]


def run_step_2(pairs, char_count, rules):
    new_pairs = collections.defaultdict(int)
    for pair, num_count in pairs.items():
        new_char = rules[pair]
        new_pairs[pair[0] + new_char] += num_count
        new_pairs[new_char + pair[1]] += num_count
        char_count[new_char] += num_count
    return new_pairs, char_count


def part2(template, rules):
    pairs = collections.defaultdict(int)
    for first, second in zip(template[:-1], template[1:]):
        pairs[first + second] += 1
    char_count = collections.Counter(template)

    for i in range(40):
        pairs, char_count = run_step_2(pairs, char_count, rules)

    counts = char_count.most_common()
    return counts[0][1] - counts[-1][1]


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]

    template = lines[0]
    rules = lines[2:]
    rules = dict([re.match("^([A-Z]{2}) -> ([A-Z])$", line).groups() for line in rules])
    print(f"Part 1: {part1(template, rules)}")
    print(f"Part 2: {part2(template, rules)}")
