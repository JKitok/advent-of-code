import os

from queue import Queue
import numpy as np


def part1(array, start):
    energized = np.zeros_like(array, dtype=np.bool8)
    beams = Queue()
    beams.put(start)  # x0, x1, vx0, vx1
    encountered_beams = set()
    while not beams.empty():
        x0, x1, vx0, vx1 = beams.get()
        while True:
            x0 += vx0
            x1 += vx1
            if (not 0 <= x0 < array.shape[0]) or not (0 <= x1 < array.shape[1]):
                break  # Beam has left
            elif (x0, x1, vx0, vx1) in encountered_beams:
                break  # We have already handled this
            else:
                encountered_beams.add((x0, x1, vx0, vx1))

            v = array[x0, x1]
            energized[x0, x1] = 1
            if v == ".":
                continue
            elif v == "\\":
                vx1, vx0 = vx0, vx1
            elif v == "/":
                vx1, vx0 = -vx0, -vx1
            elif v == "|":
                if vx1 != 0:
                    vx0 = 1
                    vx1 = 0
                    beams.put((x0, x1, -1, 0))
            elif v == "-":
                if vx0 != 0:
                    vx0 = 0
                    vx1 = 1
                    beams.put((x0, x1, 0, -1))
            else:
                raise ValueError(v)

    return np.sum(np.sum(energized))


def part2(array):
    max_ = 0
    for x0 in range(0, array.shape[0]):
        max_ = max(max_, part1(array, (x0, -1, 0, 1)))
    for x0 in range(0, array.shape[0]):
        max_ = max(max_, part1(array, (x0, array.shape[1], 0, -1)))
    for x1 in range(0, array.shape[1]):
        max_ = max(max_, part1(array, (-1, x1, 1, 0)))
    for x1 in range(0, array.shape[1]):
        max_ = max(max_, part1(array, (array.shape[0], x1, -1, 0)))
    return max_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [list(v.strip()) for v in lines]
    arr = np.array(lines, dtype=np.str_)
    print(f"Part 1: {part1(arr, (0, -1, 0, 1))}")
    print(f"Part 2: {part2(arr)}")
