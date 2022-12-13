import os
import itertools
from dataclasses import dataclass

import numpy as np

BIG = int(10e10)


def djikstra(data, all_start, end_x, end_y):
    cost = np.zeros_like(data, dtype=np.int64) + BIG
    non_visited = np.ones_like(cost, dtype=bool)
    cost[end_x, end_y] = 0
    while any(non_visited[i] for i in all_start):
        i, j = np.unravel_index(
            np.ma.argmin(np.ma.MaskedArray(cost, ~non_visited)), cost.shape
        )
        for di, dj in itertools.product([-1, 0, 1], [-1, 0, 1]):
            if di != 0 and dj != 0:
                continue
            ni = i + di
            nj = j + dj
            if ni < 0 or ni >= data.shape[0] or nj < 0 or nj >= data.shape[1]:
                continue
            elif data[i, j] - data[ni, nj] > 1:
                continue
            else:
                new_cost = cost[i, j] + 1
                cost[ni, nj] = min(new_cost, cost[ni, nj])
        non_visited[i, j] = False

    return cost


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    data = np.zeros((len(lines), len(lines[0])), dtype=np.int64)
    start_x, start_y = 0, 0
    end_x, end_y = 0, 0
    all_start = []
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == "S":
                start_x, start_y = i, j
                c = "a"
            elif c == "E":
                end_x, end_y = i, j
                c = "z"
            elif c in ["S", "a"]:
                all_start.append((i, j))
            data[i, j] = ord(c) - ord("a")

    cost = djikstra(data, all_start, end_x, end_y)
    print(f"Part 1: {cost[start_x, start_y]}")
    print(f"Part 2: {min(cost[s] for s in all_start)}")
