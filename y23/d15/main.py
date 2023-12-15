import os

from collections import defaultdict


def HASH(seq):
    v = 0
    for c in seq:
        v += ord(c)
        v *= 17
        v %= 256
    return v


def part1(line):
    sum_ = 0
    for seq in line.split(","):
        sum_ += HASH(seq)
    return sum_


def part2(line):
    boxes = defaultdict(lambda: {})
    for seq in line.split(","):
        if "=" in seq:
            label, focal_length = seq.split("=")
            boxes[HASH(label)][label] = int(focal_length)
        elif "-" in seq:
            label, _ = seq.split("-")
            if label in boxes[HASH(label)]:
                del boxes[HASH(label)][label]

    sum_ = 0
    for box, lenses in boxes.items():
        for i, (_, focal_length) in enumerate(lenses.items()):
            sum_ += (box + 1) * (i + 1) * focal_length
    return sum_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    line = lines[0]

    print(f"Part 1: {part1(line)}")
    print(f"Part 2: {part2(line)}")
