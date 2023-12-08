import os
from enum import IntEnum
from collections import Counter

REPLACEMENTS = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}


class Strength(IntEnum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    TRIPS = 3
    FULL_HOUSE = 4
    QUADS = 5
    FIVE_KIND = 6


def get_elements_strength(elements):
    if elements[0][1] == 1:
        return Strength.HIGH_CARD
    elif elements[0][1] == 2:
        if elements[1][1] == 2:
            return Strength.TWO_PAIR
        else:
            return Strength.PAIR
    elif elements[0][1] == 3:
        if elements[1][1] == 2:
            return Strength.FULL_HOUSE
        else:
            return Strength.TRIPS
    elif elements[0][1] == 4:
        return Strength.QUADS
    elif elements[0][1] == 5:
        return Strength.FIVE_KIND
    else:
        raise ValueError(elements)


def get_hand_strength(hand):
    c = Counter(hand)
    elements = c.most_common()
    return get_elements_strength(elements)


def get_hand_strength_joker_rule(hand):
    c = Counter(hand)
    elements = c.most_common()
    num_jokers = c.get("J", 0)
    elements = [e for e in elements if e[0] != "J"]
    if not elements:
        return Strength.FIVE_KIND
    else:
        elements[0] = (elements[0][0], elements[0][1] + num_jokers)
        return get_elements_strength(elements)


class Hand:
    def __init__(self, line, joker_rule):
        self.hand, self.bid = line.split(" ")
        self.bid = int(self.bid)
        if joker_rule:
            self.strength = get_hand_strength_joker_rule(self.hand)
            self.hand = self.hand.replace("J", "1")
        else:
            self.strength = get_hand_strength(self.hand)
        self.hand = tuple(map(int, (REPLACEMENTS.get(v, v) for v in self.hand)))

    def __lt__(self, other):
        return (self.strength, *self.hand) < (other.strength, *other.hand)

    def __repr__(self) -> str:
        return f"Hand({self.hand}, {self.bid})"


def run(lines, joker_rule=False):
    hands = [Hand(l, joker_rule=joker_rule) for l in lines]
    hands.sort()
    sum_ = 0
    for i, hand in enumerate(hands):
        sum_ += hand.bid * (i + 1)
    return sum_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    lines = [v for v in lines if v]

    print(f"Part 1: {run(lines, joker_rule=False)}")
    print(f"Part 2: {run(lines, joker_rule=True)}")
