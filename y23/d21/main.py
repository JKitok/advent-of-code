import os
import numpy as np
import pickle


THISDIR = os.path.dirname(__file__)


def run(array, num=64, dump=False):
    N, M = array.shape
    res = np.where(array == "S")
    x0 = res[0][0]
    x1 = res[1][0]
    positions = set()
    positions.add((x0, x1))
    i = 0
    nums = {}
    while i < num:
        new_set = set()
        for x0, x1 in positions:
            for dx0, dx1 in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x0n = x0 + dx0
                x1n = x1 + dx1
                if array[x0n % N, x1n % M] in [".", "S"]:
                    new_set.add((x0n, x1n))
        i += 1
        positions = new_set
        nums[i] = len(positions)
    if dump:
        with open(os.path.join(THISDIR, "out.pickle"), "wb") as fp:
            pickle.dump(nums, fp)
    return len(positions)


if __name__ == "__main__":
    with open(os.path.join(THISDIR, "input.txt")) as fp:
        lines = fp.readlines()

    lines = [list(v.strip()) for v in lines]
    arr = np.array(lines, dtype=np.str_)
    print(f"Part 1: {run(arr, num=64)}")
    run(arr, num=1000, dump=True)
    print("Part 2 was solved in a notebook, so go look there...")
