from dataclasses import dataclass
from typing import List

from vim_quest_cli.engine.engine_interface import EngineState
from vim_quest_cli.old.status import VimGlobalStatus, SpecialChar


def assign_screen_size(
    state: VimGlobalStatus, nb_rows: int, nb_cols: int
) -> VimGlobalStatus:
    return state.copy(
        screen_cols=nb_rows,
        screen_rows=nb_cols - 1,  # Leave space for the status
    )


@dataclass(frozen=True)
class ScreenSize:
    rows: int
    cols: int


@dataclass(frozen=True)
class CursorPos:
    line: int
    col: int


@dataclass(frozen=True)
class ScreenData:
    screen_viewport: List[str]
    status_line: str
    cursor_pos: CursorPos


@dataclass(frozen=True)
class ScreenPositionState:
    xpos: int = 1
    ypos: int = 1
    cols: int = 80
    rows: int = 24


def get_status_line(state: EngineState) -> str:
    return f"{state.command!r}  pos: {state.cursor.line},{state.cursor.col}"


def get_screen_viewport(
    state: EngineState, screen_pos: ScreenPositionState, unicode_supported=True
) -> List[str]:
    xpos, nbcols = screen_pos.xpos, screen_pos.cols
    ypos, nbrows = screen_pos.ypos, screen_pos.rows

    x_start, x_end = xpos, xpos + nbcols
    y_start, y_end = ypos, ypos + nbrows

    relevant_lines = state.buffer[y_start:y_end]
    res = [l[x_start:x_end] for l in relevant_lines]

    if not unicode_supported:

        def _replace_unicode_line(l: str, replace_by="??"):
            return "".join((replace_by if SpecialChar.is_emoji(c) else c) for c in l)

        res = [_replace_unicode_line(l) for l in relevant_lines]

    return res


def get_cursor_pos_on_screen(
    state: EngineState, screen_pos: ScreenPositionState
) -> CursorPos:
    return CursorPos(
        line=state.cursor.line - screen_pos.ypos - 1,
        col=state.cursor.col - screen_pos.xpos - 1,
    )


def get_screen_data(state: EngineState, unicode_supported=True) -> ScreenData:
    screen_pos = ScreenPositionState()  # Extract from the engine state for later
    return ScreenData(
        status_line=get_status_line(state),
        screen_viewport=get_screen_viewport(state, screen_pos, unicode_supported),
        # cursor_pos=get_cursor_pos_on_screen(state, screen_pos),
        cursor_pos=CursorPos(-1, -1),
    )
