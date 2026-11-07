#!/usr/bin/python3
"""Module that inserts a line of text after each line containing a string."""


def append_after(filename="", search_string="", new_string=""):
    """Insert new_string in the file after each line holding search_string.

    A line break is added first when the matching line is the last line of
    the file and does not end with one.
    """
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line)
            if search_string in line:
                if not line.endswith("\n"):
                    f.write("\n")
                f.write(new_string)
