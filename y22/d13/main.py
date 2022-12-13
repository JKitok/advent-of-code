import os
import functools


def list_if_not(v):
    return v if isinstance(v, list) else [v]


def compare_lists(a, b):
    a = iter(a)
    b = iter(b)
    while True:
        left = next(a, None)
        right = next(b, None)
        if left is None and right is None:
            return 0
        elif left is None:
            return -1
        elif right is None:
            return 1
        elif isinstance(left, list) or isinstance(right, list):
            v = compare_lists(list_if_not(left), list_if_not(right))
            if v != 0:
                return v
        else:
            assert isinstance(left, int) and isinstance(right, int)
            if left < right:
                return -1
            elif left > right:
                return 1


def part1(A, B):
    sum_ = 0
    for i, (a, b) in enumerate(zip(A, B)):
        sum_ += i + 1 if compare_lists(a, b) == -1 else 0
    return sum_


def part2(A, B):
    all_ = A + B
    div1 = [[2]]
    div2 = [[6]]
    all_.extend([[], div1, div2])
    all_ = sorted(all_, key=functools.cmp_to_key(compare_lists))
    return all_.index(div1) * all_.index(div2)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    A = [eval(v) for v in lines[::3]]
    B = [eval(v) for v in lines[1::3]]

    print(f"Part 1: {part1(A, B)}")
    print(f"Part 2: {part2(A, B)}")
