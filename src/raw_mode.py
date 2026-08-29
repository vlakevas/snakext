import termios


def enable_raw_mode(fd) -> None:
    attr_list = termios.tcgetattr(fd)
    # we get the [iflag, oflag, cflag, lflag, ispeed, ospeed, cc] list

    attr_list[0] &= ~(
        termios.IXON
        | termios.ICRNL
        | termios.BRKINT
        | termios.INPCK
        | termios.ISTRIP
        | termios.PARMRK
        | termios.INLCR
        | termios.IGNCR
    )
    attr_list[1] &= ~(termios.OPOST)
    attr_list[2] &= ~(termios.CSIZE | termios.PARENB)
    attr_list[2] |= termios.CS8
    attr_list[3] &= ~(termios.ICANON | termios.ECHO | termios.ISIG | termios.IEXTEN)
    attr_list[6][termios.VMIN] = 0
    attr_list[6][termios.VTIME] = 1

    termios.tcsetattr(fd, termios.TCSAFLUSH, attr_list)


def disable_raw_mode(fd, default_attr) -> None:

    termios.tcsetattr(fd, termios.TCSAFLUSH, default_attr)
