import dataclasses
from typing import Optional, Callable, Iterable, Union

from vim_quest_cli.engine.engine_interface import EngineState
from vim_quest_cli.interface.mapping import Keys

KeyPresses = Iterable[Union[Keys, str]]


@dataclasses.dataclass(frozen=True)
class KeyPressEvent:
    # We can get inspired by :
    # https://github.com/prompt-toolkit/python-prompt-toolkit/blob/9a2a550f4537f2d11cac7b902ec36e376c4131bd/src/prompt_toolkit/key_binding/key_processor.py#L421
    repeat: Optional[int] = None
    keys_press: KeyPresses = tuple()

    def get_repeat(self, default: int = 1) -> int:
        return self.repeat if self.has_repeat else default

    @property
    def has_repeat(self) -> bool:
        return self.repeat is not None


BindedFct = Callable[[KeyPressEvent, EngineState], EngineState]


class NoCommandLeftException(Exception):
    pass


class ActionNotPossibleException(Exception):
    pass


class KeyHandlerBinder:
    def bind(self, key_sequence: KeyPresses) -> Callable[[BindedFct], BindedFct]:
        ...
