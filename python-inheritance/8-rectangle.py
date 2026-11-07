#!/usr/bin/python3
"""Module that defines a rectangle class based on the geometry class."""
BaseGeometry = __import__('7-base_geometry').BaseGeometry


class Rectangle(BaseGeometry):
    """Rectangle with a private width and a private height."""

    def __init__(self, width, height):
        """Create a rectangle after validating its width and its height."""
        self.integer_validator("width", width)
        self.__width = width
        self.integer_validator("height", height)
        self.__height = height
