import os
import re
import numpy as np
import cv2


def part1(equations, X, Y, T=100):
    quarters = [0, 0, 0, 0]
    middle_x = (X - 1) / 2
    middle_y = (Y - 1) / 2
    for x0, y0, vx, vy in equations:
        x = (x0 + vx * T) % X
        y = (y0 + vy * T) % Y
        if x < middle_x and y < middle_y:
            quarters[0] += 1
        elif x < middle_x and y > middle_y:
            quarters[1] += 1
        if x > middle_x and y < middle_y:
            quarters[2] += 1
        elif x > middle_x and y > middle_y:
            quarters[3] += 1

    return np.prod(quarters)


def part2(equations, X, Y, T=10000):
    output_folder = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_folder, exist_ok=True)

    pattern = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.float32)

    for t in range(10000):
        grid = np.full((Y, X), 0, dtype=np.float32)
        for x0, y0, vx, vy in equations:
            x = (x0 + vx * t) % X
            y = (y0 + vy * t) % Y
            grid[y][x] = 1

        match = cv2.matchTemplate(grid, pattern, cv2.TM_SQDIFF)
        positions = np.argwhere(match == 0)
        if len(positions) > 0:
            print(f"Match: {t}")
            file = os.path.join(output_folder, f"{t}.txt")
            np.savetxt(file, grid, delimiter="", fmt="%.0f")


def parse(lines):
    equations = []
    for line in lines:
        x, y, vx, vy = re.findall(r"-?\d+", line)
        equations.append([*map(int, (x, y, vx, vy))])
    return equations


if __name__ == "__main__":
    if False:
        file = "example.txt"
        X = 11
        Y = 7
    else:
        file = "input.txt"
        X = 101
        Y = 103
    with open(os.path.join(os.path.dirname(__file__), file)) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    equations = parse(lines)
    print(f"Part 1: {part1(equations, X, Y)}")
    print(f"Part 2: {part2(equations, X, Y)}")
