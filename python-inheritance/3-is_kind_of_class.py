#!/usr/bin/python3
"""Module that provides a function checking the kind of class of an object."""


def is_kind_of_class(obj, a_class):
    """Return True if obj is an instance of a_class or of a subclass of it."""
    return isinstance(obj, a_class)
