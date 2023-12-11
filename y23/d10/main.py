import os
import copy

from dataclasses import dataclass

import numpy as np


def max_9(v):
    if isinstance(v, int):
        return v % 10
    else:
        return v


def print_grid(lines):
    print("")
    for line in lines:
        print("".join((str(max_9(v)) for v in line)))
    print("")


def find_start(lines):
    x, y = np.where(lines == "S")
    return x[0], y[0]


def find_start_direction(lines, x, y, first=True):
    for x1, y1, valid in [
        (x - 1, y, ["-", "L", "F"]),
        (x + 1, y, ["-", "J", "\\"]),
        (x, y - 1, ["|", "F", "\\"]),
        (x, y + 1, ["|", "J", "L"]),
    ]:
        if not 0 <= x1 < len(lines[0]):
            continue
        if not 0 <= y1 < len(lines):
            continue
        v = lines[y1][x1]
        if v != "." and v in valid:
            if first:
                return x1 - x, y1 - y
            else:
                first = True


def find_next_direction(dx, dy, s):
    if s == "-" or s == "|":
        return dx, dy
    elif s == "\\":
        return dy, dx
    elif s == "J":
        return -dy, -dx
    elif s == "L":
        return dy, dx
    elif s == "F":
        return -dy, -dx
    else:
        raise ValueError(s)


def traverse_pipe(array, start_x, start_y, first, func):
    x, y = start_x, start_y
    dx, dy = find_start_direction(array, x, y, first)
    s = lines[y + dy][x + dx]
    continue_ = True
    while not s == "S" and continue_:
        x += dx
        y += dy
        continue_ = func(x, y, dx, dy, s)
        dx, dy = find_next_direction(dx, dy, s)
        s = lines[y + dy][x + dx]


class MarkDistance:
    def __init__(self, grid):
        self.step = 1
        self.grid = np.zeros_like(grid, dtype=np.int64)

    def __call__(self, x, y, *_):
        self.grid[y][x] = self.step
        self.step += 1
        return True


def part1(array):
    y, x = find_start(array)
    dist1 = MarkDistance(array)
    dist2 = MarkDistance(array)
    traverse_pipe(array, x, y, first=True, func=dist1)
    traverse_pipe(array, x, y, first=False, func=dist2)
    return np.max(np.minimum(dist1.grid, dist2.grid))


LEFT_SIDE = {
    ("-", 1, 0): (0, -1),
    ("-", -1, 0): (0, 1),
    ("|", 0, -1): (-1, 0),
    ("|", 0, 1): (1, 0),
}


class MarkInsideOutside:
    GRID = 1
    OUTSIDE = 2
    INSIDE = 3

    def __init__(self, grid):
        self.grid = np.zeros_like(grid, dtype=np.int64)
        self.outside_side = 0

    def mark_grid(self, x, y, *_):
        self.grid[y][x] = self.GRID
        return True

    def fill_outside(self):
        for y in [0, self.grid.shape[0] - 1]:
            for x in range(self.grid.shape[1]):
                if not self.grid[y][x] == self.GRID:
                    self.grid[y][x] = self.OUTSIDE

        for x in [0, self.grid.shape[1] - 1]:
            for y in range(self.grid.shape[0]):
                if not self.grid[y][x] == self.GRID:
                    self.grid[y][x] = self.OUTSIDE

    def explode(self, s):
        area = 0
        new_area = np.count_nonzero(self.grid == s)
        while new_area > area:
            area = new_area
            for y in range(len(lines)):
                for x in range(len(lines[0])):
                    if self.grid[y][x] == s:
                        for x1, y1 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                            if not 0 <= x1 < len(lines[0]):
                                continue
                            elif not 0 <= y1 < len(lines):
                                continue
                            elif self.grid[y1][x1] in (
                                self.GRID,
                                self.INSIDE,
                                self.OUTSIDE,
                            ):
                                continue
                            else:
                                self.grid[y1][x1] = s
            new_area = np.count_nonzero(self.grid == s)

    def find_outside_side(self, x, y, dx, dy, s):
        if s in ("-", "|"):
            left_x, left_y = LEFT_SIDE[(s, dx, dy)]
            right_x, right_y = -left_x, -left_y
            if self.grid[y + left_y][x + left_x] == self.OUTSIDE:
                self.outside_side = 1
                return False
            elif self.grid[y + right_y][x + right_x] == self.OUTSIDE:
                self.outside_side = -1
                return False
        return True

    def mark(self, x, y, s):
        if 0 <= y < self.grid.shape[0] and 0 <= x < self.grid.shape[1]:
            if self.grid[y][x] != self.GRID:
                if self.grid[y][x] not in (self.GRID, 0):
                    assert self.grid[y][x] == s, f"{self.grid[y][x]} != {s}"
                self.grid[y][x] = s

    def fill_around_pipe(self, x, y, dx, dy, s):
        assert self.outside_side != 0
        if s in ("-", "|"):
            dx_out, dy_out = LEFT_SIDE[(s, dx, dy)]
            dx_in, dy_in = -dx_out, -dy_out
            if self.outside_side == -1:
                (dx_in, dy_in), (dx_out, dy_out) = (dx_out, dy_out), (dx_in, dy_in)
            self.mark(x + dx_in, y + dy_in, self.INSIDE)
            self.mark(x + dx_out, y + dy_out, self.OUTSIDE)
        elif s == "J":
            if dx == 1:
                m = self.INSIDE if self.outside_side == 1 else self.OUTSIDE
            elif dy == 1:
                m = self.OUTSIDE if self.outside_side == 1 else self.INSIDE
            else:
                raise ValueError
            self.mark(x + 1, y, m)
            self.mark(x, y + 1, m)
        elif s == "\\":
            if dx == 1:
                m = self.OUTSIDE if self.outside_side == 1 else self.INSIDE
            elif dy == -1:
                m = self.INSIDE if self.outside_side == 1 else self.OUTSIDE
            else:
                raise ValueError
            self.mark(x + 1, y, m)
            self.mark(x, y - 1, m)
        elif s == "L":
            if dx == -1:
                m = self.OUTSIDE if self.outside_side == 1 else self.INSIDE
            elif dy == 1:
                m = self.INSIDE if self.outside_side == 1 else self.OUTSIDE
            else:
                raise ValueError
            self.mark(x - 1, y, m)
            self.mark(x, y + 1, m)
        elif s == "F":
            if dx == -1:
                m = self.INSIDE if self.outside_side == 1 else self.OUTSIDE
            elif dy == -1:
                m = self.OUTSIDE if self.outside_side == 1 else self.INSIDE
            else:
                raise ValueError
            self.mark(x - 1, y, m)
            self.mark(x, y - 1, m)
        return True


def part2(array):
    y, x = find_start(array)
    mark = MarkInsideOutside(array)
    mark.grid[y][x] = mark.GRID
    traverse_pipe(array, x, y, first=True, func=mark.mark_grid)
    mark.fill_outside()
    mark.explode(MarkInsideOutside.OUTSIDE)
    traverse_pipe(array, x, y, first=True, func=mark.find_outside_side)
    traverse_pipe(array, x, y, first=True, func=mark.fill_around_pipe)
    mark.explode(MarkInsideOutside.INSIDE)
    mark.explode(MarkInsideOutside.OUTSIDE)
    if np.count_nonzero(mark.grid == 0) != 0:
        print("Warning: All locations not classified!")
    return np.count_nonzero(mark.grid == mark.INSIDE)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip().replace("7", "\\") for v in lines]
    lines = [list(v) for v in lines]
    arr = np.array(lines, dtype=np.str_)

    print(f"Part 1: {part1(arr)}")
    print(f"Part 2: {part2(arr)}")
