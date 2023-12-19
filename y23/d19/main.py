import os
import re
import copy
import math

from queue import Queue


def part1(parts, rules):
    q = Queue()
    for part in parts:
        q.put(("in", part))
    accepted = []
    while not q.empty():
        workflow, part = q.get()
        exec(part)
        for condition, dest in rules[workflow]:
            v = eval(f"1 if {condition} else 0")
            if v:
                if dest == "A":
                    accepted.append(part)
                elif dest == "R":
                    pass
                else:
                    q.put((dest, part))
                break

    sum_ = 0
    for part in accepted:
        sum_ += sum(map(int, re.findall(r"(\d+)", part)))
    return sum_


def split_range(range_, check, num):
    if check == "<":
        pass_range = [range_[0], int(num)]
        fail_range = [int(num), range_[1]]
    else:
        fail_range = [range_[0], int(num) + 1]
        pass_range = [int(num) + 1, range_[1]]
    if pass_range[1] <= pass_range[0]:
        pass_range = []
    if fail_range[1] <= fail_range[0]:
        fail_range = []
    return pass_range, fail_range


def part2(rules):
    q = Queue()
    q.put(("in", {"x": [1, 4001], "m": [1, 4001], "a": [1, 4001], "s": [1, 4001]}))
    accepted = []
    while not q.empty():
        workflow, range_ = q.get()
        for rule, dest in rules[workflow]:
            if isinstance(rule, bool):
                pass_interval = range_[var]
                fail_interval = []
            else:
                var, check, num = re.match(r"(\w)([<>])(\d+)", rule).groups()
                pass_interval, fail_interval = split_range(range_[var], check, num)
            if pass_interval:
                if dest == "R":
                    pass
                else:
                    new_range = copy.deepcopy(range_)
                    new_range[var] = pass_interval
                    if dest == "A":
                        accepted.append(new_range)
                    else:
                        q.put((dest, new_range))
            if fail_interval:
                range_[var] = fail_interval
            else:
                break
            pass

    N = 0
    for range_ in accepted:
        N += math.prod((v[1] - v[0]) for v in range_.values())
    return N


def parse_rules(lines):
    rules = {}
    for line in lines:
        name, rules_txt = re.match(r"(\w+)\{(.*)}", line).groups()
        rules_groups = rules_txt.split(",")
        groups = []
        for grp in rules_groups:
            if ":" in grp:
                condition, outcome = grp.split(":")
            else:
                condition = True
                outcome = grp
            groups.append((condition, outcome))
        rules[name] = groups
    return rules


def parse_parts(parts_lines):
    parts = []
    for line in parts_lines:
        parts.append(line.replace("{", "").replace("}", "").replace(",", ";"))
    return parts


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    rules = parse_rules(lines[: lines.index("")])
    parts = parse_parts(lines[lines.index("") + 1 :])
    print(f"Part 1: {part1(parts, rules)}")
    print(f"Part 2: {part2(rules)}")
