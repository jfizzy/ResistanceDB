#!/usr/bin/env python3.6
from mia.file_mover import FileMover

def main():
    fm = FileMover("C:\\Users\\tyron\\school\\project\\Raw Data", \
        "C:\\Users\\tyron\\school\\project\\Dest",\
        "raw")
    fm.move_files()

if __name__ == "__main__":
    main()