#!/usr/bin/python3
"""This module defines a Square class that can print itself with hashes."""


class Square:
    """This class defines a square that can compute its area and print."""

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

    def my_print(self):
        """Print the square to stdout using the character #.

        An empty line is printed when the size of the square is 0.
        """
        if self.__size == 0:
            print()
            return
        for _ in range(self.__size):
            print("#" * self.__size)
