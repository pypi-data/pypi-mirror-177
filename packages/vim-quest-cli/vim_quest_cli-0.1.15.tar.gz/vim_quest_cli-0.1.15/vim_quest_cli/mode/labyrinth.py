from typing import Iterable

from vim_quest_cli.engine.engine_interface import EngineState
from vim_quest_cli.mode.mode_interface import Mode
from vim_quest_cli.view.view import ViewData, FgColor


class LabyrinthMode(Mode):
    @staticmethod
    def _char_under_cursor(state: EngineState):
        return state.buffer[state.cursor.line - 1][state.cursor.col - 1]

    def state_change(
        self, state_init: EngineState, state_end: EngineState
    ) -> EngineState:
        if LabyrinthMode._char_under_cursor(state_end) == "#":
            return state_init.copy(command=state_end.command)
        return state_end

    def change_view(self, view: ViewData):
        for line in view.chars:
            for character in line:
                if character.ascii == "#":
                    character.fg_color = FgColor.red

        return view
