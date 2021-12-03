import os
import copy
from collections import Counter


def part1(lines):
    num1 = ""
    num2 = ""
    for i in range(len(lines[0])):
        c = Counter((v[i] for v in lines))
        (mc, _), (lc, _) = c.most_common()
        num1 += mc
        num2 += lc

    print(int(num1, 2) * int(num2, 2))


def part2(lines):
    o2 = copy.deepcopy(lines)
    co2 = copy.deepcopy(lines)

    for i in range(len(lines[0])):
        if len(o2) > 1:
            mctup, lctup = Counter((v[i] for v in o2)).most_common()
            mc = "1" if mctup[1] == lctup[1] else mctup[0]
            o2 = [v for v in o2 if v[i] == mc]

        if len(co2) > 1:
            mctup, lctup = Counter((v[i] for v in co2)).most_common()
            lc = "0" if mctup[1] == lctup[1] else lctup[0]
            co2 = [v for v in co2 if v[i] == lc]

    print(int(o2[0], 2) * int(co2[0], 2))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]

    part1(lines)
    part2(lines)
