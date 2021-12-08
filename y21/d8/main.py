import os
import re

from dataclasses import dataclass

import numpy as np


def part1(input_, output):
    count = 0
    for line in output:
        numbers = line.split(" ")
        count += len([n for n in numbers if len(n) in [2, 3, 4, 7]])
    return count


def decode_line(line):
    numbers = line.split(" ")
    numbers = [sorted(v) for v in numbers]
    n1 = next((n for n in numbers if len(n) == 2))
    n7 = next((n for n in numbers if len(n) == 3))
    n4 = next((n for n in numbers if len(n) == 4))
    n8 = next((n for n in numbers if len(n) == 7))
    # Find right-most segments, we know which they are since they appear in n1
    # And the top-right segment appears in 8 out of 10 digits (and the other appears
    # in 9 out of 10 digits)
    if sum([n1[0] in n for n in numbers]) == 8:
        tr, br = n1[0], n1[1]
    else:
        br, tr = n1[0], n1[1]

    # 0, 6, 9 all have six segments active, and both 0 and 9 have tr active
    n6 = next((n for n in numbers if len(n) == 6 and tr not in n))
    # 2, 3, 5 all have five segments active, and both 2 and 3 have tr active
    n5 = next((n for n in numbers if len(n) == 5 and tr not in n))
    # Between 2 and 3, br is not active for 2. Once we know 2 and 5, 3 can be deduced
    # as the last number with 5 segments active
    n2 = next((n for n in numbers if len(n) == 5 and br not in n and n != n5))
    n3 = next((n for n in numbers if len(n) == 5 and n != n2 and n != n5))

    # Find mid-segment by looking at the two segments active for 4 but not 1,
    # and identifying them by looking for which one does not appear in 2.
    mid_or_tr = [v for v in n4 if v not in n1]
    if mid_or_tr[0] not in n2:
        tr, mid = mid_or_tr
    else:
        mid, tr = mid_or_tr

    # Use mid-segment to identify which of the two remaining numbers is 0 and
    # 9 respectively.
    n0 = next((n for n in numbers if len(n) == 6 and mid not in n and n != n6))
    n9 = next((n for n in numbers if len(n) == 6 and n != n0 and n != n6))

    return [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9]


def part2(input_, output):
    sum_ = 0
    for in_, out in zip(input_, output):
        out_arr = [sorted(v) for v in out.split(" ")]
        translation = decode_line(in_)
        out_num = int("".join([f"{translation.index(v)}" for v in out_arr]))
        sum_ += out_num
    return sum_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]

    input_ = [line.split("|")[0].strip() for line in lines]
    output = [line.split("|")[1].strip() for line in lines]

    print(f"Part 1: {part1(input_, output)}")
    print(f"Part 2: {part2(input_, output)}")
