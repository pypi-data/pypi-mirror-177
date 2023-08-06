"""
Idea : enemies come at you. You have to delete the text they are on to be able to survive.
Once you got all the enemies, more are coming.

Enemies pop-up : Randomly, not too close to the user (leave 8 of security).
Enemies move : get all the enemies, the closests ones are to move the first (use x+y instead of sqrt).
               When they move they pop-up behind the text they were working with.
               Then they move to the closest x/y to you. If both are similar, do it randomly.
"""
import random

from vim_quest_cli.engine.engine_interface import CursorPos, EngineState
from vim_quest_cli.mode.mode_container import ModeElement
from vim_quest_cli.view.view import FgColor, ViewData

TEXT = (
    "Quisque eu sagittis lacus. Vestibulum in augue tortor. In feugiat enim"
    " massa, ut dignissim sem elementum et. Pellentesque suscipit egestas q"
    "uam egestas blandit. Suspendisse potenti. Cras eleifend dui ut diam lo"
    "bortis rhoncus. Praesent sollicitudin sed sem sed varius. Integer semp"
    "er mi id nunc fringilla, ac malesuada nunc imperdiet. Nulla maximus do"
    "lor in ligula ultrices accumsan et eu urna. Vestibulum at luctus lacus"
    ", eget gravida mauris. Aliquam scelerisque est in massa sollicitudin c"
    "ondimentum. Mauris malesuada velit libero, nec tempor nisi consectetur"
    " et. Donec gravida auctor lectus, ac viverra nunc dictum in. Vestibulu"
    "m auctor ipsum sit amet nulla pellentesque, at pharetra mi scelerisque"
    ". Suspendisse neque lorem, bibendum sed mollis in, egestas nec neque. "
    "Proin magna diam, laoreet nec justo et, vehicula vulputate arcu."
)


class EnemiesComingAtYou(ModeElement):
    _step_counts: int = 0

    def _reset_terrain(
        self, state: EngineState, reset_cursor=False, lost=False
    ) -> EngineState:

        if lost:
            self._step_counts = 0
        self._step_counts += 1

        # First empty the state.
        nb_lines, nb_cols = 14, 40
        text = "Don't let the X go to you, delete them before (dd to delete a line)."
        new_buffer = [["."] * nb_cols for _ in range(nb_lines)]
        for _ in range(self._step_counts):
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

        return state.copy(buffer=new_buffer, cursor=cursor)

    def _init_after_params(self):
        self._state = self._reset_terrain(self._state, reset_cursor=True)

    def change_view(self, view: ViewData) -> ViewData:
        for _, _, character in view.loop_chars_generator():
            if character.ascii == "X":
                character.fg_color = FgColor.red
        return view

    def state_change(
        self, state_init: EngineState, state_end: EngineState
    ) -> EngineState:
        c_line, c_col = state_end.cursor.line, state_end.cursor.col

        # Get all the X in the map
        all_x = [
            (line, col, char)
            for line, col, char in state_end.character_buffer_generator()
            if char == "X" and line != 1
        ]
        if not all_x:
            return self._reset_terrain(state_end)

        # Sort all enemies by distance
        def distance_to_cursor(e):
            e_line, e_col, e_char = e
            return abs(c_line - e_line) + abs(c_col - e_col)

        new_buffer = state_end.get_mutable_buffer_copy()

        # Now move them one by one
        def move_char(e_line, e_col, new_e_line, new_e_col):
            # Swap the two places in the buffer
            (
                new_buffer[new_e_line - 1][new_e_col - 1],
                new_buffer[e_line - 1][e_col - 1],
            ) = (
                new_buffer[e_line - 1][e_col - 1],
                new_buffer[new_e_line - 1][new_e_col - 1],
            )

        for e_line, e_col, e_char in sorted(all_x, key=distance_to_cursor):
            if e_line == c_line and e_col == c_col:
                return self._reset_terrain(state_end, lost=True)
            # Try to go to the line first

            possible_move = []
            if e_line != c_line:
                new_e_line = e_line + 1 if e_line < c_line else e_line - 1
                possible_move.append((new_e_line, e_col))
            if e_col != c_col:
                new_e_col = e_col + 1 if e_col < c_col else e_col - 1
                possible_move.append((e_line, new_e_col))
            if not possible_move or random.random() < 0.2:  # 20%
                continue
            new_e_line, new_e_col = random.choice(possible_move)
            move_char(e_line, e_col, new_e_line, new_e_col)

            if new_e_line == c_line and new_e_col == c_col:
                return self._reset_terrain(state_end, lost=True)

        return state_end.copy(buffer=new_buffer)
