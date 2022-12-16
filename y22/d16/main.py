import os
import re
import functools
import copy


def parse(lines):
    rates = {}
    map_ = {}
    for line in lines:
        ret = re.match(
            "Valve ([A-Z]+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.+)",
            line,
        )
        name, rate, groups = ret.groups()
        rates[name] = int(rate)
        map_[name] = list(map(str.strip, groups.split(",")))

    return rates, map_


def shortest_path(map_, start, ends):
    cost = {k: 1_000_000_000 for k in map_.keys()}
    visited = set()
    cost[start] = 0
    current = start
    while any(v not in visited for v in ends):
        current = min((cost[v], v) for v in cost.keys() if v not in visited)[1]
        for potential in map_[current]:
            if potential not in visited:
                cost[potential] = min(cost[potential], cost[current] + 1)
        visited.add(current)

    return {v: cost[v] for v in ends}


def get_distance_map(rates, map_):
    all_positions = [k for (k, v) in rates.items() if v > 0]
    all_positions = sorted(all_positions)
    distances = {}
    start = "AA"
    while all_positions:
        costs = shortest_path(map_, start, all_positions)
        for end, cost in costs.items():
            distances[(start, end)] = cost
        start = all_positions.pop(0)
    return distances


def calculate_total_pressure(dict_, rates, T):
    return sum((T - v) * rates[k] for k, v in dict_.items())


def part1(rates, map_, distance_func, T=30):
    to_open = [v for (v, k) in rates.items() if k > 0]
    all_paths = {(frozenset(["AA"]), "AA"): {"AA": 0}}

    best = 0
    while all_paths:
        new_paths = {}
        # Calculate new paths
        for (visited, pos), when_on in all_paths.items():
            time = next(reversed(when_on.values()))
            new_positions = [n for n in to_open if n not in when_on.keys()]
            if new_positions:
                for next_ in new_positions:
                    distance = distance_func(pos, next_)
                    t_open = time + distance + 1
                    if t_open <= T:
                        new_visited = frozenset((*visited, next_))
                        if (new_visited, next_,) not in new_paths.keys() or next(
                            reversed(new_paths[(new_visited, next_)].values())
                        ) > t_open:
                            new_when_on = copy.deepcopy(when_on)
                            new_when_on[next_] = t_open
                            new_paths[(new_visited, next_)] = new_when_on
                    else:
                        best = max(best, calculate_total_pressure(when_on, rates, T))
            else:
                best = max(best, calculate_total_pressure(when_on, rates, T))
        all_paths = new_paths
        print(len(new_paths))

    return best


def part2(rates, map_):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    rates, map_ = parse(lines)
    distance_map = get_distance_map(rates, map_)

    def get_distance(a, b):
        if b < a:
            a, b = b, a
        return distance_map[(a, b)]

    print(f"Part 1: {part1(rates, map_, get_distance)}")
    # print(f"Part 2: {part2(rates, map_)}")
