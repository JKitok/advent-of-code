import os

from sympy import *
import numpy as np


def parse1(line):
    _, rest = line.split(":")
    return np.fromstring(rest, sep=" ").astype(np.int64)


def part1(lines):
    times = parse1(lines[0])
    records = parse1(lines[1])
    all_count = []
    for time, record in zip(times, records):
        cnt = 0
        for charge_time in range(1, time):
            distance = charge_time * (time - charge_time)
            cnt += distance > record
        all_count.append(cnt)
    return np.prod(all_count)


def parse2(line):
    _, rest = line.split(":")
    rest = rest.replace(" ", "")
    return int(rest)


def part2(lines):
    time = parse2(lines[0])
    record = parse2(lines[1])
    var("x")
    lower, upper = solve(f"x*({time} - x) - {record}", x)
    ceil_f = ceiling(x)
    lower = ceil_f.subs(x, lower)
    floor_f = floor(x)
    upper = floor_f.subs(x, upper)
    return upper - lower + 1


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
