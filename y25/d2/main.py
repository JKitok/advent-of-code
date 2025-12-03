import os
import copy


def part1(ranges):
    sum_ = 0
    for start, stop in ranges:
        half = start[: len(start) // 2]
        if len(start) % 2 != 0:
            half = "1" + "0" * len(half)
        while int(half + half) <= int(stop):
            if int(half + half) >= int(start):
                sum_ += int(half + half)
            half = str(int(half) + 1)
    return sum_


def part2(ranges):
    sum_ = 0
    counted = set()
    for start, stop in ranges:
        possible_lengths = [v for v in range(len(start), len(stop) + 1)]
        for length in possible_lengths:
            for width in (w for w in range(1, len(stop) // 2 + 1) if length % w == 0):
                if length == possible_lengths[0]:
                    pattern = start[:width]
                else:
                    pattern = "1" + "0" * (width - 1)
                repeat = length // width
                while len(pattern) == width:
                    num = int(pattern * repeat)
                    if (
                        int(start) <= num <= int(stop)
                        and num not in counted
                        and num > 10
                    ):
                        sum_ += num
                        counted.add(num)
                    if num > int(stop):
                        break
                    pattern = str(int(pattern) + 1)
    return sum_


def parse(line):
    ranges = []
    for txt in line.split(","):
        start, stop = txt.split("-")
        ranges.append((start, stop))
    return ranges


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    ranges = parse(lines[0])
    print(f"Part 1: {part1(copy.deepcopy(ranges))}")
    print(f"Part 2: {part2(copy.deepcopy(ranges))}")
