import os

import numpy as np


def part1(matrix):
    vis_count = 0
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            if i in (0, matrix.shape[0]) or j in (0, matrix.shape[1]):
                vis_count += 1
            else:
                left_visible = (matrix[i, j] > matrix[i, :j]).all()
                right_visible = (matrix[i, j] > matrix[i, j + 1 :]).all()
                up_visible = (matrix[i, j] > matrix[:i, j]).all()
                down_visible = (matrix[i, j] > matrix[i + 1 :, j]).all()
                vis_count += left_visible or right_visible or up_visible or down_visible
    return vis_count


def part2(matrix):
    def check(v, arr):
        if arr.size == 0:
            return 0
        elif (v > arr).all():
            return arr.size
        else:
            return 1 + (v <= arr).argmax()

    max_ = 0
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            up_view = check(matrix[i, j], np.flipud(matrix[:i, j]))
            left_view = check(matrix[i, j], np.flip(matrix[i, :j]))
            down_view = check(matrix[i, j], matrix[i + 1 :, j])
            right_view = check(matrix[i, j], matrix[i, j + 1 :])
            max_ = max(max_, up_view * left_view * down_view * right_view)
    return max_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    comma_separated = [",".join(line) for line in lines]
    matrix = np.fromstring(",".join(comma_separated), sep=",").reshape(
        len(lines), len(lines[0])
    )

    print(f"Part 1: {part1(matrix)}")
    print(f"Part 2: {part2(matrix)}")
