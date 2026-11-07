#!/usr/bin/python3
"""This module defines a Square class with a property for its size."""


class Square:
    """This class defines a square whose size is read and set by property."""

    def __init__(self, size=0):
        """Initialize a new square by passing size through the size setter.

        Args:
            size: The length of one side of the square, a non-negative integer.
        """
        self.size = size

    @property
    def size(self):
        """Retrieve the current size of the square."""
        return self.__size

    @size.setter
    def size(self, value):
        """Set the size of the square after validating the given value.

        Args:
            value: The new length of one side, a non-negative integer.

        Raises:
            TypeError: If value is not an integer.
            ValueError: If value is less than zero.
        """
        if not isinstance(value, int):
            raise TypeError("size must be an integer")
        if value < 0:
            raise ValueError("size must be >= 0")
        self.__size = value

    def area(self):
        """Return the current area of the square, which is size squared."""
        return self.__size ** 2
