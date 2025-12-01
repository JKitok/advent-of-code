import os
import copy


def parse(line):
    num = int(line.strip("LR"))
    factor = 1
    if line.startswith("L"):
        factor = -1
    return factor, num


def part1(lines):
    cnt = 0
    dial = 50
    for line in lines:
        factor, num = parse(line)
        dial = (dial + factor * num) % 100
        if dial == 0:
            cnt += 1
    return cnt


def part2(lines):
    cnt = 0
    dial = 50
    for line in lines:
        assert 0 <= dial <= 99
        old_dial = dial
        factor, num = parse(line)
        if factor < 0:
            # Left rotation
            dial -= num
            while dial < 0:
                if old_dial != 0 or dial <= -100:
                    cnt += 1
                dial += 100
            if old_dial != 0 and dial == 0:
                cnt += 1
        else:
            # Right rotation
            dial += num
            while dial > 99:
                cnt += 1
                dial -= 100

    return cnt


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    print(f"Part 1: {part1(copy.deepcopy(lines))}")
    print(f"Part 2: {part2(copy.deepcopy(lines))}")
