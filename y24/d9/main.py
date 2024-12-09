import os
from tqdm import tqdm


def part1(line):
    files = [*map(int, line[::2])]
    ids = [*range(len(files))]
    empty_spaces = [*map(int, line[1::2])]
    checksum = 0
    end_file = 0
    fill_space = 0
    end_id = 0
    index = 0
    while True:
        if end_file == 0:
            end_id = ids.pop()
            end_file = files.pop()

        if fill_space == 0:
            if len(files) > 0:
                # Grab the next file and fill its contents
                front_id = ids.pop(0)
                front_file = files.pop(0)
                for _ in range(front_file):
                    checksum += index * front_id
                    index += 1
            # Grab the next empty space to fill
            fill_space = empty_spaces.pop(0)

        # Fill space as much as possible or entire file
        num_fill = min(end_file, fill_space)
        for _ in range(num_fill):
            checksum += index * end_id
            index += 1

        end_file -= num_fill
        fill_space -= num_fill

        if len(files) == 0 and end_file == 0:
            break

    return checksum


def part2(line):
    if len(line) % 2 != 0:
        line += "0"
    system = []  # List of tuples: (size, id | None)
    files = []
    id_ = 0
    for file, space in pairwise(line):
        files.append((int(file), id_))
        system.append((int(file), id_))
        system.append((int(space), None))
        id_ += 1

    for size, file_id in tqdm(reversed(files)):
        try:
            idx_for_file = system.index((size, file_id))
            idx, (place_size, _) = next(
                (i, x) for (i, x) in enumerate(system) if x[1] is None and x[0] >= size
            )
            if idx < idx_for_file:
                if system[idx_for_file + 1][1] is not None:
                    system[idx_for_file] = (size, None)
                else:
                    system[idx_for_file + 1] = (
                        system[idx_for_file + 1][0] + size,
                        None,
                    )
                    system.remove((size, file_id))

                system[idx] = (size, file_id)
                remaining_size = place_size - size
                if remaining_size > 0:
                    if system[idx + 1][1] is not None:
                        system.insert(idx + 1, (remaining_size, None))
                    else:
                        system[idx + 1] = (system[idx + 1][0] + remaining_size, None)
        except StopIteration:
            pass  # Don't move the file

    checksum = 0
    index = 0
    for size, file_id in tqdm(system):
        if file_id is None:
            index += size
        else:
            for _ in range(size):
                checksum += index * file_id
                index += 1
    return checksum


def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    print(f"Part 1: {part1(lines[0])}")
    print(f"Part 2: {part2(lines[0])}")
