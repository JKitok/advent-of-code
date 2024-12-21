import os
import numpy as np
import copy
from collections import namedtuple
from dataclasses import dataclass

Key = namedtuple("Index", ["index", "direction"])
Value = namedtuple("Value", ["cost", "visited_index"])


@dataclass
class Value:
    cost: int
    visited_index: list


def run(grid):
    start = np.where(grid == "S")
    start = start[0][0] + start[1][0] * 1j
    end = np.where(grid == "E")
    end = end[0][0] + end[1][0] * 1j
    to_check = {}
    visited = {}
    to_check[Key(start, (0 + 1j))] = Value(0, [start])
    while end not in visited:  # Input and examples only have one way to reach the end
        key = min(to_check, key=lambda x: to_check[x].cost)
        value = to_check[key]
        del to_check[key]
        visited[key.index] = value
        for m, additional_cost in zip([1, 1j, -1j, -1], [0, 1000, 1000, 2000]):
            new_direction = key.direction * m
            new_index = key.index + new_direction
            new_cost = value.cost + additional_cost + 1
            if (
                grid[
                    int(np.round(new_index.real)),
                    int(np.round(new_index.imag)),
                ]
                == "#"
            ):
                continue
            new_key = Key(new_index, new_direction)
            if new_key not in to_check or to_check[new_key].cost > new_cost:
                v = Value(0, [])
                v.cost = new_cost
                v.visited_index = copy.deepcopy(value.visited_index)
                v.visited_index.append(new_index)
                to_check[new_key] = v
            elif to_check[new_key].cost == new_cost:
                for v in value.visited_index:
                    if v not in to_check[new_key].visited_index:
                        to_check[new_key].visited_index.append(v)

            if key.index == end:
                print(f"Part 1: {value.cost}")

    print(f"Part 2: {len(visited[end].visited_index)}")


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    grid = np.array([list(line) for line in lines], dtype=str)
    run(grid)
