#!/usr/bin/python3
"""Module that defines LockedClass, a class restricting instance attributes."""


class LockedClass:
    """Class that only allows setting an instance attribute named first_name.

    Any attempt to create another attribute on an instance raises
    an AttributeError because __slots__ blocks dynamic attributes.
    """
    __slots__ = ["first_name"]
