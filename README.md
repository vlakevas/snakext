# snakext

A terminal-based text editor written in Python, built from scratch with only the standard library: no curses and no third-party UI libraries.

> **Status:** work in progress. The terminal layer and cursor movement work; text editing and file I/O are not implemented yet.

## What works so far

- **Raw mode.** The terminal is switched into raw mode through `termios`, so every keypress reaches the editor directly, without line buffering, echo or signal keys.
- **Safe restore.** Raw mode and the alternate screen are managed by a context manager, so the terminal is restored to its original state on exit, even when an exception is raised.
- **Input parsing.** Keypresses are read byte by byte and ANSI escape sequences are decoded into editor actions, such as the arrow keys.
- **Rendering.** Each frame is built in a byte buffer of ANSI escape sequences and written to the terminal in a single write.
- **Cursor movement** with the arrow keys, clamped to the edges of the window.

## Project structure

```
src/main.py            Main loop: read a key, update the editor, render
src/terminal.py        Raw mode, alternate screen and buffered output (context manager)
src/input_handling.py  Reading keys and decoding escape sequences
src/editor.py          Editor state, cursor movement and rendering
src/tests/             pytest tests
```

## Usage

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/). Runs on Linux and macOS (or WSL on Windows), since it relies on `termios`.

```bash
uv run src/main.py
```

Press `Ctrl-Q` to quit.

## Development

```bash
uv run pytest   # tests
uv run mypy src # type checking
```
