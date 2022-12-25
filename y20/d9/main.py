import os
import itertools


def get_sums(numbers):
    return


def part1(numbers, N=25):
    saved = []
    for i in range(N, len(numbers)):
        sums = [v1 + v2 for (v1, v2) in itertools.combinations(numbers[i - N : i], 2)]
        if numbers[i] not in sums:
            saved.append(numbers[i])
    return saved[0]


def part2(numbers, N):
    for L in range(2, len(numbers)):
        for i in range(L, len(numbers)):
            if sum(numbers[i - L : L]) == N:
                return min(numbers[i - L : L]) + max(numbers[i - L : L])


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    numbers = [int(v) for v in lines]

    res = part1(numbers)
    print(f"Part 1: {res}")
    print(f"Part 2: {part2(numbers, res)}")
