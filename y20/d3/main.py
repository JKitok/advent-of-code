import os

THISDIR = os.path.dirname(__file__)


def get_coordinate(line, index):
    local_idx = index % len(line)
    return line[local_idx]


def test_get_coordinate():
    assert get_coordinate(".#", 0) == "."
    assert get_coordinate(".#.", 1) == "#"
    assert get_coordinate(".##", 3) == "."
    assert get_coordinate(".#.", 4) == "#"


def run_down(lines, right, down):
    tree_count = 0
    column = 0
    for row in range(down, len(lines), down):
        column += right
        value = get_coordinate(lines[row], column)
        tree_count += value == "#"

    return tree_count


def test_game_example():
    lines = [
        "..##.......",
        "#...#...#..",
        ".#....#..#.",
        "..#.#...#.#",
        ".#...##..#.",
        "..#.##.....",
        ".#.#.#....#",
        ".#........#",
        "#.##...#...",
        "#...##....#",
        ".#..#...#.#",
    ]
    assert run_down(lines, 3, 1) == 7


def part1(lines):
    tree_count = run_down(lines, 3, 1)
    print(f"Answer: {tree_count}")


def part2(lines):
    tree_count = (
        run_down(lines, 1, 1)
        * run_down(lines, 3, 1)
        * run_down(lines, 5, 1)
        * run_down(lines, 7, 1)
        * run_down(lines, 1, 2)
    )
    print(f"Answer: {tree_count}")


def main():
    with open(os.path.join(THISDIR, "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines if v != ""]

    part1(lines)
    part2(lines)


if __name__ == "__main__":
    main()
