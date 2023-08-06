"""
Return a text code for every input.
"""
import fcntl
import os
import select
import sys
import termios
import tty

from vim_quest_cli.deps import stdin_reader


# compaint_number : 221109-4297797


def main():
    with stdin_reader.stdin_key_reader_ctx() as read_fct:
        print("Starting stdin tests >\r")
        while True:
            v = read_fct()
            print(f"{v!r}\r")
            if v == "q":
                return


if __name__ == "__main__":
    main()
