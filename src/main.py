import sys

from terminal import Terminal
from input_handling import read_key, process_key, Status


def main():
    fd_in: int = sys.stdin.fileno()
    fd_out: int = sys.stdout.fileno()
    with Terminal(fd_in, fd_out) as term:
        while True:
            term.draw_rows()
            term.terminal_flush()
            n_status = process_key(read_key(fd_in))
            if n_status == Status.QUIT:
                break


if __name__ == "__main__":
    main()
