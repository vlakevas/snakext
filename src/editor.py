class Editor:
    def __init__(self, lines: int, cols: int):
        self.cursor_line: int = 0
        self.cursor_col: int = 0
        self.resize(lines, cols)

    def render(self) -> bytes:
        render_buffer = bytearray()
        render_buffer.extend(b"\x1b[?25l")  # hides the cursor
        render_buffer.extend(b"\x1b[H")  # moves cursor home
        lines_seq = [
            b"\x1b[K~" for _ in range(self.terminal_lines)
        ]  # clears right and draws lines (~)
        render_buffer.extend(b"\r\n".join(lines_seq))  # adds C.R. and newline lines

        move_cursor_seq = f"\x1b[{self.cursor_line + 1};{self.cursor_col + 1}H".encode(
            "ascii"
        )
        render_buffer.extend(move_cursor_seq)  # moves the cursor

        render_buffer.extend(b"\x1b[?25h")  # unhides the cursor
        return bytes(render_buffer)

    def resize(self, lines: int, cols: int) -> None:
        self.terminal_lines = lines
        self.terminal_cols = cols

        if self.cursor_line >= self.terminal_lines:
            self.cursor_line = max(0, self.terminal_lines - 1)

        if self.cursor_col >= self.terminal_cols:
            self.cursor_col = max(0, self.terminal_cols - 1)

    def move_cursor_left(self) -> None:
        if self.cursor_col > 0:
            self.cursor_col -= 1

    def move_cursor_right(self) -> None:
        if self.cursor_col < self.terminal_cols - 1:
            self.cursor_col += 1

    def move_cursor_up(self) -> None:
        if self.cursor_line > 0:
            self.cursor_line -= 1

    def move_cursor_down(self) -> None:
        if self.cursor_line < self.terminal_lines - 1:
            self.cursor_line += 1
