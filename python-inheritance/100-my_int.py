#!/usr/bin/python3
"""Module that defines MyInt, an integer class with inverted comparisons."""


class MyInt(int):
    """Integer class whose equality operators behave the opposite way."""

    def __eq__(self, other):
        """Return True when the values differ and False when they match."""
        return super().__ne__(other)

    def __ne__(self, other):
        """Return True when the values match and False when they differ."""
        return super().__eq__(other)

    __hash__ = int.__hash__
