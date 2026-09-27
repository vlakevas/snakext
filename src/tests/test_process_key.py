from input_handling import process_key, Status


class TestProcessKey:
    def test_nothing_status(self):
        assert process_key(b"") == Status.NOTHING

    def test_quit_status(self):
        assert process_key(b"\x11") == Status.QUIT
