import random
from typing import Iterable

from vim_quest_cli.engine.engine_interface import EngineState, CursorPos
from vim_quest_cli.mode.mode_container import ModeElement
from vim_quest_cli.mode.mode_interface import Mode
from vim_quest_cli.view.view import ViewData, FgColor, CharacterView


class SearchXAndDestroy(ModeElement):

    CHAR = "#"

    def _reset_path(self, state: EngineState, reset_cursor=False) -> EngineState:
        # First empty the state.
        text = f'"x" delete a character. Use is on the {self.CHAR}.'
        nb_lines, nb_cols = 14, 40
        new_buffer = [["."] * nb_cols for _ in range(nb_lines)]
        for i in range(10):
            new_buffer[random.randint(0, nb_lines - 1)][
                random.randint(0, nb_cols - 1)
            ] = self.CHAR
        new_buffer[:] = [text] + ["".join(line) for line in new_buffer]

        cursor = state.cursor
        if reset_cursor:
            cursor = CursorPos(
                line=5,
                col=10,
                col_want=10,
            )

        return state.copy(buffer=new_buffer, cursor=cursor)

    def _init_after_params(self):
        self._state = self._reset_path(self._state, reset_cursor=True)

    @staticmethod
    def _char_under_cursor(state: EngineState):
        return state.buffer[state.cursor.line - 1][state.cursor.col - 1]

    def _num_x_left(self, state: EngineState):
        count = 0
        # Skipping the first explanation line.
        for line in state.buffer[1:]:
            for char in line:
                if char == self.CHAR:
                    count += 1
        return count

    def state_change(
        self, state_init: EngineState, state_end: EngineState
    ) -> EngineState:
        if self._num_x_left(state_end) == 0:
            return self._reset_path(state_end)
        return state_end

    def change_view(self, view: ViewData):
        for line in view.chars:
            for character in line:
                if character.ascii == self.CHAR:
                    character.fg_color = FgColor.red

        return view
