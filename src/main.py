import sys
import os
from raw_mode import enable_raw_mode, disable_raw_mode


def main():
    fd: int = sys.stdin.fileno()
    try:
        previous_settings: list = enable_raw_mode(fd)
        while True:
            char = os.read(fd, 1)
            if char == b"\x11":
                break
            print(f"{char}")

    finally:
        disable_raw_mode(fd, previous_settings)


if __name__ == "__main__":
    main()
