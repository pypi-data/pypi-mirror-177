import dataclasses
import json
import subprocess
import tempfile
from functools import cached_property
from pathlib import Path
from shutil import which
from typing import List

from vim_quest_cli.deps.is_js import IS_JS

if not IS_JS:
    import curses.ascii
    import importlib_resources


from vim_quest_cli.engine.engine_interface import (
    EngineInterface,
    EngineState,
    CursorPos,
)

from vim_quest_cli.engine.vim_exe import resources as vim_resources


class Constants:
    @cached_property
    def SAVE_STATE_VIM(self):
        return (
            importlib_resources.files(vim_resources)
            .joinpath("save_state.vim")
            .read_text()
        )


CONSTANTS = Constants()


VIM_COMMAND = "vim"


def command_interpret(cmd):
    return cmd.replace("<ESC>", chr(curses.ascii.ESC))


class VimNotExistsException(Exception):
    pass


@dataclasses.dataclass(frozen=True)
class VimExeCursorPosition:
    lnum: int
    bufnum: int
    col: int
    off: int
    curswant: int


@dataclasses.dataclass(frozen=True)
class VimStateResults:
    command: str  # Same as input, can be ignored
    buffer: List[str]
    cursor: VimExeCursorPosition

    @classmethod
    def from_json(cls, j):
        return cls(
            command=j["command"],
            buffer=j["buffer"],
            cursor=VimExeCursorPosition(**j["cursor"]),
        )


def _vim_execute_actions(buffer: List[str], commands: List[str]) -> VimStateResults:
    if not which(VIM_COMMAND):
        raise VimNotExistsException()

    with tempfile.TemporaryDirectory() as tmp_path_str:
        tmp_path = Path(tmp_path_str)

        input_path = tmp_path / "input.txt"
        command_path = tmp_path / "commands.str"
        output_path = tmp_path / "output.json"
        vim_code_path = tmp_path / "save_state.vim"

        # You are surprised that we add a \n at the end of the file.
        # It's because something something old conventions I guess.
        input_path.write_text("\n".join(buffer) + "\n")
        command_path.write_text("".join(commands))
        vim_code_path.write_text(CONSTANTS.SAVE_STATE_VIM)

        cmd = [
            "vim",
            f"+:source {vim_code_path}",
            f'+call ExecuteAndSave("{input_path}", "{command_path}", "{output_path}")',
            "--not-a-term",
            "--noplugin",
        ]

        _ = subprocess.check_output(cmd, cwd=tmp_path_str)

        output_content = output_path.read_text()
        json_res = json.loads(output_content)
        print(json_res)
        return VimStateResults.from_json(json_res)


class VimExeEngine(EngineInterface):
    def process(self, state: EngineState) -> EngineState:
        res = _vim_execute_actions(state.buffer, state.command)

        return EngineState(
            cursor=CursorPos(
                line=res.cursor.lnum,
                col=res.cursor.col,
                col_want=res.cursor.curswant,
            ),
            buffer=res.buffer,
            command=[],
        )


__all__ = ["VimExeEngine"]

if __name__ == "__main__":
    print(_vim_execute_actions("hello world", "yyx"))
    print(
        _vim_execute_actions(
            "hello world", command_interpret(r"2litoto<ESC>Atiti<ESC>")
        )
    )
