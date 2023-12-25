import os
import copy
from collections import defaultdict
from queue import Queue

import numpy as np


def get_neighbors(x0, x1, array, visited, only_this_dx=None):
    all_ = []
    for dx0, dx1, okstep in [(0, -1, "<"), (0, 1, ">"), (-1, 0, "^"), (1, 0, "v")]:
        if only_this_dx is not None and (dx0, dx1) != (only_this_dx):
            continue
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


def find_next_crossroad(array, x0, x1, dx0, dx1):
    x0end = array.shape[0] - 1
    x1end = array.shape[1] - 2
    visited = set()
    while True:
        if (x0, x1) == (x0end, x1end):
            return (x0, x1), len(visited) - 1
        visited.add((x0, x1))
        possible_next = get_neighbors(
            x0, x1, array, visited, (dx0, dx1) if dx0 is not None else None
        )
        dx0 = None
        if len(possible_next) == 0:
            # Deadend
            return None, None
        if len(possible_next) > 1:
            return (x0, x1), len(visited) - 1
        else:
            x0, x1 = possible_next[0]


def run(array):
    # Create graph
    x0end = array.shape[0] - 1
    x1end = array.shape[1] - 2
    q = Queue()
    nodes = defaultdict(lambda: dict())
    nodes[(0, 1)] = {(1, 0): None}
    q.put((0, 1, 1, 0))
    while not q.empty():
        x0, x1, dx0, dx1 = q.get()
        new_node, distance = find_next_crossroad(array, x0, x1, dx0, dx1)
        if new_node is not None:
            if new_node == (x0end, x1end):
                # Found end
                nodes[(x0, x1)][(dx0, dx1)] = (new_node, distance)
            else:
                nodes[(x0, x1)][(dx0, dx1)] = (new_node, distance)
                neighbors = get_neighbors(*new_node, array, set())
                for n in neighbors:
                    dx0 = n[0] - new_node[0]
                    dx1 = n[1] - new_node[1]
                    if nodes[new_node].get((dx0, dx1)) is None:
                        q.put((*new_node, dx0, dx1))
                    else:
                        pass
    # Find node that leads to end, other paths can be discarded
    last_nodes = set()
    for (x0, x1), edges in nodes.items():
        for (x0n, x1n), _ in edges.values():
            if (x0n, x1n) == (x0end, x1end):
                last_nodes.add((x0, x1))
    # Now calculate all paths
    if len(last_nodes) == 1:
        last_node = last_nodes.pop()
    else:
        last_node = None
    stack = []
    distances = []
    max_ = 0
    stack.append(((0, 1), 0, set()))
    while len(stack) > 0:
        (x0, x1), distance, nodes_visited = stack.pop()
        stop = False
        while not stop:
            nodes_visited.add((x0, x1))
            if (x0, x1) == (x0end, x1end):
                distances.append(distance + 1)
                if max(distances) > max_:
                    max_ = max(distances)
                    print(max_)
                    stop = True
            elif (
                last_node is not None
                and (x0, x1) != last_node
                and last_node in nodes_visited
            ):
                stop = True
                continue

            all_ = [v for v in nodes[(x0, x1)].values() if v[0] not in nodes_visited]
            if len(all_) == 0:
                stop = True
            else:
                for (x0next, x1next), d in all_[1:]:
                    stack.append(
                        (
                            (x0next, x1next),
                            distance + d,
                            copy.deepcopy(nodes_visited),
                        )
                    )
                (x0, x1), d = all_[0]
                distance += d

    return max(distances)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [list(v.strip()) for v in lines]
    array = np.array(lines, dtype=np.str_)

    print(f"Part 1: {run(array)}")
    for s in "<>^v":
        array[np.where(array == s)] = "."
    print(f"Part 2: {run(array)}")
