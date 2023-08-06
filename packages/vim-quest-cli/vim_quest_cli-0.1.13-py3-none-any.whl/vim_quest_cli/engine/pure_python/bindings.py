from vim_quest_cli.engine.engine_interface import EngineState
from vim_quest_cli.engine.pure_python.KeyPressBindingHelper import (
    KeyHandlerBinder,
    KeyPressEvent,
    ActionNotPossibleException,
)
from vim_quest_cli.engine.pure_python.engine_helper import BufferHelper
from vim_quest_cli.interface.mapping import Keys


# TODO : for the names, extract the names from the official vim documentation.
# So we can have a coherent naming.


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


# TODO : move that to engine constants or something
END_OF_LINE_MAX = 2147483647


def bind_engine_actions(engine: KeyHandlerBinder):
    @engine.bind([Keys.Down])
    @engine.bind(["j"])
    def move_down(event: KeyPressEvent, state: EngineState) -> EngineState:
        repeat = event.get_repeat()
        new_lnum = min(state.cursor.line + repeat, len(state.buffer))
        if len(state.buffer) < new_lnum:  # No more place to go
            raise ActionNotPossibleException()
        col = min(
            state.cursor.col_want, BufferHelper.get_line_len(state, line=new_lnum)
        )
        return state.copy(cursor=state.cursor.copy(line=new_lnum, col=col))

    @engine.bind([Keys.Up])
    @engine.bind(["k"])
    def move_up(event: KeyPressEvent, state: EngineState) -> EngineState:
        repeat = event.get_repeat()
        new_lnum = max(state.cursor.line - repeat, 1)
        col = min(
            state.cursor.col_want, BufferHelper.get_line_len(state, line=new_lnum)
        )
        return state.copy(cursor=state.cursor.copy(line=new_lnum, col=col))

    @engine.bind([Keys.Left])
    @engine.bind(["h"])
    def move_left(event: KeyPressEvent, state: EngineState) -> EngineState:
        repeat = event.get_repeat()
        new_col = max(state.cursor.col - repeat, 1)
        return state.copy(cursor=state.cursor.copy(col=new_col, col_want=new_col))

    @engine.bind([Keys.Right])
    @engine.bind(["l"])
    def move_right(event: KeyPressEvent, state: EngineState) -> EngineState:
        repeat = event.get_repeat()
        new_col = min(state.cursor.col + repeat, BufferHelper.get_line_len(state))
        return state.copy(cursor=state.cursor.copy(col=new_col, col_want=new_col))

    @engine.bind(["$"])
    def move_end_of_line(event: KeyPressEvent, state: EngineState) -> EngineState:
        repeat = event.get_repeat()
        new_lnum = min(state.cursor.line + repeat - 1, len(state.buffer))
        if repeat == 1:  # Normal case
            return state.copy(
                cursor=state.cursor.copy(
                    line=new_lnum,
                    col=BufferHelper.get_line_len(state, new_lnum),
                    col_want=END_OF_LINE_MAX,
                )
            )
        return state

    @engine.bind(["0"])
    def move_beginning_of_line(event: KeyPressEvent, state: EngineState) -> EngineState:
        if event.has_repeat:
            raise ValueError(
                "Cannot have beginning of line with number != 1 \n\n" + repr(state)
            )
        return state.copy(
            cursor=state.cursor.copy(
                col=1,
                col_want=1,
            )
        )

    @engine.bind(["G"])
    def move_end_of_file(event: KeyPressEvent, state: EngineState) -> EngineState:
        new_line = event.get_repeat(default=len(state.buffer))
        # TODO : It starts at the first non-space character.
        new_lnum = clamp(new_line, 0, len(state.buffer))
        new_col_num = BufferHelper.get_first_non_space_char(state, new_lnum)
        return state.copy(
            cursor=state.cursor.copy(
                line=new_lnum,
                col=new_col_num,
                col_want=new_col_num,
            )
        )
        return state

    @engine.bind(["g", "g"])
    def move_beginning_of_file(event: KeyPressEvent, state: EngineState) -> EngineState:
        new_line = event.get_repeat()
        new_lnum = clamp(new_line, 0, len(state.buffer))
        new_col_num = BufferHelper.get_first_non_space_char(state, new_lnum)
        return state.copy(
            cursor=state.cursor.copy(
                line=new_lnum,
                col=new_col_num,
                col_want=new_col_num,
            )
        )

    @engine.bind(["d", "d"])
    def delete_line(event: KeyPressEvent, state: EngineState) -> EngineState:
        repeat = event.get_repeat()
        new_buffer = (
            state.buffer[0 : state.cursor.line - 1] + state.buffer[state.cursor.line :]
        )
        return state.copy(buffer=new_buffer)

    @engine.bind(["x"])
    def delete_char_under_cursor(
        event: KeyPressEvent, state: EngineState
    ) -> EngineState:
        repeat = event.get_repeat()
        old_line = state.buffer[state.cursor.line - 1]
        new_line = old_line[0 : state.cursor.col - 1] + old_line[state.cursor.col :]
        new_cursor_col = min(state.cursor.col, len(new_line))

        new_buffer = (
            *state.buffer[0 : state.cursor.line - 1],
            new_line,
            *state.buffer[state.cursor.line :],
        )

        return state.copy(
            buffer=new_buffer,
            cursor=state.cursor.copy(
                col=new_cursor_col,
            ),
        )
