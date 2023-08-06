from typing import Iterable

from vim_quest_cli.engine.engine_interface import EngineInterface, EngineState
from vim_quest_cli.interface.mapping import Keys
from vim_quest_cli.mode.mode_container import ModeElement
from vim_quest_cli.mode.mode_interface import Mode
from vim_quest_cli.view.view import ViewFactory, ViewData

BUFFER = """\

        ************************ 
        * Welcome to vim quest *
        ************************ 

In the next screen, you have to go to the X mark.
Using the movements :
 - h : Left
 - j : Down
 - k : Up
 - l : Right

You can play moving around here.

At anytime you can press <space> to go to the next screen.
Press <space> for the next screen.
"""


class WelcomeScreen(ModeElement):
    def _init_after_params(self):
        self._state = self._state.copy(buffer=BUFFER.split("\n"))

    def feedkeys(self, keys: Iterable[Keys] = ()) -> ViewData:
        if " " not in keys:
            return super().feedkeys(keys)
        # Space in keys, setup the next mode
        self._container.move_next_mode()
