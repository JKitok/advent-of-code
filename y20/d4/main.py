import os
import re

from dataclasses import dataclass

import numpy as np


def read_fields(line):
    values = [re.match(r"(.+):(.+)", s).groups() for s in line.split(" ")]
    return dict(values)


def parse_passports(lines):
    passport_lines = []
    while len(lines):
        try:
            next_ = lines.index("")
        except ValueError:
            next_ = len(lines)
        passport_lines.append(lines[:next_])
        lines = lines[next_ + 1 :]

    passports = []
    for line in passport_lines:
        passports.append(read_fields(" ".join(line)))
    return passports


def passport_contains_required_keys(dict_):
    for key in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]:
        if key not in dict_.keys():
            return False
    else:
        return True


def check_int_range(value, min_, max_):
    try:
        year = int(value)
    except ValueError:
        return False
    else:
        return min_ <= year <= max_


def check_byr(value):
    return check_int_range(value, 1920, 2002)


def check_iyr(value):
    return check_int_range(value, 2010, 2020)


def check_eyr(value):
    return check_int_range(value, 2020, 2030)


def test_check_byr():
    assert not check_byr("")
    assert not check_byr("1919")
    assert check_byr("1920")
    assert check_byr("2002")
    assert not check_byr("2003")


def check_hgt(value):
    if value.endswith("cm"):
        try:
            length = int(value.replace("cm", ""))
        except ValueError:
            return False
        else:
            return 150 <= length <= 193
    elif value.endswith("in"):
        try:
            length = int(value.replace("in", ""))
        except ValueError:
            return False
        else:
            return 59 <= length <= 76
    else:
        return False


def test_check_hgt():
    assert not check_hgt("")

    assert not check_hgt("149cm")
    assert check_hgt("150cm")
    assert not check_hgt("194cm")

    assert not check_hgt("58in")
    assert check_hgt("59in")
    assert not check_hgt("77in")


def check_hcl(value):
    return bool(re.match(r"^#[0-9a-f]{6}$", value))


def test_check_hcl():
    assert check_hcl("#000000")
    assert not check_hcl("#00000")
    assert not check_hcl("00000")
    assert not check_hcl("#0000gg")


def check_ecl(value):
    return value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def check_pid(value):
    return bool(re.match(r"^[0-9]{9}$", value))


def fields_are_ok(dict_):
    if not check_byr(dict_["byr"]):
        return False
    if not check_iyr(dict_["iyr"]):
        return False
    if not check_eyr(dict_["eyr"]):
        return False
    if not check_hgt(dict_["hgt"]):
        return False
    if not check_hcl(dict_["hcl"]):
        return False
    if not check_ecl(dict_["ecl"]):
        return False
    if not check_pid(dict_["pid"]):
        return False
    return True


def part1(lines):
    passports = parse_passports(lines)
    return sum(passport_contains_required_keys(p) for p in passports)


def part2(lines):
    passports = parse_passports(lines)
    passports = [p for p in passports if passport_contains_required_keys(p)]
    passports = [p for p in passports if fields_are_ok(p)]
    return len(passports)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
