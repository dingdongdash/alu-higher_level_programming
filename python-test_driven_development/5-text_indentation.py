#!/usr/bin/python3
"""Module for the text_indentation function.

This module defines a function that prints a text with indentation.
Two new lines are printed after each dot, question mark and colon.
No printed line starts or ends with a space.
"""


def text_indentation(text):
    """Print a text with two new lines after each of the characters . ? and :

    The text must be a string, otherwise a TypeError is raised.
    Spaces at the beginning and at the end of each line are removed.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    line = ""
    for char in text:
        line += char
        if char in ".?:":
            print(line.strip(), end="\n\n")
            line = ""
    print(line.strip(), end="")
