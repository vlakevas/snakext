import os
import enum

# low-level input reading:


def read_key(fd: int) -> bytes:
    key: bytes = os.read(fd, 1)
    return key


# -----------------------------


# high-level input processing:
class Status(enum.Enum):
    NOTHING = enum.auto()
    QUIT = enum.auto()


def process_key(key: bytes) -> Status:

    if key == b"\x11":
        return Status.QUIT

    #yet to add the b"a" handling
    
    else:  # default case
        return Status.NOTHING
