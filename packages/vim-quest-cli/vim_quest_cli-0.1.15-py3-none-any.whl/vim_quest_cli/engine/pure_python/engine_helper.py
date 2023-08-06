"""
Bunch of helper class for repeated actions on the text.
"""
from __future__ import annotations
import dataclasses
import enum
from typing import Tuple, Optional

from vim_quest_cli.engine.engine_interface import EngineState
from vim_quest_cli.engine.pure_python.KeyPressBindingHelper import KeyPresses

NUMBERS = set(map(str, range(10)))
# NUMBERS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'}
END_OF_LINE_MAX = 2147483647
LINE_BUFFER = 5


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class BufferHelper:
    @staticmethod
    def get_line_len(
        state: EngineState, line: Optional[int] = None, min_1: bool = True
    ) -> int:
        lnum = state.cursor.line if line is None else line
        line_len = len(state.buffer[lnum - 1])
        if min_1:
            return max(line_len, 1)
        return line_len

    @staticmethod
    def get_first_non_space_char(
        state: EngineState, lnum: Optional[int] = None, min_1: bool = True
    ) -> int:
        """Used for cursor positioning"""
        lnum = state.cursor.line if lnum is None else lnum
        line = state.buffer[lnum - 1]
        res = 0
        for res, char in enumerate(line):
            if char not in (" ", "\t"):
                break
        return max(res + 1, 1 if min_1 else 0)


class KeyMatchStatus(enum.IntEnum):
    NO_MATCH = enum.auto()
    KEY_PRESS_IS_COMMAND = enum.auto()
    KEY_PRESS_IS_PARTIAL_COMMAND = enum.auto()


@dataclasses.dataclass(frozen=True)
class KeyMatchResults:
    key_match_status: KeyMatchStatus
    keys_matching: Optional[KeyPresses] = None
    keys_left: Optional[KeyPresses] = None


class KeysHelper:
    @staticmethod
    def extract_keys_match(keys: KeyPresses, command: KeyPresses) -> KeyMatchResults:
        for i in range(max(len(keys), len(command))):
            if len(command) <= i:  # End of the command, it's a match
                return KeyMatchResults(
                    KeyMatchStatus.KEY_PRESS_IS_COMMAND, keys[: i + 1], keys[i + 1 :]
                )
            if len(keys) <= i:  # Command continues but the the keys stops. Partials
                return KeyMatchResults(KeyMatchStatus.KEY_PRESS_IS_PARTIAL_COMMAND)
            if command[i] != keys[i]:
                return KeyMatchResults(KeyMatchStatus.NO_MATCH)
        return KeyMatchResults(
            KeyMatchStatus.KEY_PRESS_IS_COMMAND, keys[: i + 1], keys[i + 1 :]
        )

    @staticmethod
    def split_repeat(keys: KeyPresses) -> Tuple[Optional[int], KeyPresses]:
        keys = list(keys)
        if not keys:  # Should not happen, but is an added security.
            return None, ()

        if keys[0] == "0" or keys[0] not in NUMBERS:
            return None, tuple(keys)

        repeat_str = ""
        while keys and keys[0] in NUMBERS:
            repeat_str += keys.pop(0)
        return int(repeat_str), tuple(keys)
