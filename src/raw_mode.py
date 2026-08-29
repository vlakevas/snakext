from __future__ import annotations
import termios


class RawMode:

    def __init__(self, fd: int):
        self.fd: int = fd
        self.normal_attr_list: list
        # [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]

    def __enter__(self) -> RawMode:
        self.normal_attr_list = termios.tcgetattr(self.fd)
        raw_attr_list: list = termios.tcgetattr(self.fd)

        raw_attr_list[0] &= ~(
            termios.IXON
            | termios.ICRNL
            | termios.BRKINT
            | termios.INPCK
            | termios.ISTRIP
            | termios.PARMRK
            | termios.INLCR
            | termios.IGNCR
        )
        raw_attr_list[1] &= ~(termios.OPOST)
        raw_attr_list[2] &= ~(termios.CSIZE | termios.PARENB)
        raw_attr_list[2] |= termios.CS8
        raw_attr_list[3] &= ~(
            termios.ICANON | termios.ECHO | termios.ISIG | termios.IEXTEN
        )
        raw_attr_list[6][termios.VMIN] = 0
        raw_attr_list[6][termios.VTIME] = 1

        termios.tcsetattr(self.fd, termios.TCSAFLUSH, raw_attr_list)

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.normal_attr_list)
        return False
