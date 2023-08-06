"""
Map between code received and a text representing the code launched.
"""
import collections
import enum
import string
from typing import List

from vim_quest_cli.deps.prompt_toolkit import keys, ansi_escape_sequences

OUTSIDE_OF_ENUM = set(string.ascii_lowercase + string.ascii_uppercase + string.digits)

Keys = keys.Keys

__all__ = [
    "Keys",  # From vim library instead of the prompt one.
    "input_to_keys",
]

PRINTABLE = frozenset(string.printable)


def input_to_keys(input: str):
    """Right now we expect the input_code to contain only one and only one command.
    TODO: For later handle multiples commands that could be included in the input_code.
    This may happen on older system or when the tool become too heavy.

    I think a better way to handle it would be to not have latency while reading stdin.
    But it would only works for typped input. When doing copy-paste, this woudn't work at all.

    I guess we need both, multiprocess input and management of longer inputs when copy-pasting.
    """
    if not input:
        return []
    if input in ansi_escape_sequences.ANSI_SEQUENCES:
        return [ansi_escape_sequences.ANSI_SEQUENCES[input]]
    return [input]
