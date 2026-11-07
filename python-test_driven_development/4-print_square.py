#!/usr/bin/python3
"""Module for the print_square function.

This module defines a function that prints a square.
The square is drawn with the character hash and a given size.
A size that is not an integer or that is negative raises an error.
"""


def print_square(size):
    """Print a square of the given size using the character hash.

    The size must be an integer, otherwise a TypeError is raised.
    A negative size raises a ValueError and a size of zero prints nothing.
    """
    if not isinstance(size, int):
        raise TypeError("size must be an integer")
    if size < 0:
        raise ValueError("size must be >= 0")
    for _ in range(size):
        print("#" * size)
