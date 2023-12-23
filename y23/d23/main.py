import os
import copy
from dataclasses import dataclass
from queue import Queue
import numpy as np


def get_neighbors(x0, x1, array, visited):
    all_ = []
    for dx0, dx1, okstep in [(0, -1, "<"), (0, 1, ">"), (-1, 0, "^"), (1, 0, "v")]:
        x0n = x0 + dx0
        x1n = x1 + dx1
        if not (0 <= x0n < array.shape[0] and 0 <= x1n < array.shape[1]):
            continue
        elif array[x0n, x1n] not in [".", okstep]:
            continue
        elif array[x0, x1] in "<>^v" and array[x0, x1] != okstep:
            continue
        else:
            if (x0n, x1n) in visited:
                continue
            else:
                all_.append((x0n, x1n))
    return all_


def part1(array):
    x0end = array.shape[0] - 1
    x1end = array.shape[1] - 2
    distances = []
    q = Queue()
    q.put((0, 1, set()))
    while not q.empty():
        stop = False
        x0, x1, visited = q.get()
        while not stop:
            if (x0, x1) == (x0end, x1end):
                distances.append(len(visited))
                stop = True
                continue
            visited.add((x0, x1))
            possible_next = get_neighbors(x0, x1, array, visited)
            if len(possible_next) == 0:
                stop = False  # Deadend
                continue
            if len(possible_next) > 1:
                for i, j in possible_next[1:]:
                    q.put((i, j, copy.deepcopy(visited)))
            x0, x1 = possible_next[0]
    return max(distances)


def part2(array):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [list(v.strip()) for v in lines]
    array = np.array(lines, dtype=np.str_)

    print(f"Part 1: {part1(array)}")
    print(f"Part 2: {part2(array)}")
