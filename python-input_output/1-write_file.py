#!/usr/bin/python3
"""Module that defines a function writing a string to a text file."""


def write_file(filename="", text=""):
    """Write a string to a UTF8 text file and return the characters written.

    The file is created when it does not exist and overwritten otherwise.
    """
    with open(filename, "w", encoding="utf-8") as f:
        return f.write(text)
