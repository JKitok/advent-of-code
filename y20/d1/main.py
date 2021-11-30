import os

THISDIR = os.path.dirname(__file__)


def part1(lines):
    for i, value1 in enumerate(lines):
        for value2 in lines[i + 1 :]:
            if value1 + value2 == 2020:
                print(f"Answer: {value1 * value2}")


def part2(lines):
    for i, value1 in enumerate(lines):
        for j, value2 in enumerate(lines[i + 1 :]):
            for value3 in lines[i + j + 1 :]:
                if value1 + value2 + value3 == 2020:
                    print(f"Answer: {value1 * value2 * value3}")


def main():
    with open(os.path.join(THISDIR, "input.txt")) as fp:
        lines = fp.readlines()

    lines = [int(val.strip()) for val in lines]
    part1(lines)
    part2(lines)


if __name__ == "__main__":
    main()
