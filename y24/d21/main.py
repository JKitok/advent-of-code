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
        yield "".join((*seq, "A"))


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
        yield "".join((*seq, "A"))


@functools.cache
def get_num_movements(seq, level, numpad=True):
    res = 0
    seq = "A" + seq
    for u, v in itertools.pairwise(seq):
        if numpad:
            paths = [*generate_numpad_sequences(u, v)]
        else:
            paths = [*generate_directional_sequences(u, v)]
        if level == 0:
            res += min(map(len, paths))
        else:
            res += min(get_num_movements(path, level - 1, numpad=False) for path in paths)
    return res


def run(lines, n):
    total = 0
    for line in lines:
        total += get_num_movements(line, n) * int(line.replace("A", ""))
    return total


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    print(f"Part 1: {run(lines, n=2)}")
    print(f"Part 2: {run(lines, n=25)}")
