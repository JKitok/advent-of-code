import os
import math

from collections import defaultdict
from functools import cmp_to_key


def part1(rules, update_list):
    sum_ = 0
    for numbers in update_list:
        if check_ok(rules, numbers):
            idx = math.floor(len(numbers) / 2)
            sum_ += numbers[idx]
    return sum_


def part2(rules, update_list):
    sum_ = 0
    for numbers in update_list:
        if not check_ok(rules, numbers):
            numbers = sorted(
                numbers,
                key=cmp_to_key(
                    lambda v1, v2: -1 if check_order_correct(rules, v1, v2) else 1
                ),
            )
            idx = math.floor(len(numbers) / 2)
            sum_ += numbers[idx]
    return sum_


def check_ok(rules, numbers):
    for i, n in enumerate(numbers[:-1]):
        for after in numbers[i + 1 :]:
            if not check_order_correct(rules, n, after):
                return False
    return True


def check_order_correct(rules, n1, n2):
    one_before_two = n2 in rules[n1]
    two_before_one = n1 in rules[n2]
    return one_before_two and not two_before_one


def parse(lines):
    lines = [v.rstrip("\n") for v in lines]
    idx = lines.index("")
    rules_list = lines[:idx]
    updates_list = lines[idx + 1 :]

    rules = defaultdict(list)
    for txt in rules_list:
        before, after = map(int, txt.split("|"))
        rules[before].append(after)

    updates = []
    for txt in updates_list:
        updates.append([*map(int, txt.split(","))])
    return rules, updates


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    rules, updates = parse(lines)
    print(f"Part 1: {part1(rules, updates)}")
    print(f"Part 2: {part2(rules, updates)}")
