import os
import re

import numpy as np


class Map:
    def __init__(self, dest_start, src_start, length):
        self.src_start = src_start
        self.src_end = src_start + length
        self.dest_start = dest_start
        self.dest_end = dest_start + length

    def to_destination(self, src):
        if self.src_start <= src < self.src_end:
            return self.dest_start + src - self.src_start
        else:
            return None

    def __repr__(self):
        return f"Map([{self.src_start},{self.src_end})->[{self.dest_start},{self.dest_end}))"


def parse(lines):
    _, seeds_line = lines[0].split(":")
    seeds = np.fromstring(seeds_line, sep=" ").astype(np.int64)
    all_maps = {}
    stack = []
    for line in lines[2:]:
        if line.endswith("map:"):
            stack.sort(key=lambda x: x.src_start)
            src, dest = re.match(r"(\w+)-to-(\w+) map:", line).groups()
        elif not line:
            all_maps[src] = {"destination": dest, "maps": stack}
            stack = []
        else:
            stack.append(Map(*map(int, re.match(r"(\d+) (\d+) (\d+)", line).groups())))

    return seeds, all_maps


def to_destination(v, maps):
    for map in maps:
        n = map.to_destination(v)
        if n is not None:
            return n
    return v


def part1(nums, all_maps):
    current = "seed"
    while current != "location":
        maps = all_maps[current]["maps"]
        nums = [to_destination(v, maps) for v in nums]
        current = all_maps[current]["destination"]
    return min(nums)


def part2(nums, all_maps):
    # Create the ranges
    ranges = []
    for start, range_ in zip(nums[0::2], nums[1::2]):
        ranges.append((start, start + range_))

    next_key = "seed"
    maps = all_maps[next_key]["maps"]
    print(f"{next_key}: {len(ranges)} ranges")

    while (next_key := all_maps.get(next_key, {}).get("destination")) is not None:
        new_ranges = []
        for range_ in ranges:
            start, end = range_
            while end - start > 0:
                try:
                    map = next((m for m in maps if m.src_start <= start < m.src_end))
                    end_i = min(end, map.src_end)
                    new_ranges.append(
                        (map.to_destination(start), map.to_destination(end_i - 1) + 1)
                    )
                    start = end_i
                except StopIteration:
                    map_next = next((m for m in maps if m.src_start > start), None)
                    end_i = map_next.src_start if map_next is not None else end
                    new_ranges.append((start, end))
                    start = end_i
        ranges = new_ranges
        maps = all_maps.get(next_key, {}).get("maps")
        print(f"{next_key}: {len(ranges)} ranges")

    return min((x[0] for x in ranges))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()

    lines = [v.strip() for v in lines]
    lines.append("")
    seeds, all_maps = parse(lines)

    print(f"Part 1: {part1(seeds, all_maps)}")
    print(f"Part 2: {part2(seeds, all_maps)}")
