#!/usr/bin/python3
"""Module that defines a function describing an object as a dictionary."""


def class_to_json(obj):
    """Return the dictionary description of an object for serialization."""
    return obj.__dict__
