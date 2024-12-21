import os
import itertools
import functools


def get_numpad_coordinate(v):
    if v == "0":
        return (1, 0)
    elif v == "A":
        return (2, 0)
    else:
        x = (int(v) - 1) % 3
        y = 1 + (int(v) - 1) // 3
        return x, y


def get_directional_coordinate(v):
    return {"<": (0, 0), "v": (1, 0), ">": (2, 0), "^": (1, 1), "A": (2, 1)}[v]


def create_directional_sequence_from_coords(dx, dy, x_first=True):
    x_sign = "<" if dx < 0 else ">"
    y_sign = "v" if dy < 0 else "^"
    if x_first:
        return x_sign * abs(dx) + y_sign * abs(dy)
    else:
        return y_sign * abs(dy) + x_sign * abs(dx)


def generate_numpad_sequences(numpad_start, numpad_end):
    x1, y1 = get_numpad_coordinate(numpad_start)
    x2, y2 = get_numpad_coordinate(numpad_end)
    sequence = create_directional_sequence_from_coords(x2 - x1, y2 - y1)

    def check_legal_sequence(seq):
        x, y = (x1, y1)
        for v in seq:
            if v == "<":
                x -= 1
            elif v == ">":
                x += 1
            elif v == "^":
                y += 1
            elif v == "v":
                y -= 1
            if x < 0 or x > 2 or y < 0 or y > 3:
                return False
            elif (x, y) == (0, 0):
                return False
        return True

    for seq in set(itertools.permutations(sequence)):
        # Check that we don't pass any restricted areas
        if not check_legal_sequence(seq):
            continue
        yield (*seq, "A")


def generate_directional_sequences(dir_start, dir_end):
    x1, y1 = get_directional_coordinate(dir_start)
    x2, y2 = get_directional_coordinate(dir_end)
    # It only makes sense to press first all x-movements followed by y-movements, or vice versa
    sequence1 = create_directional_sequence_from_coords(x2 - x1, y2 - y1, x_first=True)
    sequence2 = create_directional_sequence_from_coords(x2 - x1, y2 - y1, x_first=False)

    def check_legal_sequence(seq):
        x, y = (x1, y1)
        for v in seq:
            if v == "<":
                x -= 1
            elif v == ">":
                x += 1
            elif v == "^":
                y += 1
            elif v == "v":
                y -= 1
            if x < 0 or x > 2 or y < 0 or y > 1:
                return False
            elif (x, y) == (0, 1):
                return False
        return True

    for seq in set([sequence1, sequence2]):
        if not check_legal_sequence(seq):
            continue
        yield (*seq, "A")


@functools.cache
def best_directional_move(dir_start, dir_end):
    return "".join(
        sorted(
            generate_directional_sequences(dir_start, dir_end),
            key=lambda x: len(x),
        )[0]
    )


def get_robot_sequence(dir_sequence):
    start = "A"
    seq = ""
    for v in dir_sequence:
        seq += best_directional_move(start, v)
        start = v
    return seq


@functools.cache
def best_numpad_move(numpad_start, numpad_end, n):
    best_len = 1_000_000_000_000
    for numpad_seq in generate_numpad_sequences(numpad_start, numpad_end):
        seq = numpad_seq
        for i in range(n):
            seq = get_robot_sequence(seq)
        if best_len > len(seq):
            best_len = len(seq)
    return best_len


def run(lines, n):
    sum_ = 0
    for line in lines:
        num_moves = 0
        start = "A"
        for v in line:
            num_moves += best_numpad_move(start, v, n)
            start = v
        sum_ += num_moves * int(line.replace("A", ""), base=10)
    return sum_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    print(f"Part 1: {run(lines, n=2)}")
    print(f"Part 2: {run(lines, n=25)}")
