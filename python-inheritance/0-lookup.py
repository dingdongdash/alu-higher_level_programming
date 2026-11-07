#!/usr/bin/python3
"""Module that provides a function listing the attributes of an object."""


def lookup(obj):
    """Return the list of available attributes and methods of an object."""
    return dir(obj)
