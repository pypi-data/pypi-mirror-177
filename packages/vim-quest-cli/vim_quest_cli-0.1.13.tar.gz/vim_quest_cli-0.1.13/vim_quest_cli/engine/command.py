"""
Common process around the commands and what format they have.

"""
import enum
import string

ALL_RAW = set(string.printable)


@enum.Enum
class KeyEnum:
    LEFT = "<Left>"
    RIGHT = "<Right>"
    UP = "<Up>"
    DOWN = "<Down>"
