from __future__ import annotations

from typing import Iterable, Optional, List, Callable

from vim_quest_cli.engine.engine_interface import EngineInterface, EngineState
from vim_quest_cli.interface.mapping import Keys
from vim_quest_cli.mode.mode_interface import Mode
from vim_quest_cli.view.view import ViewFactory, ViewData

MODE_FCT_LIST = List[
    Callable[[EngineInterface, EngineState, ViewFactory], "ModeElement"]
]


class ModeContainer(Mode):
    _current_mode: Optional[ModeElement] = None
    _mode_fct_list: MODE_FCT_LIST = []

    def __init__(
        self,
        engine: EngineInterface,
        state: EngineState,
        view: ViewFactory,
        mode_fct_list: MODE_FCT_LIST,
    ):
        super().__init__(engine, state, view)
        self._mode_fct_list = mode_fct_list

        self._current_mode = None
        self._current_mode_idx = -1
        self._current_mode_changed = False
        self.move_next_mode()

    def move_next_mode(self, clear_command=True):
        self._current_mode_idx = (self._current_mode_idx + 1) % len(self._mode_fct_list)
        fct = self._mode_fct_list[self._current_mode_idx]
        call_kwargs = (
            self._current_mode.kwargs_create_mode()
            if self._current_mode is not None
            else self.kwargs_create_mode()
        )
        # TODO: move should receive only one dataclass with the 3 values together.
        if clear_command:  # Avoid some problems.
            call_kwargs['state'] = call_kwargs['state'].copy(command=())
        self._current_mode = fct(**call_kwargs)
        self._current_mode.bind_container(self)
        self._current_mode_changed = True

    # Passthrough methods
    def feedkeys(self, keys: Iterable[Keys] = ()) -> ViewData:
        result = self._current_mode.feedkeys(keys)
        if self._current_mode_changed:
            self._current_mode_changed = False
            return self.feedkeys(())
        return result


class ModeElement(Mode):
    _container: Optional[ModeContainer] = None

    def _init_after_params(self):
        self._container = None

    def bind_container(self, container: ModeContainer):
        self._container = container
