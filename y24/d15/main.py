import os
import numpy as np
import io

def print_grid(grid):
    # Use StringIO to capture the output of savetxt
    with io.StringIO() as output:
        np.savetxt(output, grid, delimiter="", fmt="%s")
        result = output.getvalue()  # Get the string value
    # Print the result
    print(result)


def run(grid, movement, width):
    index = np.where(grid == "@")
    index = index[1][0] + index[0][0]*1j

    for m in movement:
        d = {">": 1, "<": -1, "^": -1j, "v": 1j}[m]
        boxes = find_all_boxes(grid, index, d)
        if len(boxes) == 0:
            new_index = index + d
            if grid[int(new_index.imag), int(new_index.real)] == ".":
                index = move_self(grid, index, d)

        elif all((can_move(box, grid, d, width) for box in boxes)):
            move_boxes(grid, boxes, d, width)
            index = move_self(grid, index, d)

    total = 0
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r][c] in ("[", "O"):
                total += 100 * r + c

    return total

def move_self(grid, index, d):
    grid[int(index.imag), int(index.real)] = "."
    index += d
    grid[int(index.imag), int(index.real)] = "@"
    return index

def find_all_boxes(grid, index, d):
    boxes = []
    new_index = index + d
    if (c := grid[int(new_index.imag), int(new_index.real)]) in ["O", "[", "]"]:
        # Add current box
        if c == "]":
            box_index = new_index - 1
        else:
            box_index = new_index
        boxes.append(box_index)
        # Continue search
        if c != "O" and d == 1:
            boxes.extend(find_all_boxes(grid, box_index + 1, d))
        else:
            boxes.extend(find_all_boxes(grid, box_index, d))
        if c != "O" and d.imag != 0:
            boxes.extend(find_all_boxes(grid, box_index + 1, d))
    return boxes


def can_move(box, upscaled_grid, d, width):
    match d:
        case -1: return upscaled_grid[int(box.imag), int(box.real) - 1] != "#"
        case 1: return upscaled_grid[int(box.imag), int(box.real) + width] != "#"
        case _:
            check_index = box + d
            first = upscaled_grid[int(check_index.imag), int(check_index.real)] != "#"
            if width == 1:
                second = True
            else:
                second = upscaled_grid[int(check_index.imag), int(check_index.real) + 1] != "#"
            return first and second


def move_boxes(grid, boxes, d, width):
    type_ = ["[", "]"] if width == 2 else ["O"]
    new_boxes = [b + d for b in boxes]
    for box in boxes:
        for i, c in enumerate(type_):
            grid[int(box.imag), int(box.real) + i] = "."

    for box in new_boxes:
        for i, c in enumerate(type_):
            grid[int(box.imag), int(box.real) + i] = c


def upscale(grid):
    R, C = grid.shape
    upscaled_grid = np.zeros((R, 2 * C), dtype=str)
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            match grid[r][c]:
                case "#": upscaled_grid[r][2*c:2*c + 2] = ["#", "#"]
                case ".": upscaled_grid[r][2*c:2*c + 2] = [".", "."]
                case "O": upscaled_grid[r][2*c:2*c + 2] = ["[", "]"]
                case "@": upscaled_grid[r][2*c:2*c + 2] = ["@", "."]
    return upscaled_grid


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.rstrip("\n") for v in lines]
    grid_txt = lines[: lines.index("")]
    grid = np.array([list(line) for line in grid_txt], dtype=str)
    movement_txt = lines[lines.index("") + 1 :]
    movement = "".join(movement_txt)
    upscaled_grid = upscale(grid)
    print(f"Part 1: {run(grid, movement, width=1)}")
    print(f"Part 2: {run(upscaled_grid, movement, width=2)}")
