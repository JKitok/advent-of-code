import os
import re


def getmap(map_, v):
    return map_[round(-v.imag)][round(v.real)]


def wrap_part_1(position, map_):
    if -position.imag >= len(map_):
        position = position.real
    elif position.imag > 0:
        position = position.real - 1j * (len(map_) - 1)

    if position.real >= len(map_[0]):
        position = 1j * position.imag
    elif position.real < 0:
        position = len(map_[0]) - 1 + 1j * position.imag
    return position


def wrap_part_2(position, direction):
    match (position.imag, position.real, direction):
        # fmt: off
        case (y, 49, -1) if -50 < y <= 0: return 0 + (-149 - y)*1j, 1
        case (1, x, 1j) if 50 <= x < 100: return 0 + (-150 - (x - 50))*1j, 1
        case (1, x, 1j) if 100 <= x < 150: return (x - 100) - 199j, 1j
        case (y, 150, 1) if -50 < y <= 0: return 99 + (-149 - y) * 1j, -1
        case (-50, x, -1j) if 100 <= x < 150: return 99 - (x - 100 + 50) * 1j, -1
        case (y, 100, 1) if -100 < y <= -50: return 100 - (y + 50) - 49j, 1j
        case (y, 100, 1) if -150 < y <= -100: return 149 + (-149 - y) * 1j, -1
        case (-150, x, -1j) if 50 <= x < 100: return 49 - (150 + (x - 50)) * 1j, -1
        case (y, 50, 1) if -200 < y <= -150: return  50 + (-y - 150) -149j, 1j
        case (-200, x, -1j) if 0 <= x < 50: return  100 + x, -1j
        case (y, -1, -1) if -200 < y <= -150: return  50 + (-y - 150), -1j
        case (y, -1, -1) if -150 < y <= -100: return  50 + (-y - 149) * 1j, 1
        case (-99, x, 1j) if 0 <= x < 50: return  50 - (50 + x) * 1j, 1
        case (y, 49, -1) if -100 < y <= -50: return -y - 50 - 100j, -1j
        case _: assert getmap(map_, position) != " "; return position, direction
        # fmt: on


def test_wrap_part_2():
    # Case 1
    assert wrap_part_2(49 - 0j, -1) == (-149j, 1)
    assert wrap_part_2(49 - 49j, -1) == (-100j, 1)
    # Case 2
    assert wrap_part_2(50 + 1j, 1j) == (-150j, 1)
    assert wrap_part_2(99 + 1j, 1j) == (-199j, 1)
    # Case 3
    assert wrap_part_2(100 + 1j, 1j) == (0 + -199j, 1j)
    assert wrap_part_2(149 + 1j, 1j) == (49 + -199j, 1j)
    # Case 4
    assert wrap_part_2(150 - 0j, 1) == (99 - 149j, -1)
    assert wrap_part_2(150 - 49j, 1) == (99 - 100j, -1)
    # Case 5
    assert wrap_part_2(100 - 50j, -1j) == (99 - 50j, -1)
    assert wrap_part_2(149 - 50j, -1j) == (99 - 99j, -1)
    # case 6
    assert wrap_part_2(100 - 50j, 1) == (100 - 49j, 1j)
    assert wrap_part_2(100 - 99j, 1) == (149 - 49j, 1j)
    # Case 7
    assert wrap_part_2(100 - 100j, 1) == (149 - 49j, -1)
    assert wrap_part_2(100 - 149j, 1) == (149 - 0j, -1)
    # Case 8
    assert wrap_part_2(50 - 150j, -1j) == (49 - 150j, -1)
    assert wrap_part_2(99 - 150j, -1j) == (49 - 199j, -1)
    # Case 9
    assert wrap_part_2(50 - 150j, 1) == (50 - 149j, 1j)
    assert wrap_part_2(50 - 199j, 1) == (99 - 149j, 1j)
    # Case 10
    assert wrap_part_2(0 - 200j, -1j) == (100, -1j)
    assert wrap_part_2(49 - 200j, -1j) == (149, -1j)
    # Case 11
    assert wrap_part_2(-1 - 150j, -1) == (50, -1j)
    assert wrap_part_2(-1 - 199j, -1) == (99, -1j)
    # Case 12
    assert wrap_part_2(-1 - 100j, -1) == (50 - 49j, 1)
    assert wrap_part_2(-1 - 149j, -1) == (50, 1)
    # Case 13
    assert wrap_part_2(-99j, 1j) == (50 - 50j, 1)
    assert wrap_part_2(49 - 99j, 1j) == (50 - 99j, 1)
    # Case 14
    assert wrap_part_2(49 - 50j, -1) == (-100j, -1j)
    assert wrap_part_2(49 - 99j, -1) == (49 - 100j, -1j)


def move(position, v, map_, part):
    position += v
    if part == 1:
        return wrap_part_1(position, map_), v
    else:
        return wrap_part_2(position, v)


def find_next(map_, direction, position, part):
    while True:
        position, direction = move(position, direction, map_, part)
        if getmap(map_, position) != " ":
            return position, direction


def run(map_, instructions, part):
    direction = 1
    position, direction = find_next(map_, direction, 0, 1)
    for instr in instructions:
        if instr == "L":
            direction *= 1j
        elif instr == "R":
            direction *= -1j
        else:
            num = int(instr)
            for _ in range(num):
                new, new_direction = move(position, direction, map_, part)
                if getmap(map_, new) == " ":
                    new, direction = find_next(map_, direction, new, part)
                if getmap(map_, new) == ".":
                    position = new
                    direction = new_direction
                elif getmap(map_, new) == "#":
                    break
    score_map = {1: 0, -1j: 1, -1: 2, 1j: 3}
    return int(
        1000 * (-position.imag + 1) + 4 * (position.real + 1) + score_map[direction]
    )


if __name__ == "__main__":
    test_wrap_part_2()
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    *map_, _, instructions = [v.rstrip("\n") for v in lines]
    max_ = max(len(v) for v in map_)
    map_ = [v.ljust(max_) for v in map_]
    instructions = re.findall("(\d+|L|R)", instructions)

    print(f"Part 1: {run(map_, instructions, 1)}")
    print(f"Part 2: {run(map_, instructions, 2)}")
