import os
import re


def getmap(map_, v):
    return map_[round(-v.imag)][round(v.real)]


def increase(position, v, map_):
    position += v
    if -position.imag >= len(map_):
        position = position.real
    elif position.imag > 0:
        position = position.real - 1j * (len(map_) - 1)

    if position.real >= len(map_[0]):
        position = 1j * position.imag
    elif position.real < 0:
        position = len(map_[0]) - 1 + 1j * position.imag
    return position


def find_next(map_, direction, position):
    while True:
        position = increase(position, direction, map_)
        if getmap(map_, position) != " ":
            return position


def part1(map_, instructions):
    direction = 1
    position = find_next(map_, direction, 0)
    for instr in instructions:
        if instr == "L":
            direction *= 1j
        elif instr == "R":
            direction *= -1j
        else:
            num = int(instr)
            for _ in range(num):
                new = increase(position, direction, map_)
                if getmap(map_, new) == " ":
                    new = find_next(map_, direction, new)
                if getmap(map_, new) == ".":
                    position = new
                elif getmap(map_, new) == "#":
                    break
    score_map = {1: 0, -1j: 1, -1: 2, 1j: 3}
    return int(
        1000 * (-position.imag + 1) + 4 * (position.real + 1) + score_map[direction]
    )


def part2(entries):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    *map_, _, instructions = [v.rstrip("\n") for v in lines]
    max_ = max(len(v) for v in map_)
    map_ = [v.ljust(max_) for v in map_]
    instructions = re.findall("(\d+|L|R)", instructions)

    print(f"Part 1: {part1(map_, instructions)}")
    print(f"Part 2: {part2(lines)}")
