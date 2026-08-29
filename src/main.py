import sys
import os
from raw_mode import RawMode


def main():
    fd: int = sys.stdin.fileno()
    with RawMode(fd):
        while True:
            char = os.read(fd, 1)
            if char == b"\x11":
                break
            print(char)


if __name__ == "__main__":
    main()
