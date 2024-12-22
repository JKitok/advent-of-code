import os
from tqdm import tqdm
import functools

def run(lines):
    types_list, _, *towels = lines
    types = tuple([*map(str.strip, types_list.split(","))])
    ways = []
    for towel in tqdm(towels):
        ways.append(ways_to_construct(towel, types))

    print(f"Part 1: {sum((1 for v in ways if v > 0))}")
    print(f"Part 2: {sum((v for v in ways))}")

@functools.cache
def ways_to_construct(towel, types):
    num_ways = 0

    for t in types:
        if t == towel:
            num_ways += 1
        if towel.startswith(t):
            num_ways += ways_to_construct(towel.replace(t, "", 1), types)
    return num_ways


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    run(lines)
