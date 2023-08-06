""" Transform an Engine state into a matrix of chars. """
import dataclasses
import enum
from typing import List, Optional
from ansi.colour.base import Graphic

from vim_quest_cli.engine.engine_interface import EngineState
from vim_quest_cli.interface.mapping import Keys

RESET_STYLE = str(Graphic("0"))


class FgColor(enum.Enum):
    # TODO use ansi.color.fg instead
    black = str(Graphic("30"))
    red = str(Graphic("31"))
    green = str(Graphic("32"))
    yellow = str(Graphic("33"))
    blue = str(Graphic("34"))
    magenta = str(Graphic("35"))
    cyan = str(Graphic("36"))
    white = str(Graphic("37"))


class BgColor(enum.Enum):
    black = str(Graphic("40"))
    red = str(Graphic("41"))
    green = str(Graphic("42"))
    yellow = str(Graphic("43"))
    blue = str(Graphic("44"))
    magenta = str(Graphic("45"))
    cyan = str(Graphic("46"))
    white = str(Graphic("47"))


@dataclasses.dataclass()
class CharacterView:
    ascii: str = " "  # Should always be of length 1
    fg_color: Optional[FgColor] = None
    bg_color: Optional[BgColor] = None


@dataclasses.dataclass()
class CursorPos:
    line: int = 1
    column: int = 1


@dataclasses.dataclass()
class ViewData:
    chars: List[List[CharacterView]] = dataclasses.field(default_factory=list)
    cursor: CursorPos = CursorPos()
    status: str = None


class ViewFactory:
    @staticmethod
    def createView(engine_state: EngineState):
        def k_to_s(k):
            if isinstance(k, Keys):
                return f"<{k.value}>"
            return k

        return ViewData(
            chars=[[CharacterView(c) for c in line] for line in engine_state.buffer],
            cursor=CursorPos(
                line=engine_state.cursor.line, column=engine_state.cursor.col
            ),
            status=repr(
                engine_state.command
            ),  # "".join(map(k_to_s, engine_state.command)),
        )
