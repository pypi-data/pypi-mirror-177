# TODO: using .executor_interface instead of full path failed when bundle.
import dataclasses
from contextlib import suppress
from typing import Optional, List, Tuple, Callable, Iterable, Union, Dict

from vim_quest_cli.engine.engine_interface import (
    EngineInterface,
    EngineState,
    CursorPos,
)
from vim_quest_cli.engine.pure_python.KeyPressBindingHelper import (
    KeyPresses,
    BindedFct,
    NoCommandLeftException,
    KeyPressEvent,
    KeyHandlerBinder,
    ActionNotPossibleException,
)
from vim_quest_cli.engine.pure_python.bindings import bind_engine_actions
from vim_quest_cli.engine.pure_python.engine_helper import KeysHelper
from vim_quest_cli.interface.mapping import Keys


class PurePythonEngine(EngineInterface, KeyHandlerBinder):
    def __init__(self):
        # TODO: find a better data structure for that.
        # I know, a choice tree would be the best.
        self._binded_keys: Dict[KeyPresses, BindedFct] = {}
        bind_engine_actions(self)

    def bind(self, key_sequence: KeyPresses) -> Callable[[BindedFct], BindedFct]:
        def _bind_fct(fct: BindedFct) -> BindedFct:
            self._binded_keys[tuple(key_sequence)] = fct
            return fct

        return _bind_fct

    def process(self, state: EngineState) -> EngineState:

        previous_state, next_state = state, state
        with suppress(NoCommandLeftException):
            while previous_state.command:
                next_state = self._execute_single_command(previous_state)
                previous_state = next_state

        return next_state

    def _execute_single_command(self, state: EngineState) -> EngineState:
        if not state.command:
            return state

        if state.command[0] is None or state.command[0] == '':
            return state.copy(command = state.command[1:])

        repeat, c = KeysHelper.split_repeat(state.command)
        c = list(c)

        for keys, fct in self._binded_keys.items():
            if KeysHelper.does_keys_match(keys, c):
                action, leftover = KeysHelper.does_keys_match(keys, c)
                f_state = state.copy(command=leftover)
                f_event = KeyPressEvent(
                    repeat=repeat,
                    keys_press=action,
                )

                try:
                    return fct(f_event, f_state)
                except ActionNotPossibleException as _:
                    return f_state

        # TODO: it's not specifically like that
        if c and (
                c[-1] == Keys.Escape or c[-1] == Keys.ControlC):
            return state.copy(command=())

        raise NoCommandLeftException()
