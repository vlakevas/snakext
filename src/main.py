import sys
from editor import Editor
from terminal import Terminal
from input_handling import read_key, process_key, Status


def main():
    fd_in: int = sys.stdin.fileno()
    fd_out: int = sys.stdout.fileno()
    with Terminal(fd_in, fd_out) as term:
        size = term.get_terminal_size()
        editor = Editor(size.lines, size.columns)
        while True:
            size = term.get_terminal_size()
            editor.resize(size.lines, size.columns)
            term.write(editor.render())
            term.flush()
            n_status = process_key(read_key(fd_in))

            if n_status == Status.QUIT:
                break
            elif n_status == Status.CURSOR_LEFT:
                editor.move_cursor_left()
            elif n_status == Status.CURSOR_RIGHT:
                editor.move_cursor_right()
            elif n_status == Status.CURSOR_UP:
                editor.move_cursor_up()
            elif n_status == Status.CURSOR_DOWN:
                editor.move_cursor_down()


if __name__ == "__main__":
    main()
