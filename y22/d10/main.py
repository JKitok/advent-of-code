import os


def parse_changes(lines):
    cycle = 1
    changes = {1: 1}
    for line in lines:
        if line == "noop":
            cycle += 1
        elif line.startswith("addx"):
            _, num = line.split(" ")
            cycle += 2
            changes[cycle] = int(num)
    return changes


def part1(changes):
    ret = 0
    for i in [20, 60, 100, 140, 180, 220]:
        X = sum((v for (k, v) in changes.items() if k <= i))
        ret += i * X
    return ret


def part2(changes):
    cnt = 0
    drawing = ""
    for row in range(0, 6):
        for col in range(0, 40):
            cnt += 1
            X = sum((v for (k, v) in changes.items() if k <= cnt))
            if X - 1 <= col <= X + 1:
                drawing += "#"
            else:
                drawing += "."
        drawing += "\n"
    print(drawing)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    changes = parse_changes(lines)

    print(f"Part 1: {part1(changes)}")
    print(f"Part 2: {part2(changes)}")
