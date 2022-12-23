import os
import copy
from collections import defaultdict
from dataclasses import dataclass


def run(positions, N=10):
    considerations = [
        [-1 + 1j, 1j, 1 + 1j],
        [-1 - 1j, -1j, 1 - 1j],
        [-1 - 1j, -1, -1 + 1j],
        [1 - 1j, 1, 1 + 1j],
    ]
    around = set()
    for c in considerations:
        for v in c:
            around.add(v)

    for round in range(N):
        if round % 10 == 0:
            print(f"{round=}", end="\r")
        consider = dict()
        for i, elf in enumerate(positions):
            possible = {v: ((elf + v) not in positions) for v in around}
            if all(possible.values()):
                consider[elf] = elf
            else:
                for c in considerations:
                    if all(possible[v] for v in c):
                        consider[elf] = elf + c[1]
                        break
                else:
                    consider[elf] = elf

        new_positions = set()
        counts = defaultdict(int)
        for c in consider.values():
            counts[c] += 1

        for pos in positions:
            new_pos = consider[pos]
            if counts[new_pos] == 1:
                new_positions.add(new_pos)
            else:
                new_positions.add(pos)
        if new_positions == positions:
            return positions, round + 1
        else:
            positions = new_positions
        considerations = [*considerations[1:], considerations[0]]

    return positions, N


def part1(positions, N=10):
    positions, _ = run(positions, N=10)
    min_x = int(min(p.real for p in positions))
    max_x = int(max(p.real for p in positions))
    min_y = int(min(p.imag for p in positions))
    max_y = int(max(p.imag for p in positions))

    cnt = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            cnt += (x + y * 1j) not in positions
    return cnt


def part2(positions):
    return run(positions, N=10000)[1]


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    positions = set()
    for j, line in enumerate(lines):
        for i, c in enumerate(line):
            if c == "#":
                positions.add(i + (len(lines) - 1 - j) * 1j)

    print(f"Part 1: {part1(copy.deepcopy(positions))}")
    print(f"Part 2: {part2(copy.deepcopy(positions))}")
