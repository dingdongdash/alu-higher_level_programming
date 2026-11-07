#!/usr/bin/python3
"""This module defines a Square class that stores a private size."""


class Square:
    """This class defines a square by storing its size privately."""

    def __init__(self, size):
        """Initialize a new square with the given size, unchecked."""
        self.__size = size
