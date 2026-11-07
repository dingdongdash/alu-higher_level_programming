#!/usr/bin/python3
"""This module defines a Square class that can compute its own area."""


class Square:
    """This class defines a square with a validated size and an area."""

    def __init__(self, size=0):
        """Initialize a new square after checking the type and value of size.

        Args:
            size: The length of one side of the square, a non-negative integer.

        Raises:
            TypeError: If size is not an integer.
            ValueError: If size is less than zero.
        """
        if not isinstance(size, int):
            raise TypeError("size must be an integer")
        if size < 0:
            raise ValueError("size must be >= 0")
        self.__size = size

    def area(self):
        """Return the current area of the square, which is size squared."""
        return self.__size ** 2
