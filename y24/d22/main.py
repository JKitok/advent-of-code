import os
import copy
from tqdm import tqdm


def mix(number, secret):
    return number ^ secret


def prune(number):
    return number % 16777216


def secret(number):
    v = 64 * number
    number = mix(v, number)
    number = prune(number)

    v = number // 32
    number = mix(v, number)
    number = prune(number)

    v = number * 2048
    number = mix(v, number)
    return prune(number)


def part1(lines):
    total = 0
    for line in tqdm(lines):
        num = int(line)
        for i in range(2000):
            num = secret(num)
        total += num
    return total


def part2(lines):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    print(f"Part 1: {part1(copy.deepcopy(lines))}")
    print(f"Part 2: {part2(copy.deepcopy(lines))}")
