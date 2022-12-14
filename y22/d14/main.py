import os
import copy


def print_(area):
    xmin = min(v[0] for v in area)
    xmax = max(v[0] for v in area)
    ymin = min(v[1] for v in area)
    ymax = max(v[1] for v in area)
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            print(area.get((x, y), "."), end="")
        print("")


def parse_rock(lines):
    area = dict()
    for line in lines:
        vertices = line.split("->")
        for start, stop in zip(vertices[0:-1], vertices[1:]):
            x1, y1 = map(int, start.split(","))
            x2, y2 = map(int, stop.split(","))
            if x2 < x1:
                x1, x2 = x2, x1
            if y2 < y1:
                y1, y2 = y2, y1
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    area[x, y] = "#"
    return area


def calculate_falling_sand(area, floor=None):
    ymax = max(v[1] for v in area.keys())

    if floor is None:

        def in_area(x, y):
            return (x, y) in area

    else:
        ymax += floor

        def in_area(x, y):
            if y == ymax:
                return True
            else:
                return (x, y) in area

    xs, ys = 500, 0
    filled = False
    x, y = None, None
    while not in_area(xs, ys) and (y is None or y < ymax + 2):
        if x is None:
            x, y = xs, ys
        if not in_area(x, y + 1):
            x, y = x, y + 1
        elif not in_area(x - 1, y + 1):
            x, y = x - 1, y + 1
        elif not in_area(x + 1, y + 1):
            x, y = x + 1, y + 1
        else:
            area[(x, y)] = "o"
            x, y = None, None
    return sum((v == "o" for v in area.values()))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    area = parse_rock(lines)
    print(f"Part 1: {calculate_falling_sand(copy.deepcopy(area))}")
    print(f"Part 2: {calculate_falling_sand(copy.deepcopy(area), floor=2)}")
