import os
import itertools
import collections


def part1(positions, score_to_win=1000):
    scores = [0 for v in positions]
    positions = [v - 1 for v in positions]
    num_rolls = 0
    die = 1
    while True:
        for i in range(len(positions)):
            for j in range(3):
                positions[i] = (positions[i] + die) % 10
                die += 1
                if die > 100:
                    die = 1
                num_rolls += 1

            scores[i] += positions[i] + 1
            if any((s >= score_to_win for s in scores)):
                return min(scores) * num_rolls


def part2(positions, score_to_win=21):
    wins = [0, 0]
    counter = collections.Counter()
    counter[tuple([*[v - 1 for v in positions], 0, 0])] = 1
    player = 0
    while counter:
        next_counter = collections.Counter()
        for vals, num in counter.items():
            for rolls in [v for v in itertools.product([1, 2, 3], repeat=3)]:
                new_pos = list(vals[:2])
                scores = list(vals[2:])
                new_pos[player] = (new_pos[player] + sum(rolls)) % 10
                scores[player] += new_pos[player] + 1
                if any((p >= score_to_win for p in scores)):
                    wins[0 if scores[0] >= score_to_win else 1] += num
                else:
                    next_counter[(*new_pos, *scores)] += num
        counter = next_counter
        player = (player + 1) % 2
    return max(wins)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    positions = [int(v.split(":")[1]) for v in lines]
    print(f"Part 1: {part1(positions)}")
    print(f"Part 2: {part2(positions)}")
