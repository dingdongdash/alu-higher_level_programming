#!/usr/bin/python3
"""Module for the add_integer function.

This module defines a function that adds two numbers.
Floating point arguments are first casted to integers.
A TypeError is raised when an argument is not a number.
"""


def add_integer(a, b=98):
    """Add two numbers and return the integer result.

    Both arguments must be integers or floats and floats are casted.
    A TypeError is raised when a or b is not an integer or a float.
    """
    if not isinstance(a, (int, float)):
        raise TypeError("a must be an integer")
    if not isinstance(b, (int, float)):
        raise TypeError("b must be an integer")
    return int(a) + int(b)
