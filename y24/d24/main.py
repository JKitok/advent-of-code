import os
import re
class Device:
    def __init__(self, connections):
        self._gates = []
        for c in connections:
            self._gates.append([*re.match(r"(\S+) (AND|OR|XOR) (\S+) -> (\S+)", c).groups()])

        self._unique = set()
        for gate in self._gates:
            self._unique.add(gate[0])
            self._unique.add(gate[2])
            self._unique.add(gate[3])

    def run(self, values):
        stuck = False
        while not stuck and not all((v in values for v in self._unique)):
            stuck = True
            for (key1, operator, key2, output) in (gate for gate in self._gates if gate[3] not in values):
                v1 = values.get(key1)
                v2 = values.get(key2)
                if v1 is not None and v2 is not None:
                    stuck = False
                    out = 0
                    match operator:
                        case "OR": out = v1 or v2
                        case "AND": out = v1 and v2
                        case "XOR": out = v1 != v2
                        case _: raise ValueError(operator)
                    assert isinstance(out, bool)
                    values[output] = out
        
        if stuck:
            return None

        number = 0
        for (k, v) in values.items():
            if v and k.startswith("z"):
                bit = int(k.replace("z", ""))
                number += 1 << bit
        return number
    
    def add(self, n1, n2):
        values = {}
        for x, v in (("x", n1), ("y", n2)):
            for i in range(45):
                values[f"{x}{i:02d}"] = bool(v & (1 << i))
        return self.run(values)

def part1(initial, connections):
    dev = Device(connections)
    values = {}
    for v in initial:
        key, val = map(str.strip, v.split(":"))
        values[key] = val == "1"
    return dev.run(values)


def part2(connections):
    # Write output to graphviz format for manual inspection :)
    with open(os.path.join(os.path.dirname(__file__), "output.txt"), "w") as fp:
        xor_ = 0
        and_ = 0
        or_ = 0
        for c in connections:
            k1, op, k2, out = re.match(r"(\S+) (AND|OR|XOR) (\S+) -> (\S+)", c).groups()
            to_text = ""
            match op:
                case "AND": to_text = f"AND_{and_}"; and_+= 1
                case "OR": to_text = f"OR_{or_}"; or_+= 1
                case "XOR": to_text = f"XOR_{xor_}"; xor_+= 1
            to_text = f"{op}_{k1}_{k2}"
            fp.write(f"{k1} -> {to_text}\n")
            fp.write(f"{k2} -> {to_text}\n")
            fp.write(f"{to_text} -> {out}\n")

    # Try to add numbers until something breaks
    dev = Device(connections)
    for i1 in range(1, 45):
        for i2 in range(1, 20):
            v1 = 1 << i1
            v2 = 1 << i2
            v = dev.add(v1, v2)
            if v != v1 + v2:
                print(i1, i2)
                return


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    initial = lines[:lines.index("")]
    connections = lines[lines.index("") + 1:]
    print(f"Part 1: {part1(initial, connections)}")
    print(f"Part 2: {part2(connections)}")
