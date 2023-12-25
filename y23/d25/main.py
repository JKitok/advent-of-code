import os
import math

import networkx as nx


def part1(lines):
    g = nx.Graph()
    for line in lines:
        v, list_ = line.split(": ")
        for adj in list_.split(" "):
            g.add_edge(v, adj)

    g.remove_edges_from(nx.minimum_edge_cut(g))
    return math.prod((len(c) for c in nx.connected_components(g)))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]

    print(f"Part 1: {part1(lines)}")
