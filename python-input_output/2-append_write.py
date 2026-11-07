#!/usr/bin/python3
"""Module that defines a function appending a string to a text file."""


def append_write(filename="", text=""):
    """Append a string at the end of a UTF8 text file and return its length.

    The file is created when it does not exist yet.
    """
    with open(filename, "a", encoding="utf-8") as f:
        return f.write(text)
