import os
import re
import math
import itertools


def to_list(string):
    chars = "[],"
    idx = 0
    splitted = []
    while idx < len(string):
        if string[idx] in chars:
            splitted.append(string[idx])
            idx += 1
        else:
            ni = next((i for i in range(idx, len(string)) if string[i] in chars))
            splitted.append(string[idx:ni])
            idx = ni
    return splitted


def explode(splitted):
    last = None
    depth = 0
    idx = 0
    while idx < len(splitted):
        if splitted[idx] == "[":
            depth += 1
        elif splitted[idx] == "]":
            depth -= 1
        if depth > 4:
            if last is not None:
                splitted[last] = str(int(splitted[last]) + int(splitted[idx + 1]))
            for i in range(idx + 5, len(splitted)):
                if splitted[i].isdigit():
                    splitted[i] = str(int(splitted[i]) + int(splitted[idx + 3]))
                    break
            splitted = splitted[:idx] + ["0"] + splitted[idx + 5 :]
            return splitted, False
        elif splitted[idx].isdigit():
            last = idx
        idx += 1
    return splitted, True


def split(splitted):
    idx = 0
    while idx < len(splitted):
        if splitted[idx].isdigit():
            val = int(splitted[idx])
            if val > 9:
                content = [
                    "[",
                    str(int(val // 2)),
                    ",",
                    str(int(math.ceil(val / 2))),
                    "]",
                ]
                splitted = splitted[:idx] + content + splitted[idx + 1 :]
                return splitted, False
        idx += 1
    return splitted, True


def reduce(string):
    splitted = to_list(string)
    done = False
    while not done:
        splitted, done = explode(splitted)
        if done:
            splitted, done = split(splitted)
    return "".join(splitted)


def test_reduce():
    assert reduce("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]"
    assert reduce("[7,[6,[5,[4,[3,2]]]]]") == "[7,[6,[5,[7,0]]]]"
    assert reduce("[[6,[5,[4,[3,2]]]],1]") == "[[6,[5,[7,0]]],3]"
    assert (
        reduce("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
        == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    )


def magnitude(number):
    while groups := re.findall(r"(\[\d+,\d+\])+", number):
        for g in groups:
            l, r = re.match(r"^\[(\d+),(\d+)\]$", g).groups()
            number = number.replace(g, str(3 * int(l) + 2 * int(r)))
    return int(number)


def test_magnitude():
    assert magnitude("[9,1]") == 29
    assert magnitude("[[1,2],[[3,4],5]]") == 143
    assert magnitude("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]") == 1384
    assert magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]") == 3488


def add(string1, string2):
    new = f"[{string1},{string2}]"
    return reduce(new)


def part1(lines):
    number = lines[0]
    for num in lines[1:]:
        number = add(number, num)
    return magnitude(number)


def part2(lines):
    a = max(magnitude(add(a, b)) for a, b in itertools.combinations(lines, 2))
    b = max(magnitude(add(b, a)) for a, b in itertools.combinations(lines, 2))
    return a if a > b else b


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    lines = [l for l in lines if l]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
