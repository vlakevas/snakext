import termios


def enable_raw_mode(fd: int) -> list:
    old_attr_list = termios.tcgetattr(fd)
    # we store the old attr list for the disabling module
    new_attr_list = termios.tcgetattr(fd)
    # we get the [iflag, oflag, cflag, lflag, ispeed, ospeed, cc] list

    new_attr_list[0] &= ~(
        termios.IXON
        | termios.ICRNL
        | termios.BRKINT
        | termios.INPCK
        | termios.ISTRIP
        | termios.PARMRK
        | termios.INLCR
        | termios.IGNCR
    )
    new_attr_list[1] &= ~(termios.OPOST)
    new_attr_list[2] &= ~(termios.CSIZE | termios.PARENB)
    new_attr_list[2] |= termios.CS8
    new_attr_list[3] &= ~(termios.ICANON | termios.ECHO | termios.ISIG | termios.IEXTEN)
    new_attr_list[6][termios.VMIN] = 0
    new_attr_list[6][termios.VTIME] = 1

    termios.tcsetattr(fd, termios.TCSAFLUSH, new_attr_list)

    return old_attr_list


def disable_raw_mode(fd: int, default_attr: list) -> None:

    termios.tcsetattr(fd, termios.TCSAFLUSH, default_attr)
