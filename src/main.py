import sys
import termios
import os
from raw_mode import enable_raw_mode, disable_raw_mode


def main():

    default_attr = termios.tcgetattr(sys.stdin)

    try:
        enable_raw_mode(sys.stdin)
        while True:
            char = os.read(0, 1)
            if char == b"\x11":
                break
            print(f"{char}")

    finally:
        disable_raw_mode(sys.stdin, default_attr)


if __name__ == "__main__":
    main()
