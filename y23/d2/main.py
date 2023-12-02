import os
import math

from collections import namedtuple, defaultdict
from dataclasses import dataclass

import numpy as np


def is_possible(sets, bag):
    for set_ in sets:
        for color, num in bag.items():
            if set_.get(color, 0) > num:
                return False
    return True


def part1(games, bag):
    sum_ = 0
    for game_id, sets in games.items():
        if is_possible(sets, bag):
            sum_ += game_id
    return sum_


def part2(games):
    sum_ = 0
    for game_id, sets in games.items():
        bag = {"red": 0, "blue": 0, "green": 0}
        for set in sets:
            for c in ["red", "blue", "green"]:
                bag[c] = max(bag[c], set.get(c, 0))
        power = math.prod(bag.values())
        sum_ += power
    return sum_


Game = namedtuple("Game", ["id", "sets"])


def parse(lines):
    games = {}
    for line in lines:
        id_line, sets_line = map(str.strip, line.split(":"))
        _, game_id = id_line.split(" ")
        game_id = int(game_id)
        sets = []
        for set_ in sets_line.split(";"):
            cubes = {}
            for c in map(str.strip, set_.split(",")):
                n, color = map(str.strip, c.split(" "))
                cubes[color] = int(n)
            sets.append(cubes)
        games[game_id] = sets

    return games


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    games = parse(lines)

    bag = {"red": 12, "green": 13, "blue": 14}

    print(f"Part 1: {part1(games, bag)}")
    print(f"Part 2: {part2(games)}")
