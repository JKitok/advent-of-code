import os
import itertools
import numpy as np

rocks = [
    [[0, 0, 0, 0], [0, 1, 2, 3]],
    [[0, -1, -1, -1, -2], [1, 0, 1, 2, 1]],
    [[0, 0, 0, -1, -2], [0, 1, 2, 2, 2]],
    [[0, -1, -2, -3], [0, 0, 0, 0]],
    [[0, 0, -1, -1], [0, 1, 0, 1]],
]


def height(space):
    return space.shape[0] - np.argwhere(np.max(space, axis=1) == 0)[-1][0] - 1


def run(pattern, N, find_period=False):
    space = np.zeros((10000 + 4, 7), np.int8)
    iterpattern = itertools.cycle(enumerate(pattern))
    iterrocks = itertools.cycle(enumerate(rocks))
    pattern_index = len(pattern)  # Previous gas pattern
    i = 0
    cache = {}
    h_periods = 0

    while i < N:
        # Calculate starting position of rock
        y = np.argwhere(np.max(space, axis=1) == 0)[-1][0] - 3
        x = 2

        # Spawn rock at correct coordinate
        ri, rock = next(iterrocks)
        rock_coords = np.array(rock)
        is_long_piece = np.all(rock_coords[0, :] == 0)
        rock_coords[0, :] += y
        rock_coords[1, :] += x

        if find_period:
            # Store current state cache to detect period
            floor = (space != 0).argmax(axis=0)
            floor = floor - np.min(floor)
            state_key = (pattern_index, ri, str(floor.tolist()))
            if state_key not in cache.keys():
                cache[state_key] = (i, height(space))
            else:
                # Success, fast forward using the period
                prev_i, prev_height = cache[state_key]
                period = i - prev_i
                h_period = height(space) - prev_height
                # Fast forward
                periods_left = (N - i) // period
                print(f"Found period: {period} after {i} rounds, fastforwarding")
                i += periods_left * period
                h_periods = periods_left * h_period
                find_period = False
                pass

        gas = True
        while True:
            if gas:
                # Gas
                dy = 0
                pattern_index, dx = next(iterpattern)
                gas = False
            else:
                dy = 1
                dx = 0
                gas = True

            rock_coords[0, :] += dy
            rock_coords[1, :] += dx
            could_move = True

            if (
                np.any(rock_coords[1, :] < 0)
                or np.any(rock_coords[1, :] >= space.shape[1])
                or np.any(rock_coords[0, :] >= space.shape[0])
                or np.any(space[*list(rock_coords)])
            ):
                rock_coords[0, :] -= dy
                rock_coords[1, :] -= dx
                could_move = False

            if not could_move and gas:
                space[*list(rock_coords)] = 1
                break
        i += 1

    return height(space) + h_periods


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    pattern = lines[0]
    pattern = [-1 if c == "<" else 1 for c in pattern]

    print(f"Part 1: {run(pattern, N=2022, find_period=False)}")
    print(f"Part 2: {run(pattern, N=1000000000000, find_period=True)}")
