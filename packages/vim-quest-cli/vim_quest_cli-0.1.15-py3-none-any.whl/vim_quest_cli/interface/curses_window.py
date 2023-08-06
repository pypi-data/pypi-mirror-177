# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#file-ansi-md
import enum
import os
import re
import select
import sys
from typing import Tuple

from vim_quest_cli.deps.is_js import IS_JS
from vim_quest_cli.interface import mapping

if not IS_JS:
    import curses

from vim_quest_cli.interface.mapping import input_to_keys
from vim_quest_cli.deps.ansi import cursor as ansi_cursor
from vim_quest_cli.deps.ansi.sequence import sequence


# TODO for cursor position :
# https://stackoverflow.com/questions/46651602/determine-the-terminal-cursor-position-with-an-ansi-sequence-in-python-3


def get_char(file, timeout=0):
    if select.select([file], [], [], timeout) == ([file], [], []):
        print("ready for reading")
        return file.read(1)
    return ""


class Ansi:
    # Escape sequence = "\033"
    CLEAR_ENTIRE_SCREEN = "\033[2J"
    RESET = "\033[c"
    MOVE_CURSOR = "\033[{line};{column}H"
    REQUEST_CURSOR_POSITION = "\033[6n"
    REQUEST_CURSOR_POSITION_2 = sequence("6n")()
    assert REQUEST_CURSOR_POSITION == REQUEST_CURSOR_POSITION_2
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"

    @staticmethod
    def cursor_goto(row: int, col: int):
        return ansi_cursor.goto(row, col)

    # Reading sequence
    CURSOR_POSITION_RESPONSE = re.compile(r"\033\[(?P<line>[0-9]*);(?P<column>[0-9]*)R")

    def getmaxyx(self):
        return curses.wrapper(lambda stdscr: stdscr.getmaxyx())


def stdout_write(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def reading_stdin(blocking=True, timeout=0.5):
    # We could use https://github.com/prompt-toolkit/python-prompt-toolkit/blob/9a2a550f4537f2d11cac7b902ec36e376c4131bd/src/prompt_toolkit/input/posix_utils.py#L51
    import tty

    # Not needed anymore
    # tty.setraw(sys.stdin)
    return sys.stdin.read(1)
    # return sys.stdin.read(1)  # In the meantime

    # tty.setraw(sys.stdin.fileno())
    if blocking:
        res = sys.stdin.read(1)  # Blocking
    else:
        res = ""

    tty.setraw(sys.stdin.fileno())

    rfds, _, _ = select.select([sys.stdin.fileno()], [], [], timeout)
    while sys.stdin.fileno() in rfds or sys.stdin in rfds:
        res += sys.stdin.read(1)
        rfds, _, _ = select.select([sys.stdin.fileno()], [], [], 0)

    # We could also use

    return res


class InputKeysNames(enum.Enum):
    pass


def reset_terminal():
    stdout_write(Ansi.RESET)


def interpret_input(s):
    char = ord(s)
    if char == 3:  # Ctr-C
        raise KeyboardInterrupt()

    if 32 <= char <= 126:  # Regular characters
        return chr(char)

    if char in {10, 13}:  # Enter
        return "ENTER"  # TODO: check

    if char == 27:
        # It's also the ESC sequence
        return "KEY_ESC"  # In the meantime

        # if not self._has_stdin_more(timeout=0):
        #    return 'KEY_ESC'

        # next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
        # command = (char, next1, next2)
        # if command == (27, 91, 68):
        #    return "KEY_LEFT"
        # if command == (27, 91, 67):
        #    return "KEY_RIGHT"
        # if command == (27, 91, 66):
        #    return "KEY_DOWN"
        # if command == (27, 91, 65):
        #    return "KEY_UP"
        return f"{command=!r}"


class Window:
    """Ansi window that duck-type the curses window."""

    def __init__(self, reading_stdin_fct=reading_stdin, stdout_write_fct=stdout_write):
        self._reading_stdin_fct = reading_stdin_fct
        self._stdout_write_fct = stdout_write_fct

        self._stdout_written = []

    def _write(self, s):
        self._stdout_written.append(s)

    def _has_stdin_more(self, timeout=0.1):
        return select.select([self._stdin], [], [], 0) == ([self._stdin], [], [])

    def clear(self) -> None:
        self._write(Ansi.CLEAR_ENTIRE_SCREEN)

    def getmaxyx(self) -> Tuple[int, int]:
        return (24, 80)
        if os.getenv("VIMQUEST_MAXYX"):
            max_str = os.getenv("VIMQUEST_MAXYX")
            max_y_str, max_x_str = max_str.split("-")
            return int(max_y_str), int(max_x_str)

        return curses.wrapper(lambda stdscr: stdscr.getmaxyx())

    def addstr(self, row: int, col: int, s: str):
        self._write(Ansi.cursor_goto(row, col))
        self._write(s.replace("\n", "\n\r"))

    def move(self, row: int, col: int) -> None:
        row += 1  # Values are base 1 in ansi
        col += 1
        self._write(Ansi.cursor_goto(row, col))

    def refresh(self) -> None:
        self._stdout_write_fct("".join(self._stdout_written))
        self._stdout_written.clear()

    def getkey(self) -> str:
        return mapping.input_to_keys(self._reading_stdin_fct())
