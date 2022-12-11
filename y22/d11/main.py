import os
from typing import Callable
from dataclasses import dataclass
from collections import defaultdict
import math
import copy


@dataclass
class Monkey:
    items: list[int]
    operation: str
    divisor: int
    true_receiver: int
    false_receiver: int


def parse_operation(operation_str):
    a, op, b = operation_str.split(" ")
    assert a == "old"
    if op == "*":
        if b == "old":
            return lambda x: x * x
        else:
            return lambda x: x * int(b)
    elif op == "+":
        if b == "old":
            return lambda x: x + x
        else:
            return lambda x: x + int(b)
    else:
        return ValueError(op)


def parse_monkeys(lines):
    monkeys = []
    while True:
        id_line = next(lines)
        starting_items = list(map(int, next(lines).split(":")[1].strip().split(",")))
        operation_text = next(lines).split("=")[1].strip()
        operation = parse_operation(operation_text)
        divisor = int(next(lines).split(" ")[-1])
        true_receiver = int(next(lines).split(" ")[-1])
        false_receiver = int(next(lines).split(" ")[-1])
        monkeys.append(
            Monkey(starting_items, operation, divisor, true_receiver, false_receiver)
        )
        newline = next(lines, None)
        if newline is None:
            return monkeys


def play(monkeys, N, use_divisor):
    divisor = math.prod((m.divisor for m in monkeys))
    count = defaultdict(int)
    for round in range(N):
        for i in range(len(monkeys)):
            monkey = monkeys[i]
            for item in monkey.items:
                count[i] += 1
                worry = monkey.operation(item)
                if use_divisor:
                    worry %= divisor
                else:
                    worry //= 3
                if worry % monkey.divisor == 0:
                    monkeys[monkey.true_receiver].items.append(worry)
                else:
                    monkeys[monkey.false_receiver].items.append(worry)
            monkey.items = []

    sorted_count = sorted(count.values(), reverse=True)
    return sorted_count[0] * sorted_count[1]


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    monkeys = parse_monkeys(iter(lines))
    print(f"Part 1: {play(copy.deepcopy(monkeys), N=20, use_divisor=False)}")
    print(f"Part 2: {play(copy.deepcopy(monkeys), N=10000, use_divisor=True)}")
