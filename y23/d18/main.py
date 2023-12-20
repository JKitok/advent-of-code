import os
import re
from queue import Queue
import numpy as np

STEPS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}


def floodfill(arr, coords, val):
    x, y = coords
    val_to_replace = arr[y, x]
    q = Queue()
    q.put((x, y))
    while not q.empty():
        x, y = q.get()
        arr[y, x] = val
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= y + dy < arr.shape[0] and 0 <= x + dx < arr.shape[1]:
                if arr[y + dy, x + dx] == val_to_replace:
                    q.put((x + dx, y + dy))
                    arr[y + dy, x + dx] = val
    return arr


def part1(lines):
    coords = [(0, 0)]
    x, y = 0, 0
    for direction, N, color in lines:
        for n in range(int(N)):
            dx, dy = STEPS[direction]
            x += dx
            y += dy
            coords.append((x, y))
    min_x = min(v[0] for v in coords)
    max_x = max(v[0] for v in coords)
    min_y = min(v[1] for v in coords)
    max_y = max(v[1] for v in coords)
    x_off = -min_x + 1
    y_off = -min_y + 1
    arr = np.zeros((max_y - min_y + 3, max_x - min_x + 3), dtype=np.int64)
    for x, y in coords:
        arr[y + y_off, x + x_off] = 1

    arr = floodfill(arr, (0, 0), 2)
    print(np.flipud(arr))
    return np.sum(arr != 2)


def part2(lines):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    data = [re.match(r"([A-Z]) (\d+) \(\#(.*)\)", l).groups() for l in lines]

    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
