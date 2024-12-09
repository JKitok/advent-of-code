import os
import itertools
from tqdm.contrib import tzip


def parse(lines):
    test_values, numbers = [], []
    for line in lines:
        test, rest = map(str.strip, line.split(":"))
        test_values.append(int(test))
        numbers.append([*map(int, rest.split())])
    return test_values, numbers


def run(test_values, numbers, operators):
    sum_ = 0
    for test, nums in tzip(test_values, numbers):
        for operations in itertools.product(operators, repeat=len(nums) - 1):
            start = nums[0]
            for op, n in zip(operations, nums[1:]):
                if start > test:
                    break
                if op == "*":
                    start *= n
                elif op == "+":
                    start += n
                elif op == "||":
                    start = int(str(start) + str(n))
                else:
                    raise ValueError(op)

            if start == test:
                sum_ += test
                break
    return sum_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    test_values, numbers = parse(lines)
    print(f"Part 1: {run(test_values, numbers, operators=['+', '*'])}")
    print(f"Part 2: {run(test_values, numbers, operators=['+', '*', '||'])}")
