import os
import re

from dataclasses import dataclass

import numpy as np


@dataclass
class Bag:
    name: str
    contents: dict

    @classmethod
    def from_line(cls, line):
        a, b = line.split("contain", 2)
        bag_name = re.match(r"([a-z ]+) bags", a).groups()[0]
        contents = {}
        if not "no other bags" in b:
            lines = b.split(",")
            for line in lines:
                num, name = re.match(r"^\s?(\d+) (.+) bags?.?$", line).groups()
                contents[name] = int(num)
        return cls(bag_name, contents)


def test_from_line():
    assert Bag.from_line("dotted black bags contain no other bags.") == Bag(
        "dotted black",
        {},
    )
    assert Bag.from_line(
        "light red bags contain 1 bright white bag, 2 muted yellow bags."
    ) == Bag("light red", {"bright white": 1, "muted yellow": 2})


def part1(lines):
    bags = [Bag.from_line(line) for line in lines]
    bags = sorted(bags, key=lambda x: len(x.contents))
    expected = "shiny gold"
    bags = [bag for bag in bags if bag.name != expected]
    contains = []
    not_contains = []

    while len(bags):
        for bag in bags:
            if expected in bag.contents.keys():
                contains.append(bag.name)
            elif any((key in contains for key in bag.contents.keys())):
                contains.append(bag.name)
            elif not bag.contents:
                not_contains.append(bag.name)
            else:
                # Go through content and remove instances that do not contain the expected bag
                bag.contents = {
                    k: v for k, v in bag.contents.items() if k not in not_contains
                }
        bags = [
            bag
            for bag in bags
            if (bag.name not in not_contains and bag.name not in contains)
        ]
    return len(contains)


def part2(lines):
    bags = [Bag.from_line(line) for line in lines]
    bags = sorted(bags, key=lambda x: len(x.contents))
    known_quantity = {}

    while bags:

        for bag in bags:
            if not any(key not in known_quantity.keys() for key in bag.contents.keys()):
                known_quantity[bag.name] = 1 + sum(
                    (
                        value * known_quantity[key]
                        for (key, value) in bag.contents.items()
                    )
                )

        bags = [bag for bag in bags if bag.name not in known_quantity.keys()]

    return known_quantity["shiny gold"] - 1


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
