import os

import numpy as np

STEPS = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}


def dijkstra(array, min_, max_):
    # Dimensions are x0, x1, direction, num steps in direction
    visited = np.zeros((*array.shape, 4, max_ - min_ + 1), dtype=bool)
    heat_loss = np.zeros_like(visited, dtype=np.int64) + 1e6

    def IDX(n):
        return n - min_

    def FROM_IDX(n):
        return n + min_

    x0, x1 = 0, 0
    step = None
    old_N = None
    old_value = 0
    while True:
        if step is not None:
            visited[x0, x1, step, IDX(old_N)] = 1

        for new_step, (dx0, dx1) in STEPS.items():
            if STEPS.get(step, (0, 0)) in [(dx0, dx1), (-dx0, -dx1)]:
                continue  # Cannot go back
            for new_N in range(min_, max_ + 1):
                x0n = x0 + new_N * dx0
                x1n = x1 + new_N * dx1
                if not (0 <= x0n < array.shape[0] and 0 <= x1n < array.shape[1]):
                    continue
                if not visited[x0n, x1n, new_step, IDX(new_N)]:
                    if dx0 > 0:
                        new_value = old_value + np.sum(array[x0 + 1 : x0n + 1, x1])
                    elif dx0 < 0:
                        new_value = old_value + np.sum(array[x0n:x0, x1])
                    elif dx1 > 0:
                        new_value = old_value + np.sum(array[x0, x1 + 1 : x1n + 1])
                    else:
                        new_value = old_value + np.sum(array[x0, x1n:x1])
                    if heat_loss[x0n, x1n, new_step, IDX(new_N)] > new_value:
                        heat_loss[x0n, x1n, new_step, IDX(new_N)] = new_value

        if np.any(visited[array.shape[0] - 1, array.shape[1] - 1, :, :]):
            return np.min(
                heat_loss[array.shape[0] - 1, array.shape[-1] - 1, :, :].flatten()
            )

        indices = np.nonzero(~visited)
        n = np.argmin(heat_loss[indices])
        x0 = indices[0][n]
        x1 = indices[1][n]
        step = indices[2][n]
        old_N = FROM_IDX(indices[3][n])
        old_value = heat_loss[x0, x1, step, IDX(old_N)]


def part1(array):
    return dijkstra(array, min_=1, max_=3)


def part2(array):
    return dijkstra(array, min_=4, max_=10)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [list(v.strip()) for v in lines]
    array = np.array(lines, dtype=np.int64)

    print(f"Part 1: {part1(array)}")
    print(f"Part 2: {part2(array)}")
