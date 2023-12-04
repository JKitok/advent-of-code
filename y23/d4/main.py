import os

from collections import defaultdict

import numpy as np


def part1(cards):
    sum_ = 0
    for winning, have in cards.values():
        N = np.intersect1d(winning, have).size
        if N > 0:
            sum_ += 2 ** (N - 1)
    return sum_


def part2(cards):
    num_cards = defaultdict(lambda: 1)
    for i, (winning, have) in cards.items():
        N = np.intersect1d(winning, have).size
        for j in range(i + 1, i + 1 + N):
            num_cards[j] += num_cards[i]

    return sum(num_cards.values())


def parse(lines):
    cards = {}
    for i, line in enumerate(lines):
        _, list_ = map(str.strip, line.split(":"))
        winning, have = map(str.strip, list_.split("|"))
        winning = np.fromstring(winning, sep=" ")
        have = np.fromstring(have, sep=" ")
        cards[i + 1] = [winning, have]
    return cards


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    cards = parse(lines)

    print(f"Part 1: {part1(cards)}")
    print(f"Part 2: {part2(cards)}")
