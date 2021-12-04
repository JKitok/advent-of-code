import os

from dataclasses import dataclass

import numpy as np


@dataclass
class Board:
    matrix: np.ndarray

    @classmethod
    def from_lines(cls, lines):
        data = np.fromstring(" ".join(lines), sep=" ").astype(np.int64)
        return cls(data.reshape((5, 5)))

    def has_bingo(self) -> bool:
        bingo = False
        for axis in [0, 1]:
            rows = np.sum(self.matrix, axis=axis)
            bingo = bingo or bool(np.any(rows == -len(rows)))
        return bingo

    def cross_number(self, number):
        self.matrix[self.matrix == number] = -1


def run_bingo(numbers, boards):
    for number in numbers:
        for board in boards:
            board.cross_number(number)

        for i, board in enumerate(boards):
            if board.has_bingo():
                return board, number

    raise ValueError("No bingo?")


def read_info(lines):
    bingo_numbers = np.fromstring(lines[0], sep=",").astype(np.int64)
    boards = []
    for i in range(2, len(lines[2:]), 6):
        boards.append(Board.from_lines(lines[i : i + 5]))
    return bingo_numbers, boards


def part1(lines):
    bingo_numbers, boards = read_info(lines)
    winning_board, last_number = run_bingo(bingo_numbers, boards)
    winning_board.matrix[winning_board.matrix == -1] = 0
    print(f"Answer: {np.sum(np.sum(winning_board.matrix))*last_number}")


def part2(lines):
    bingo_numbers, boards = read_info(lines)
    while len(boards) > 0:
        winning_board, last_number = run_bingo(bingo_numbers, boards)
        boards = [board for board in boards if not board.has_bingo()]
        bingo_numbers = bingo_numbers[
            np.where(bingo_numbers == last_number)[0][0] + 1 :
        ]
    winning_board.matrix[winning_board.matrix == -1] = 0
    print(f"Answer: {np.sum(np.sum(winning_board.matrix))*last_number}")


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    part1(lines)
    part2(lines)
