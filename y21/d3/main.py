import os

import numpy as np


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as fp:
        lines = fp.readlines()
    lines = [v.strip() for v in lines]


if __name__ == "__main__":
    main()
