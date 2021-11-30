import os
import re
from dataclasses import dataclass
from collections import Counter

THISDIR = os.path.dirname(__file__)


@dataclass
class Rule:
    min_: int
    max_: int
    character: str

    @classmethod
    def from_text(cls, line):
        match = re.match(r"(\d+)-(\d+)\s([a-z]):\s[a-z]+", line)
        min_, max_, character = match.groups()
        return Rule(int(min_), int(max_), character)


def test_rule_from_text():
    assert Rule.from_text("1-3 a: abcde") == Rule(1, 3, "a")
    assert Rule.from_text("1-3 b: cdefg") == Rule(1, 3, "b")
    assert Rule.from_text("2-9 c: ccccccccc") == Rule(2, 9, "c")


def get_num_in_passwd(password, character):
    return Counter(password).get(character, 0)


def test_get_num_in_passwd():
    assert get_num_in_passwd("aaa", "a") == 3
    assert get_num_in_passwd("aaabbb", "a") == 3
    assert get_num_in_passwd("aaa", "b") == 0


def is_valid_p1(line) -> bool:
    rule = Rule.from_text(line)
    colon_idx = line.find(":")
    password = line[colon_idx + 1 :].strip()
    num_in_passwd = get_num_in_passwd(password, rule.character)
    return num_in_passwd >= rule.min_ and num_in_passwd <= rule.max_


def is_valid_p2(line) -> bool:
    rule = Rule.from_text(line)
    colon_idx = line.find(":")
    password = line[colon_idx + 1 :].strip()
    return (
        Counter(password[rule.min_ - 1] + password[rule.max_ - 1]).get(
            rule.character, 0
        )
        == 1
    )


def test_is_valid_p1():
    assert is_valid_p1("1-3 a: abcde")
    assert not is_valid_p1("1-3 b: cdefg")
    assert is_valid_p1("2-9 c: ccccccccc")


def part1(lines):
    num_valid = sum((is_valid_p1(line) for line in lines))
    print(f"Num valid: {num_valid}")


def part2(lines):
    num_valid = sum((is_valid_p2(line) for line in lines))
    print(f"Num valid: {num_valid}")


def main():
    with open(os.path.join(THISDIR, "input.txt")) as fp:
        lines = fp.readlines()

    part1(lines)
    part2(lines)


if __name__ == "__main__":
    main()
