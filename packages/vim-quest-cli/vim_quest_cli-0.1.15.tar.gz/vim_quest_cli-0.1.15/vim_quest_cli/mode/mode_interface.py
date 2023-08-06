# TODO: tests that take a mode (every mode with seed needs a seed in the init)
# and do unittest on them. Pushing a few key and expecting the output.
from typing import Iterable

from vim_quest_cli.engine.engine_interface import EngineInterface, EngineState
from vim_quest_cli.interface.mapping import Keys
from vim_quest_cli.view.view import ViewFactory, ViewData, CharacterView


class ModeHelper:
    @staticmethod
    def char_under_cursor(state: EngineState):
        return state.buffer[state.cursor.line - 1][state.cursor.col - 1]

    @staticmethod
    def set_view_char_raw(view: ViewData, char: str, line: int, column: int):
        """Change a single character in the view. Throw exception if out of bound."""
        view.chars[line - 1][column - 1] = CharacterView(ascii=char)

    @staticmethod
    def set_view_char(view: ViewData, char: str, line: int, column: int):
        """Change a single character in the view. Ignore out of bounds."""
        # TODO: make sure the cursor and the line/col are on the same base.
        # I think it's going to be easier to be all 0 based from now on, and to adapt the interface to be otherwise.
        if line < 1 or line > len(view.chars):
            return
        if column < 1 or column > len(view.chars[0]):
            return
        view.chars[line - 1][column - 1] = CharacterView(ascii=char)


class Mode:
    def __init__(self, engine: EngineInterface, state: EngineState, view: ViewFactory):
        self._engine = engine
        self._state = state
        self._view = view
        self._init_after_params()

    def feedkeys(self, keys: Iterable[Keys] = ()) -> ViewData:

        state_previous = self._state.with_added_command(keys)
        state_next = self._engine.process(self._state.with_added_command(keys))

        self._state = self.state_change(state_previous, state_next)

        view = self._view.createView(self._state)
        return self.change_view(view)

    # To be overloaded by subclasses

    def _init_after_params(self):
        ...

    def change_view(self, view: ViewData) -> ViewData:
        return view

    def state_change(
        self, state_init: EngineState, state_end: EngineState
    ) -> EngineState:
        return state_end

    # Easy way to copy modes.
    def kwargs_create_mode(self):
        return dict(
            engine=self._engine,
            state=self._state,
            view=self._view,
        )


"""

the screeze has to be passed around for mode to be able to use it.
Maybe in a GeneralConfig structure ?
- If the printing is unicode friendly or not.

    create_new_path
        - keep the curspor pos.
        - Generate a target to go
    When someting moves :
        - Check if the move ends up on the target,
        - If yes, then create new path.
    When printing happens :
        - change the target in red (first by just changing the target text by the red addition)

Improvements :
    - Cancel every non-movement.
    - Have the redness be part of the visual buffer.
    - Then add the target as metadata of the input, and use that to check what's happening.
"""

"""         
            k 
            ^ 
        h < x > l
            v
            j
             
"""


class PassthroughMode:

    pass
