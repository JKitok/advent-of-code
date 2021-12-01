import os

import numpy as np


def num_increase(arr):
    return np.sum(np.diff(np.array(arr)) > 0)


def num_increase_three_sum(values):
    three_sum = values[:-2] + values[1:-1] + values[2:]
    return num_increase(three_sum)


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    values = np.array([int(val.strip()) for val in lines])
    p1 = num_increase(values)
    print(f"Part 1: {p1}")
    p2 = num_increase_three_sum(values)
    print(f"Part 2: {p2}")


def test_num_increase():
    assert num_increase([1, 2, 3]) == 2
    assert num_increase([1, 2, 1]) == 1


def test_three_sum_example():
    # Run test from question description
    array = np.array([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
    assert num_increase_three_sum(array) == 5


if __name__ == "__main__":
    main()
