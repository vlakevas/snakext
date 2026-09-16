from __future__ import annotations
import termios
import os


class Terminal:

    def __init__(self, fd_in: int, fd_out: int):
        self.fd_in: int = fd_in
        self.fd_out: int = fd_out
        self.terminal_buffer: bytearray = bytearray()

        # type declaration only

        self.terminal_size: os.terminal_size
        self.normal_attr_list: list
        # [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]

    def __enter__(self) -> Terminal:
        self.enable_raw_mode()
        self.terminal_size = os.get_terminal_size(
            self.fd_out
        )  # will become a problem when we want to resize the terminal
        self.enter_alt()
        self.terminal_flush()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.exit_alt()
        self.terminal_flush()
        self.disable_raw_mode()

        return False

    def enable_raw_mode(self) -> None:
        self.normal_attr_list = termios.tcgetattr(self.fd_in)
        raw_attr_list: list = termios.tcgetattr(self.fd_in)

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

        termios.tcsetattr(self.fd_in, termios.TCSAFLUSH, raw_attr_list)

    def disable_raw_mode(self) -> None:
        termios.tcsetattr(self.fd_in, termios.TCSAFLUSH, self.normal_attr_list)

    def draw_rows(self) -> None: # doesn't really belong in the terminal but its here cuz we don't have an editor class yet
        self.terminal_buffer.extend(b"\x1b[H")  # moves the cursor home
        rows = [
            b"\x1b[K~" for _ in range(self.terminal_size.lines)
        ]  # clears right and draws rows (~)
        self.terminal_buffer.extend(
            b"\r\n".join(rows) + b"\x1b[H"
        )  # merges every draw with carriage return and newline + moves cursor home

    def terminal_flush(self) -> None:
        os.write(self.fd_out, self.terminal_buffer)  # try to write everything at once
        self.terminal_buffer.clear()

    def enter_alt(self) -> None:
        self.terminal_buffer.extend(b"\x1b[?1049h")

    def exit_alt(self) -> None:
        self.terminal_buffer.extend(b"\x1b[?1049l")
