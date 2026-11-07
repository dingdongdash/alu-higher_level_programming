#!/usr/bin/python3
"""Module that defines a square class based on the rectangle class."""
Rectangle = __import__('9-rectangle').Rectangle


class Square(Rectangle):
    """Square with a private size, built on top of the rectangle class."""

    def __init__(self, size):
        """Create a square after validating its size."""
        self.integer_validator("size", size)
        super().__init__(size, size)
        self.__size = size

    def area(self):
        """Return the area of the square."""
        return self.__size * self.__size
