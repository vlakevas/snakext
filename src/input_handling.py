import os
import enum

# low-level input reading:


def read_key(fd: int) -> bytes:
    first_byte: bytes = os.read(fd, 1)

    if first_byte == b"\x1b":
        csi_byte = os.read(fd, 1)

        if csi_byte != b"[":
            return first_byte + csi_byte

        seq: bytes = first_byte + csi_byte
        while True:
            parameter_byte = os.read(fd, 1)
            if not parameter_byte:
                break

            seq += parameter_byte

            is_digit = parameter_byte.isdigit()
            is_semicolon = parameter_byte == b";"

            if not (is_digit or is_semicolon):
                break
        return seq

    return first_byte


# -----------------------------


# high-level input processing:
class Status(enum.Enum):
    NOTHING = enum.auto()
    QUIT = enum.auto()
    CURSOR_LEFT = enum.auto()
    CURSOR_RIGHT = enum.auto()
    CURSOR_UP = enum.auto()
    CURSOR_DOWN = enum.auto()


KEY_CASES: dict[bytes, Status] = {
    b"\x11": Status.QUIT,
    b"\x1b[A": Status.CURSOR_UP,
    b"\x1b[B": Status.CURSOR_DOWN,
    b"\x1b[C": Status.CURSOR_RIGHT,
    b"\x1b[D": Status.CURSOR_LEFT,
}


def process_key(key: bytes) -> Status:
    return KEY_CASES.get(key, Status.NOTHING)
