import os
import itertools

import numpy as np


class Array(np.ndarray):
    boundary = 0

    def __getitem__(self, idx):
        if isinstance(idx, tuple) and len(idx) == 2:
            N, M = self.shape
            if idx[0] < 0 or idx[1] < 0 or idx[0] >= N or idx[1] >= M:
                return self.boundary
        return super().__getitem__(idx)


def run(img, algorithm, N):
    image = np.zeros((img.shape[0] + 2 * N, img.shape[1] + 2 * N), dtype=int)
    image[N:-N, N:-N] = img
    boundary = 0
    for n in range(N):
        old_image = np.copy(image).view(Array)
        old_image.boundary = boundary
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                idx = sum(
                    (
                        old_image[i + v[0], j + v[1]] * (2 ** (8 - x))
                        for (x, v) in enumerate(
                            itertools.product([-1, 0, 1], [-1, 0, 1])
                        )
                    )
                )
                image[i, j] = algorithm[idx]

        boundary = algorithm[-1 if old_image.boundary else 0]
        print(f"n: {n}")
    return np.sum(image)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    algo_line, _, *img_lines = [v.strip() for v in lines]
    algorithm = [1 if v == "#" else 0 for v in algo_line]
    img = np.fromstring(
        ",".join("".join(img_lines).replace("#", "1").replace(".", "0")), sep=","
    )
    img = img.reshape(len(img_lines), len(img) // len(img_lines))
    print(f"Part 1: {run(img, algorithm, 2)}")
    print(f"Part 2: {run(img, algorithm, 50)}")
