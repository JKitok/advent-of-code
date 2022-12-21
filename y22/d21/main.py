import os
import copy

from sympy import solve
from sympy.parsing.sympy_parser import parse_expr


def simplify(data):
    ret = {}
    was_changed = True
    while was_changed:
        was_changed = False
        remaining = {}
        for monkey, expression in data.items():
            try:
                ret[monkey] = int(eval(expression))
                was_changed = True
            except NameError:
                for m, v in ret.items():
                    if m in expression:
                        expression = expression.replace(m, str(v))
                        was_changed = True
                remaining[monkey] = expression
        data = remaining
    return ret, data


def part1(data):
    ret, _ = simplify(data)
    return ret["root"]


def part2(data):
    eq = data["root"].replace("+", "-")
    del data["humn"]
    del data["root"]
    ret, data = simplify(data)

    for m, v in ret.items():
        if m in eq:
            eq = eq.replace(m, str(v))

    eqs = [parse_expr(eq)] + [parse_expr(f"{v} - {k}") for k, v in data.items()]
    slv = solve(eqs)
    slv = {str(k): v for k, v in slv.items()}
    return slv["humn"]


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    data = dict(map(str.strip, v.split(":")) for v in lines)
    print(f"Part 1: {part1(copy.deepcopy(data))}")
    print(f"Part 2: {part2(data)}")
