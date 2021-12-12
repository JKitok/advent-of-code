import os
import re

from dataclasses import dataclass

import numpy as np


def is_valid_part1(path):
    lowercases = set([v for v in path if v.islower()])
    sums = [sum((v == l for v in path)) for l in lowercases]
    return not any((s > 1) for s in sums)


def is_valid_part2(path):
    lowercases = set([v for v in path if v.islower()])
    sums = sorted((sum((v == l for v in path)) for l in lowercases), reverse=True)
    if any((s > 2) for s in sums):
        return False
    elif len(sums) > 1 and sums[1] == 2:
        return False
    elif sum((v == "start" for v in path)) > 1:
        return False
    else:
        return True


def find_all_paths(entries: list, pos: str, current_path: list, is_valid):
    # print("Calling: ", pos, dont_visit)
    all_paths = []
    all_next = [e for e in entries if pos in e]
    all_next = [([e[1], e[0]] if e[1] == pos else e) for e in all_next]

    for path in all_next:
        if path[1] == "end":
            all_paths.append(path)
        else:
            new_path = [*current_path, path[1]]
            if not is_valid(new_path):
                continue
            all_sub = find_all_paths(entries, path[1], new_path, is_valid)
            for sub in all_sub:
                all_paths.append([path[0], *sub])

    return all_paths

def part1(entries):
    all_paths = find_all_paths(entries, "start", ["start"], is_valid_part1)
    return len(all_paths)

def part2(entries):
    all_paths = find_all_paths(entries, "start", ["start"], is_valid_part2)
    return len(all_paths)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    entries = [line.split("-") for line in lines]

    print(f"Part 1: {part1(entries)}")
    print(f"Part 2: {part2(entries)}")
