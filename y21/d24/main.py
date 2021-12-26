import os
from collections import defaultdict


def func(val, z, v1, v2, v3):
    # When v1 == 1, v2 > 10 is always true. Therefore, x > 10 != val after first
    # line and = 1 after second line.
    # When v1 == 26, x is either positive or negative so we can have x = 1 or
    # x = 0.
    x = z % 26 + v2
    x = 1 if x != val else 0
    # 7 times, we divide by 26, and 7 times this is no-op.
    z //= v1
    # The 7 times v1 == 1, we always multiply by 26 below here.
    # The 7 times v1 == 27, we either multiply by 26 or 1.
    y = 25 * x + 1
    z *= y
    # Here, we have either
    y = val + v3
    y *= x
    # Here, we add a positive value when x is 1, and 0 otherwise.
    z += y
    # In summary, we never multiply z with a negative value, and we multiply it
    # with 26 7 times. This means that we need to divide it by exactly 7 times
    # (i.e. when v1 is 26).
    return z


def find_(all_v1, all_v2, all_v3):
    cache = defaultdict(list)
    cache[0].append("")

    # The maximum value can be calculated by keeping track of the number of available
    # v1 == 26 that are left after each step (for the first time, there are 7
    # of them). This makes the search space significantly smaller.
    max_z = 26 ** 7

    for n, (v1, v2, v3) in enumerate(zip(all_v1, all_v2, all_v3)):
        new_cache = defaultdict(list)
        for z, values in cache.items():
            for i in range(1, 10):
                new_z = func(i, z, int(v1), int(v2), int(v3))
                if new_z < max_z:
                    new_cache[new_z].extend((v + str(i) for v in values))
        cache = new_cache
        max_z = max_z // int(v1)

        print(n, len(cache))

    min_, max_ = 1e15, 0
    for z, values in cache.items():
        if z == 0:
            nmin = min((int(v) for v in (v for v in values if len(v) == 14)))
            nmax = max((int(v) for v in (v for v in values if len(v) == 14)))
            if nmin < min_:
                min_ = nmin
            if nmax > max_:
                max_ = nmax

    return min_, max_


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    indices = [i for i in range(len(lines)) if lines[i].startswith("inp")]
    commands = []
    for start, end in zip(indices, indices[1:] + [len(lines)]):
        commands.append(lines[start:end])

    # Read the non-hardcoded values from the MONAD
    all_v1 = [command[4].split(" ")[-1] for command in commands]
    all_v2 = [command[5].split(" ")[-1] for command in commands]
    all_v3 = [command[-3].split(" ")[-1] for command in commands]

    min_, max_ = find_(all_v1, all_v2, all_v3)
    print(f"Part 1: {max_}")
    print(f"Part 2: {min_}")
