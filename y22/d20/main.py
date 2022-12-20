import os


def prune(number, N):
    if number > N:
        return number % N
    elif number < -N:
        return number % N - N
    else:
        return number


def mix(active, num):
    order = list(range(len(active)))

    for n in range(num):
        pass
        for i in range(len(order)):
            idx = order.index(i)
            v = active.pop(idx)
            o = order.pop(idx)

            m = prune(idx + v, len(active))

            active.insert(m, v)
            order.insert(m, o)

    idx0 = active.index(0)
    a = active[prune(idx0 + 1000, len(active))]
    b = active[prune(idx0 + 2000, len(active))]
    c = active[prune(idx0 + 3000, len(active))]
    return a + b + c


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [int(v.strip()) for v in lines]
    fixed_lines = [811589153 * v for v in lines]
    print(f"Part 1: {mix(lines, num=1)}")
    print(f"Part 2: {mix(fixed_lines, num=10)}")
