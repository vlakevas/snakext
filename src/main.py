import sys
from raw_mode import RawMode
from input_handling import read_key, process_key, Status


def main():
    fd: int = sys.stdin.fileno()
    with RawMode(fd):
        while True:
            n_status = process_key(read_key(fd))
            if n_status == Status.QUIT:
                break


if __name__ == "__main__":
    main()
