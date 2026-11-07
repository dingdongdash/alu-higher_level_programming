#!/usr/bin/python3
"""Module that defines a list subclass able to print itself sorted."""


class MyList(list):
    """List subclass that can print its items in ascending order."""

    def print_sorted(self):
        """Print the items of the list sorted, leaving the list unchanged."""
        print(sorted(self))
