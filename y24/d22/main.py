import os
from collections import defaultdict


def secret(number):
    number = ((64 * number) ^ number) % 16777216
    number = ((number // 32) ^ number) % 16777216
    number = ((2048 * number) ^ number) % 16777216
    return number

def part1(lines):
    total = 0
    for line in lines:
        num = int(line)
        for i in range(2000):
            num = secret(num)
        total += num
    return total


def part2(lines):
    secrets = [int(v) for v in lines]
    diffs = [tuple() for v in secrets]
    n = 0
    for n in range(4):
        new_secrets = [secret(v) for v in secrets]
        diffs = [(*d, new_secrets[i] % 10 - secrets[i] % 10) for i, d in enumerate(diffs)]
        secrets = new_secrets

    n = 3
    all_seqs = defaultdict(lambda: {"counter": 0, "included": set()})
    while True:
        for i, d in enumerate(diffs):
            if i not in all_seqs[d]["included"]:
                all_seqs[d]["included"].add(i)
                all_seqs[d]["counter"] += (secrets[i] % 10)
        
        if n >= 2000 - 1:
            break
        new_secrets = [secret(v) for v in secrets]
        diffs = [(*d[1:], new_secrets[i] % 10 - secrets[i] % 10) for i, d in enumerate(diffs)]
        secrets = new_secrets
        n += 1

    all_ = list(all_seqs.items())
    all_.sort(key=lambda x: x[1]["counter"], reverse=True)
    return all_[0][1]["counter"]


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
