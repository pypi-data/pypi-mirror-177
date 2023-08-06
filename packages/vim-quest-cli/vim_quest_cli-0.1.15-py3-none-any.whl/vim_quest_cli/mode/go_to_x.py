import dataclasses
from typing import Iterable

from vim_quest_cli.engine.engine_interface import EngineState, CursorPos
from vim_quest_cli.mode.mode_container import ModeElement
from vim_quest_cli.mode.mode_interface import Mode
from vim_quest_cli.view.view import ViewData, FgColor, CharacterView

import random


class GoToXMode(ModeElement):

    _count: int = 5

    def _reset_path(self, state: EngineState, reset_cursor=False) -> EngineState:
        # First empty the state.
        nb_lines, nb_cols = 14, 40
        text = "Go to the X using the hjkl keys."
        new_buffer = [["."] * nb_cols for _ in range(nb_lines)]
        new_buffer[random.randint(0, nb_lines - 1)][
            random.randint(0, nb_cols - 1)
        ] = "X"
        new_buffer[:] = [text] + ["".join(line) for line in new_buffer]

        cursor = state.cursor
        if reset_cursor:
            cursor = CursorPos(
                line=5,
                col=10,
                col_want=10,
            )

        # After 5 reset, change mode
        if self._count <= 0:
            self._container.move_next_mode()
        self._count -= 1

        return state.copy(buffer=new_buffer, cursor=cursor)

    def _init_after_params(self):
        self._state = self._reset_path(self._state, reset_cursor=True)

    @staticmethod
    def _char_under_cursor(state: EngineState):
        return state.buffer[state.cursor.line - 1][state.cursor.col - 1]

    def state_change(
        self, state_init: EngineState, state_end: EngineState
    ) -> EngineState:
        if GoToXMode._char_under_cursor(state_end) == "X":
            return self._reset_path(state_end)
        return state_end

    def _set_view_char(self, view: ViewData, char: str, line: int, column: int):
        # TODO: make sure the cursor and the line/col are on the same base.
        # I think it's going to be easier to be all 0 based from now on, and to adapt the interface to be otherwise.
        if line < 1 or line > len(view.chars):
            return
        if column < 1 or column > len(view.chars[0]):
            return
        current_val = view.chars[line - 1][column - 1]
        if current_val.ascii == "X":
            return
        view.chars[line - 1][column - 1] = CharacterView(
            ascii=char,
        )

    def change_view(self, view: ViewData):
        for line in view.chars:
            for character in line:
                if character.ascii == "X":
                    character.fg_color = FgColor.red
                if character.ascii == "#":
                    character.fg_color = FgColor.green

        self._set_view_char(view, "k", view.cursor.line - 1, view.cursor.column)
        self._set_view_char(view, "^", view.cursor.line - 2, view.cursor.column)
        self._set_view_char(view, "j", view.cursor.line + 1, view.cursor.column)
        self._set_view_char(view, "v", view.cursor.line + 2, view.cursor.column)
        self._set_view_char(view, "l", view.cursor.line, view.cursor.column + 2)
        self._set_view_char(view, ">", view.cursor.line, view.cursor.column + 4)
        self._set_view_char(view, "h", view.cursor.line, view.cursor.column - 2)
        self._set_view_char(view, "<", view.cursor.line, view.cursor.column - 4)

        return view
