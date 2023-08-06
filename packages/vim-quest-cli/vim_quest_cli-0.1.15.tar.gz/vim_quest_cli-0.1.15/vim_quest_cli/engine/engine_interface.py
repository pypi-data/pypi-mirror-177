# First have a method that take a suite of
import dataclasses
import enum
import itertools
from typing import List, Iterable, Union, Tuple, Generator

from vim_quest_cli.interface.mapping import Keys


# TODO put EVERYTHING in base 0. Because otherwise it's too complex to understand.


@dataclasses.dataclass(frozen=True)
class CursorPos:
    line: int = 1  # 1 based. The first line is 1. Even without any char in the line.
    col: int = 1  # 1 based. The first element of the line is 1. Even without lines.
    col_want: int = 1  # Same as columns.

    def copy(self, **changes):
        return dataclasses.replace(self, **changes)


DEFAULT_CURSOR_POS = CursorPos()


@dataclasses.dataclass(frozen=True, eq=True)
class EngineState:
    cursor: CursorPos = DEFAULT_CURSOR_POS

    # Todo later
    # screen_rows: int = 2
    # screen_cols: int = 2
    # screen_xpos: int = 0
    # screen_ypos: int = 0

    buffer: Tuple[str] = dataclasses.field(default_factory=tuple)
    # paste: str = ""
    # command: str = ""
    # search: str = ""
    command: Tuple[Union[Keys, str]] = dataclasses.field(default_factory=tuple)

    # should_quit: bool = False

    # action: None = None  # Placeholder for any other kind of action outside the status

    def copy(self, **changes):
        if "buffer" in changes:
            # Ensure that the buffer is a tuple.
            changes["buffer"] = tuple("".join(line) for line in changes["buffer"])

        return dataclasses.replace(self, **changes)

    def with_added_command(self, command: List[str]):
        if not command:
            return self
        return self.copy(command=tuple(itertools.chain(self.command, command)))

    def character_buffer_generator(self) -> Generator[Tuple[int, int, str], None, None]:
        for line_num, line in enumerate(self.buffer):
            for col_num, char in enumerate(line):
                yield line_num + 1, col_num + 1, char

    def get_mutable_buffer_copy(self):
        return [list(line) for line in self.buffer]


class EngineInterface:
    def process(self, state: EngineState) -> EngineState:
        raise NotImplemented
