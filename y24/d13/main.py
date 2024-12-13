import os
import itertools
import re
import sympy as sp
from tqdm import tqdm


def run(equations, offset):
    A, B = sp.symbols("A, B")
    total = 0
    for eq in tqdm(equations):
        eq1 = sp.Eq(A * int(eq[0]) + B * int(eq[2]), int(eq[4]) + offset)
        eq2 = sp.Eq(A * int(eq[1]) + B * int(eq[3]), int(eq[5]) + offset)
        ans = sp.solve((eq1, eq2), (A, B))
        number_a = ans[A]
        number_b = ans[B]
        if isinstance(number_a, sp.core.numbers.Integer) and isinstance(
            number_b, sp.core.numbers.Integer
        ):
            if offset > 0 or (number_a <= 100 and number_b <= 100):
                total += 3 * number_a + number_b
    return total


def parse(lines):
    equations = []
    for button_a, button_b, prize, _ in grouper(lines, 4):
        equations.append(
            (
                *re.findall(r"\d+", button_a),
                *re.findall(r"\d+", button_b),
                *re.findall(r"\d+", prize),
            )
        )
    return equations


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    equations = parse(lines)
    print(f"Part 1: {run(equations, offset=0)}")
    print(f"Part 2: {run(equations, offset=10000000000000)}")
