#!/usr/bin/python3
"""This module defines a Square class that can be printed at a position."""


class Square:
    """This class defines a square with a size and a printing position."""

    def __init__(self, size=0, position=(0, 0)):
        """Initialize a new square by passing both values through setters.

        Args:
            size: The length of one side of the square, a non-negative integer.
            position: A tuple of 2 non-negative integers giving the offset.
        """
        self.size = size
        self.position = position

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

    @property
    def position(self):
        """Retrieve the current position of the square as a tuple."""
        return self.__position

    @position.setter
    def position(self, value):
        """Set the position of the square after validating the given value.

        Args:
            value: A tuple of 2 non-negative integers giving the offset.

        Raises:
            TypeError: If value is not a tuple of 2 non-negative integers.
        """
        if (not isinstance(value, tuple) or len(value) != 2 or
                not all(isinstance(n, int) for n in value) or
                value[0] < 0 or value[1] < 0):
            raise TypeError("position must be a tuple of 2 positive integer")
        self.__position = value

    def area(self):
        """Return the current area of the square, which is size squared."""
        return self.__size ** 2

    def my_print(self):
        """Print the square to stdout using the character # at its position.

        An empty line is printed when the size of the square is 0. Otherwise
        position[1] blank lines come first and each row is indented by
        position[0] spaces.
        """
        print(self)

    def __str__(self):
        """Return the square drawn with the character # at its position.

        The returned text has no trailing newline, so printing the square
        gives the same output as calling the my_print method.
        """
        if self.__size == 0:
            return ""
        rows = [" " * self.__position[0] + "#" * self.__size] * self.__size
        return "\n" * self.__position[1] + "\n".join(rows)
