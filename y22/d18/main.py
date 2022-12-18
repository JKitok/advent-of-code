import os
from queue import Queue
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)


def run(data):
    directions = [
        Point(0, 0, 1),
        Point(0, 0, -1),
        Point(0, 1, 0),
        Point(0, -1, 0),
        Point(1, 0, 0),
        Point(-1, 0, 0),
    ]

    max_x = max(d.x for d in data) + 2
    max_y = max(d.y for d in data) + 2
    max_z = max(d.z for d in data) + 2

    min_x = min(d.x for d in data) - 2
    min_y = min(d.y for d in data) - 2
    min_z = min(d.z for d in data) - 2

    outside = set()
    to_check = Queue()
    to_check.put(Point(0, 0, 0))
    outside.add(Point(0, 0, 0))
    while not to_check.empty():
        pos = to_check.get()
        for dir in directions:
            next_ = pos + dir
            if (
                min_x < next_.x < max_x
                and min_y < next_.y < max_y
                and min_z < next_.z < max_z
                and next_ not in outside
                and next_ not in data
            ):
                to_check.put(next_)
                outside.add(next_)

    cnt1 = 0
    cnt2 = 0
    for p in data:
        for dir in directions:
            if p + dir not in data:
                cnt1 += 1
            if p + dir in outside:
                cnt2 += 1

    return cnt1, cnt2


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    data = [Point(*map(int, v.split(","))) for v in lines]
    p1, p2 = run(data)
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
