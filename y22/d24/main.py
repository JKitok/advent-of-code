import os
from collections import defaultdict


def run(blizzards, walls, X, Y):
    start = 1 + (Y - 1) * 1j
    destination = X - 2
    part1_reached = False
    positions = set()
    positions.add((start, False, False))
    t = 0
    while True:
        t += 1
        # Move blizzards
        new_blizzards = defaultdict(list)
        for pos, all_b in blizzards.items():
            for b in all_b:
                new_pos = pos + b
                if new_pos.real == 0:
                    new_pos = X - 2 + new_pos.imag * 1j
                elif new_pos.real == X - 1:
                    new_pos = 1 + new_pos.imag * 1j
                elif new_pos.imag == 0:
                    new_pos = new_pos.real + (Y - 2) * 1j
                elif new_pos.imag == Y - 1:
                    new_pos = new_pos.real + 1j
                new_blizzards[new_pos].append(b)
        blizzards = new_blizzards
        # Do all possible movements
        new_positions = set()
        for pos, reached_dest, reached_start in positions:
            for dp in [0, 1, 1j, -1, -1j]:
                new_pos = pos + dp
                if new_pos not in walls and (
                    0 <= new_pos.real < X and 0 <= new_pos.imag < Y
                ):
                    if new_pos not in blizzards.keys():
                        new_positions.add((new_pos, reached_dest, reached_start))
                        if not reached_dest:
                            reached_dest = new_pos == destination
                        elif not reached_start:
                            reached_start = new_pos == start
                        if not part1_reached and reached_dest:
                            print(f"Part 1: {t}")
                            part1_reached = True

                        if reached_dest and reached_start and new_pos == destination:
                            print(f"Part 2: {t}")
                            return

        positions = new_positions


def part2(entries):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    X = len(lines[0])
    Y = len(lines)
    blizzards = {}
    walls = set()
    for y, line in enumerate(reversed(lines)):
        for x, c in enumerate(line):
            if c == ".":
                continue
            elif c == "#":
                walls.add(x + y * 1j)
            else:
                direction = {">": 1, "<": -1, "^": 1j, "v": -1j}[c]
                blizzards[x + y * 1j] = [direction]

    run(blizzards, walls, X, Y)
