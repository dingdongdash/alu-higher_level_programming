#!/usr/bin/python3
"""Module that defines a function adding a new attribute to an object."""


def add_attribute(obj, name, value):
    """Add a new attribute to an object when the object supports attributes.

    Raise a TypeError with the message can't add new attribute when the
    object has no instance dictionary and so cannot store a new attribute.
    """
    if not hasattr(obj, "__dict__"):
        raise TypeError("can't add new attribute")
    setattr(obj, name, value)
