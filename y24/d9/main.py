import os
import copy
from collections import defaultdict
import itertools


def run(lines, resonance=False):
    N = len(lines[0])
    M = len(lines)
    antennas = defaultdict(lambda: [])
    anti_nodes = defaultdict(lambda: [])
    for i, line in enumerate(lines):
        for j, v in enumerate(line):
            if v != ".":
                antennas[v].append((i, j))

    for frequency, locations in antennas.items():
        for p1, p2 in itertools.combinations(locations, 2):
            dn = p2[0] - p1[0]
            dm = p2[1] - p1[1]

            for point, direction in ((p2, 1), (p1, -1)):
                if resonance:
                    anti_nodes[point].append(frequency)
                factor = 1
                while True:
                    node = (
                        point[0] + direction * factor * dn,
                        point[1] + direction * factor * dm,
                    )
                    if 0 <= node[0] < N and 0 <= node[1] < M:
                        anti_nodes[node].append(frequency)
                        factor += 1
                        if not resonance:
                            break
                    else:
                        break

    return len(anti_nodes.items())


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    print(f"Part 1: {run(copy.deepcopy(lines), resonance=False)}")
    print(f"Part 2: {run(copy.deepcopy(lines), resonance=True)}")
