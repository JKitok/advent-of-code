import os
from collections import defaultdict


def run(line, N):
    values = line.split()
    stones = defaultdict(int)
    for v in values:
        stones[int(v)] += 1
    for i in range(N):
        new_stones = defaultdict(int)
        for v, num in stones.items():
            if v == 0:
                new_stones[1] += num
            elif len(as_string := str(v)) % 2 == 0:
                size = len(as_string) // 2
                new_stones[int(as_string[:size])] += num
                new_stones[int(as_string[size:])] += num
            else:
                new_stones[v * 2024] += num
        stones = new_stones

    return sum(stones.values())


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    print(f"Part 1: {run(lines[0], N=25)}")
    print(f"Part 2: {run(lines[0], N=75)}")
