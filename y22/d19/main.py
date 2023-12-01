import os
import re
import enum
from dataclasses import dataclass, astuple
from queue import Queue
import math


class Type(enum.Enum):
    ORE = 1
    CLAY = 2
    OBS = 3
    GEODE = 4


@dataclass
class BluePrint:
    ore: tuple[int, int, int, int]
    clay: tuple[int, int, int, int]
    obs: tuple[int, int, int, int]
    geode: tuple[int, int, int, int]


def parse(lines):
    bps = []
    for line in lines:
        ints = list(map(int, re.findall("\d+", line)))
        assert len(ints) == 7
        bps.append(
            BluePrint(
                (ints[1], 0, 0, 0),
                (ints[2], 0, 0, 0),
                (ints[3], ints[4], 0, 0),
                (ints[5], 0, ints[6], 0),
            )
        )
    return bps


@dataclass(frozen=True)
class State:
    t: int = 0
    ores: tuple[int] = (0, 0, 0, 0)
    robots: tuple[int] = (1, 0, 0, 0)
    build_next: Type = None


def get_cost(bp, t):
    return {
        Type.ORE: bp.ore,
        Type.CLAY: bp.clay,
        Type.OBS: bp.obs,
        Type.GEODE: bp.geode,
    }[t]


def build(t: Type, bp, ores):
    cost = get_cost(bp, t)
    return tuple((o - c for (o, c) in zip(ores, cost)))


def get_possible_next(bp, robots):
    max_ore_needed = max((bp.ore[0], bp.clay[0], bp.obs[0], bp.geode[0]))

    ret = []
    if robots[0] < max_ore_needed:
        ret.append(Type.ORE)
    if robots[1] < bp.obs[1]:
        ret.append(Type.CLAY)
    if robots[1] > 0:
        ret.append(Type.OBS)
    if robots[2] > 0:
        ret.append(Type.GEODE)
    return ret


def time_for_build(bp: BluePrint, type_: Type, robots, ores, t):
    cost = get_cost(bp, type_)
    left = tuple(
        0 if c == 0 else math.ceil((c - o) / r) for (c, o, r) in zip(cost, ores, robots)
    )
    return t + max(left)


def run(bp, T):
    results = set()
    queue = Queue()
    queue.put(State(build_next=Type.ORE), State(build_next=Type.CLAY))
    cache = {}

    while not queue.empty():
        t, ores, robots, build_next = astuple(queue.get())
        t_b = time_for_build(bp, build_next, robots, ores, t)
        key = (robots, build_next)
        best = cache.get(key, (0, T + 1))
        if best[0] >= ores[-1] and best[1] < t_b:
            # Ignore branch
            continue

        # Count until build and build
        ores = tuple((o + (t_b - t) * r for (o, r) in zip(ores, robots)))
        t = t_b + 1
        ores = build(build_next, bp, ores)
        robots = tuple(r + (build_next == e) for r, e in zip(robots, Type))

        for v in get_possible_next(bp, robots):
            t_b = time_for_build(bp, v, robots, ores, t)

            if t_b > T:
                # Count up ores and store
                ores = tuple((o + (T - t) * r for (o, r) in zip(ores, robots)))
                results.add(State(t, ores, robots, v))
            else:
                # Generate next builds and store
                key = (robots, v)
                best = cache.get(key, (0, T + 1))
                if ores[-1] >= best[0] and t_b <= best[1]:
                    cache[key] = (ores[-1], t_b)
                    state = State(t, ores, robots, v)
                    queue.put(state)
                    break

    results = sorted(results, key=lambda x: x.ores[-1], reverse=True)
    return results[0].ores[-1]


def part1(blueprints):
    all_max = [0]
    for i, bp in enumerate(blueprints):
        res = run(bp, T=24)
        print(f"{i}/{len(blueprints)}", end="\r")
        all_max.append(res)
    return sum(i * v for (i, v) in enumerate(all_max))


def part2(blueprints):
    prod_ = 1
    for i, bp in enumerate(blueprints[:3]):
        res = run(bp, T=32)
        print(f"{i}/3", end="\r")
        prod_ *= res
    return prod_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "example.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    blueprints = parse(lines)
    print(f"Part 1: {part1(blueprints)}")
    print(f"Part 2: {part2(blueprints)}")
