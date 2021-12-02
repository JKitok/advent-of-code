import os

import numpy as np


def parse_line_a(line):
    direction, step = line.split(" ", 1)
    step = int(step)
    if direction == "forward":
        return 0, step
    elif direction == "down":
        return step, 0
    elif direction == "up":
        return -step, 0


def parse_line_b(line, aim):
    direction, step = line.split(" ", 1)
    step = int(step)
    if direction == "forward":
        return aim * step, step, 0
    elif direction == "down":
        return 0, 0, step
    elif direction == "up":
        return 0, 0, -step


def part1(lines):
    res = np.array([0, 0])
    for line in lines:
        res += np.array(parse_line_a(line))

    print(f"Answer: {res[0] * res[1]}")


def part2(lines):
    res = np.array([0, 0, 0])  # Depth, Horizontal, Aim
    for line in lines:
        res += np.array(parse_line_b(line, res[2]))

    print(f"Answer: {res[0] * res[1]}")


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    part1(lines)
    part2(lines)


if __name__ == "__main__":
    main()
