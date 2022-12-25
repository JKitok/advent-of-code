import os

FROM_SNAFU = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
TO_SNAFU = {v: k for k, v in FROM_SNAFU.items()}


def to_snafu(n):
    s = ""
    while n:
        n, r = divmod(n + 2, 5)
        s = TO_SNAFU[r - 2] + s
    return s


def from_base_5(s):
    n = 0
    for i, c in enumerate(reversed(s)):
        n += FROM_SNAFU[c] * 5**i
    return n


def part1(snafus):
    sum_ = sum((from_base_5(v) for v in snafus))
    return to_snafu(sum_)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    print(f"Part 1: {part1(lines)}")
