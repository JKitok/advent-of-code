import os
import sys
import shutil

THISDIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(THISDIR, "template")

if __name__ == "__main__":
    year = sys.argv[1]
    day = sys.argv[2]
    path = os.path.join(THISDIR, f"y{year}", f"d{day}")
    if os.path.exists(path):
        print("Path already exists!")
        exit(-1)
    else:
        os.makedirs(path)
        for file in os.listdir(TEMPLATE_DIR):
            dstfile = file.replace(".in", "")
            shutil.copyfile(
                os.path.join(TEMPLATE_DIR, file), os.path.join(path, dstfile)
            )
