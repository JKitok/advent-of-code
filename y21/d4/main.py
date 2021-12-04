import os

import numpy as np


def read_as_matrix(lines):
    data = np.fromstring(" ".join(lines), sep=" ").astype(np.int64)
    return data.reshape((5, 5))


def check_bingo(matrix):
    bingo = False
    for axis in [0, 1]:
        rows = np.sum(matrix, axis=axis)
        bingo = bingo or np.any(rows == -len(rows))
    return bingo


def run_bingo(numbers, boards):
    for number in numbers:
        for i in range(boards.shape[0]):
            board = boards[i, :, :]
            board[board == number] = -1
            boards[i, :, :] = board

        for i in range(boards.shape[0]):
            has_bingo = check_bingo(boards[i, :, :])
            if has_bingo:
                return boards[i, :, :], number, i
    print(boards)
    raise ValueError("No bingo?")


def read_info(lines):
    bingo_numbers = np.fromstring(lines[0], sep=",").astype(np.int64)
    boards = []
    for i in range(2, len(lines[2:]), 6):
        boards.append(read_as_matrix(lines[i : i + 5]))
    boards_3d = np.stack(boards)
    return bingo_numbers, boards_3d


def part1(lines):
    bingo_numbers, boards_3d = read_info(lines)
    winning_board, last_number, _ = run_bingo(bingo_numbers, boards_3d)
    winning_board[winning_board == -1] = 0
    print(f"Answer: {np.sum(np.sum(winning_board))*last_number}")


def check_num_with_bingo(boards):
    return sum((check_bingo(boards[i, :, :]) for i in range(boards.shape[0])))


def part2(lines):
    bingo_numbers, boards_3d = read_info(lines)
    while boards_3d.shape[0] > 0:
        print(f"Running with {boards_3d.shape[0]} boards")
        winning_board, last_number, index = run_bingo(bingo_numbers, boards_3d)
        boards_3d = np.delete(boards_3d, index, axis=0)
    winning_board[winning_board == -1] = 0

    print(f"Answer: {np.sum(np.sum(winning_board))*last_number}")


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]
    part1(lines)
    part2(lines)
