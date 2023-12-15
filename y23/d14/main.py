import os
import math

import numpy as np


def tilt(array, direction):
    dx, dy = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}[direction]
    moved = True
    while moved:
        moved = False
        idx_y, idx_x = np.where(array == "O")
        for x, y in zip(idx_x, idx_y):
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < array.shape[1] and 0 <= new_y < array.shape[0]:
                if array[new_y, new_x] == ".":
                    array[new_y, new_x] = "O"
                    array[y, x] = "."
                    moved = True
    return array


def load(array):
    idx_y, _ = np.where(array == "O")
    return sum((array.shape[0] - y for y in idx_y))


def part1(array):
    array = tilt(array, "N")
    return load(array)


class CycleDetector:
    def __init__(self, min_=5, max_=50):
        self._loads = np.zeros(2 * max_ + 1)
        self._idx = 0
        self._detect = False
        self.cycle = 0
        self._min = min_

    def detect(self, v):
        self._loads[self._idx] = v
        self._idx = (self._idx + 1) % self._loads.size
        if self._idx == 0:
            self._detect = True
        return self._do_detect()

    def _do_detect(self):
        if not self._detect:
            return False
        idx = self._idx - 1
        for cycle in range(self._min, len(self._loads)):
            found = True
            for i in range(0, cycle):
                found = found and (self._loads[idx - i] == self._loads[idx - cycle - i])
            if found:
                self.cycle = cycle
                return True


def part2(array):
    N = 1000000000
    n = 0
    cycle_found = False
    detector = CycleDetector()
    while n < N:
        for dir_ in ["N", "W", "S", "E"]:
            array = tilt(array, dir_)
        n += 1
        if not cycle_found:
            cycle_found = detector.detect(load(array))
            if cycle_found:
                n += detector.cycle * ((N - n) // detector.cycle)
        if n % 10 == 0:
            print(n)
    return load(array)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    lines = [list(l) for l in lines]
    array = np.array(lines, dtype=np.str_)

    print(f"Part 1: {part1(np.copy(array))}")
    print(f"Part 2: {part2(np.copy(array))}")
