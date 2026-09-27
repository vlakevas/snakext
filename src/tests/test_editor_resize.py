from editor import Editor


class TestEditorResize:
    def test_cursor_shrink(self):
        test_obj = Editor(24, 80)
        test_obj.cursor_line = 21
        test_obj.cursor_col = 75

        test_obj.resize(10, 40)
        assert test_obj.cursor_line == 9
        assert test_obj.cursor_col == 39

    def test_cursor_no_move(self):
        test_obj = Editor(10, 10)
        test_obj.cursor_line = 5
        test_obj.cursor_col = 5
        test_obj.resize(20, 40)

        assert test_obj.cursor_line == 5
        assert test_obj.cursor_col == 5
