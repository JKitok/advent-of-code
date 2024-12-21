import os
import copy


class Computer:
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c

    def _combo(self, v):
        if v == 4:
            v = self._a
        elif v == 5:
            v = self._b
        elif v == 6:
            v = self._c
        return v

    def op_0(self, v):
        v = self._combo(v)
        self._a = int(self._a / 2**v)

    def op_1(self, v):
        self._b = self._b ^ v

    def op_2(self, v):
        v = self._combo(v)
        self._b = v % 8

    def op_3(self, v):
        if self._a == 0:
            return
        else:
            return None, v

    def op_4(self, _):
        self._b = self._b ^ self._c

    def op_5(self, v):
        v = self._combo(v)
        return v % 8, None

    def op_6(self, v):
        v = self._combo(v)
        self._b = int(self._a / 2**v)

    def op_7(self, v):
        v = self._combo(v)
        self._c = int(self._a / 2**v)

    def run(self, program):
        pointer = 0
        output = []
        while pointer < len(program):
            assert pointer + 1 < len(program)
            opcode = program[pointer]
            operand = program[pointer + 1]
            func = getattr(self, f"op_{opcode}")
            if (a := func(operand)) is not None:
                out, jump = a
                if out is not None:
                    output.append(out)
                if jump is not None:
                    pointer = jump
                else:
                    pointer += 2
            else:
                pointer += 2
        return output


def part1(A, B, C, program):
    c = Computer(A, B, C)
    output = c.run(program)
    return ",".join((str(v) for v in output))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fin:
        lines = fin.read().strip().split("\n")
        A, B, C = [int(lines[i].split(" ")[2]) for i in range(3)]
        program = list(map(int, lines[4].split(" ")[1].split(",")))

    print(f"Part 1: {part1(A, B, C, program)}")
