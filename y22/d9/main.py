import os
import math

import numpy as np

sign = lambda x: int(math.copysign(1, x))


def follow(Hx, Hy, Tx, Ty):
    dx = Hx - Tx
    dy = Hy - Ty
    if abs(dx) > 1:
        if abs(dy) > 0:
            return Tx + sign(dx), Ty + sign(dy)
        else:
            return Tx + sign(dx), Ty
    elif abs(dy) > 1:
        if abs(dx) > 0:
            return Tx + sign(dx), Ty + sign(dy)
        else:
            return Tx, Ty + sign(dy)
    return Tx, Ty


def move(instructions, N):
    visited = set()
    positions = [[0, 0] for i in range(N)]
    for instr in instructions:
        direction, n = instr.split(" ")
        dHx, dHy = {"R": (1, 0), "D": (0, -1), "L": (-1, 0), "U": (0, 1)}[direction]
        for i in range(int(n)):
            positions[0][0] += dHx
            positions[0][1] += dHy
            for t in range(1, N):
                positions[t] = follow(*positions[t - 1], *positions[t])
            visited.add(positions[-1])

    return len(visited)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    instructions = [v.strip() for v in lines]
    print(f"Part 1: {move(instructions, N=2)}")
    print(f"Part 2: {move(instructions, N=10)}")
