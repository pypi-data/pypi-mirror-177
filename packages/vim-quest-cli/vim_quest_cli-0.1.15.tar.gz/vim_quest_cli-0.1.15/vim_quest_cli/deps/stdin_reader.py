"""
When reading from stdin, if we want to be efficient, we need to read without cache and fast.
That's why we want to read stdin in a raw mode, but this messes with the stdin and the terminal doesn't like that.
"""
import contextlib
import os
import sys

from vim_quest_cli.deps.is_js import IS_JS
from vim_quest_cli.deps.prompt_toolkit.keys import Keys
from vim_quest_cli.interface import mapping

if not IS_JS:
    import termios
    import tty


def _read_stdin_raw(fd: int = sys.stdin.fileno()) -> bytes:
    res = os.read(fd, 1024)
    if res == b"\x03":
        raise KeyboardInterrupt()
    return res


def _str_from_bytes(input: bytes) -> str:
    return input.decode("utf-8")


def full_read_method():
    return _str_from_bytes(_read_stdin_raw())


@contextlib.contextmanager
def stdin_key_reader_ctx():
    fd = sys.stdin.fileno()
    with contextlib.suppress(termios.error):
        old_settings = termios.tcgetattr(fd)
    try:
        with contextlib.suppress(termios.error):
            tty.setraw(fd)
        yield full_read_method
    finally:
        with contextlib.suppress(termios.error):
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        # Should have a way of doing that in python, but maybe for later.
        # subprocess.check_call(["stty", "sane"])
