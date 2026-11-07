#!/usr/bin/python3
"""This module defines a Square class that can be compared by its area."""


class Square:
    """This class defines a square that is compared to others by its area."""

    def __init__(self, size=0):
        """Initialize a new square by passing size through the size setter.

        Args:
            size: The length of one side of the square, a non-negative number.
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
            value: The new length of one side, a non-negative number.

        Raises:
            TypeError: If value is not a float or an integer.
            ValueError: If value is less than zero.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("size must be a number")
        if value < 0:
            raise ValueError("size must be >= 0")
        self.__size = value

    def area(self):
        """Return the current area of the square, which is size squared."""
        return self.__size ** 2

    def __eq__(self, other):
        """Return True if both squares have the same area."""
        return self.area() == other.area()

    def __ne__(self, other):
        """Return True if the squares do not have the same area."""
        return self.area() != other.area()

    def __lt__(self, other):
        """Return True if this square has a smaller area than the other."""
        return self.area() < other.area()

    def __le__(self, other):
        """Return True if this square area is at most that of the other."""
        return self.area() <= other.area()

    def __gt__(self, other):
        """Return True if this square has a larger area than the other."""
        return self.area() > other.area()

    def __ge__(self, other):
        """Return True if this square area is at least that of the other."""
        return self.area() >= other.area()
