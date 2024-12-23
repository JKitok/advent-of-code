import os
from itertools import combinations
from collections import defaultdict
import networkx as nx

def part1(lines):
    connections = defaultdict(list)
    for line in lines:
        a, b = line.split("-")
        connections[a].append(b)
        connections[b].append(a)

    groups = set()
    
    for node, conns in connections.items():
        for a, b in combinations(conns, 2):
            if not any((v.startswith("t") for v in (node, a, b))):
                continue
            if b in connections[a]:
                groups.add(tuple(sorted((node, a, b))))

    return len(groups)
    


def part2(lines):
    G = nx.Graph()
    for line in lines:
        G.add_edge(*line.split("-"))
    cliques = list(nx.find_cliques(G))
    cliques.sort(key=lambda x: len(x), reverse=True)
    return ",".join(sorted(cliques[0]))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
