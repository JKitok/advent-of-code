import os
import re

from dataclasses import dataclass

import numpy as np


def parse_literal(bits):
    res = ""
    idx = 0
    stop = False
    while not stop:
        next_ = bits[idx : idx + 5]
        res += next_[1:]
        idx += 5
        stop = next_[0] != "1"
    res = int(res, 2)
    return res, bits[idx:]


def parse_packet(bits):
    version = int(bits[:3], 2)
    version_total = version
    type_ = int(bits[3:6], 2)
    result = 0
    if type_ == 4:
        result, bits = parse_literal(bits[6:])
    else:
        all_results = []
        if bits[6] == "0":
            length = int(bits[7 : 7 + 15], 2)
            subpackets = bits[7 + 15 : 7 + 15 + length]
            bits = bits[7 + 15 + length :]
            while len(subpackets) > 7:
                ver, result, subpackets = parse_packet(subpackets)
                all_results.append(result)
                version_total += ver
        else:
            numpackets = int(bits[7 : 7 + 11], 2)
            bits = bits[7 + 11 :]
            for i in range(numpackets):
                ver, result, bits = parse_packet(bits)
                all_results.append(result)
                version_total += ver

        if type_ == 0:
            result = sum(all_results)
        elif type_ == 1:
            result = np.prod(all_results)
        elif type_ == 2:
            result = np.min(all_results)
        elif type_ == 3:
            result = np.max(all_results)
        elif type_ == 5:
            result = 1 if all_results[0] > all_results[1] else 0
        elif type_ == 6:
            result = 1 if all_results[0] < all_results[1] else 0
        elif type_ == 7:
            result = 1 if all_results[0] == all_results[1] else 0
    return version_total, result, bits


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]

    hexstring = lines[0]
    bitstring = "".join((bin(int(v, 16))[2:].zfill(4) for v in hexstring))

    version_total = 0
    result_total = 0
    while len(bitstring) > 7:
        ver, result, bitstring = parse_packet(bitstring)
        version_total += ver
        result_total += result

    print(f"Part 1: {version_total}")
    print(f"Part 2: {result_total}")
