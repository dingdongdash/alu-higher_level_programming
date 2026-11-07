#!/usr/bin/python3
"""Module for the say_my_name function.

This module defines a function that prints a full name.
The first name and the last name must both be strings.
The last name is optional and is empty when it is not given.
"""


def say_my_name(first_name, last_name=""):
    """Print the sentence My name is followed by a first and last name.

    Both names must be strings, otherwise a TypeError is raised.
    The first name is checked before the last name.
    """
    if not isinstance(first_name, str):
        raise TypeError("first_name must be a string")
    if not isinstance(last_name, str):
        raise TypeError("last_name must be a string")
    print("My name is {} {}".format(first_name, last_name))
