import os
import copy
from dataclasses import dataclass
from enum import Enum
import math
from typing import Optional, List
from queue import Queue


class SignalState(Enum):
    LOW = 0
    HIGH = 1


@dataclass
class Signal:
    state: SignalState
    source: str


class Module:
    def __init__(self, name: str, outputs: List[str]):
        self.name = name
        self.outputs = outputs

    def connect_input(self, module: str):
        pass

    def receive(self, signal: Signal) -> Optional[Signal]:
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.outputs})"


class FlipFlop(Module):
    def __init__(self, name: str, outputs: List[str]):
        super().__init__(name, outputs)
        self.on = False

    def receive(self, signal: Signal):
        if signal.state == SignalState.HIGH:
            return
        elif not self.on:
            self.on = True
            return Signal(SignalState.HIGH, self.name)
        else:
            self.on = False
            return Signal(SignalState.LOW, self.name)


class Conjunction(Module):
    def __init__(self, name: str, outputs: List[str]):
        super().__init__(name, outputs)
        self.inputs = {}

    def connect_input(self, module: str):
        self.inputs[module] = SignalState.LOW

    def receive(self, signal: Signal):
        self.inputs[signal.source] = signal.state
        if all((v == SignalState.HIGH for v in self.inputs.values())):
            return Signal(SignalState.LOW, self.name)
        else:
            return Signal(SignalState.HIGH, self.name)


class BroadCaster(Module):
    def receive(self, signal: Signal):
        return Signal(signal.state, self.name)


def parse(lines):
    modules = {}
    for line in lines:
        module_str, connection_str = map(str.strip, line.split(">"))
        module_str = module_str[:-1].strip()
        connections = list(map(str.strip, connection_str.split(",")))
        if module_str == "broadcaster":
            modules["broadcaster"] = BroadCaster("broadcaster", connections)
        elif module_str.startswith("%"):
            name = module_str[1:]
            modules[name] = FlipFlop(name, connections)
        elif module_str.startswith("&"):
            name = module_str[1:]
            modules[name] = Conjunction(name, connections)
        else:
            raise ValueError(module_str)

    for name, module in modules.items():
        for c in module.outputs:
            if c in modules:
                modules[c].connect_input(name)
    return modules


def run(modules, NUM, part2=False):
    signals = []
    q = Queue()
    N = 0
    stop = False
    # For part 2:
    # The following are all Conjunction modules connected directly to another Conjunction module that itself
    # is connected to the rx-module. I have printed the states of these four modules, and they all switch to
    # high for a single button press, and switch to low directly after. They do this with a given period respectively
    # (why is evident when looking and the graph, all 4 conjunction modules are part of their own cycle).
    #
    # Therefore, what will happen is that all four of these modules will switch to high on the same period,
    # which will trigger the conjunction module that they are connected to send a high signal to rx, and we
    # are done.
    #
    # Since this will take quite some time, we register the period for all four conjunction modules respectively,
    # and then calculate the lowest common multiple to get the button press when this will happen.
    periods = {k: None for k in ["fv", "jd", "vm", "lm"]}
    while N < NUM and not stop:
        # Press button
        q.put(("broadcaster", Signal(SignalState.LOW, "button")))
        N += 1
        # Handle all signals
        while not q.empty():
            receiver, signal = q.get()
            signals.append((receiver, signal))
            rec = modules.get(receiver)
            if rec:
                signal = rec.receive(signal)
                if signal:
                    for o in rec.outputs:
                        q.put((o, signal))

                    if part2 and rec.name in periods.keys():
                        if signal.state == SignalState.HIGH:
                            if periods[rec.name] is None:
                                periods[rec.name] = N
                            if all((v is not None for v in periods.values())):
                                print(f"N={N} and we have all periods")
                                stop = True

    if not part2:
        num_low = sum((s.state == SignalState.LOW for _, s in signals))
        num_high = sum((s.state == SignalState.HIGH for _, s in signals))
        return num_low * num_high
    else:
        return math.lcm(*periods.values())


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    modules = parse(lines)

    print(f"Part 1: {run(copy.deepcopy(modules), NUM=1000)}")
    print(f"Part 2: {run(copy.deepcopy(modules), NUM=1e5, part2=True)}")
