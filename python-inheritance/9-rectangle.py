#!/usr/bin/python3
"""Module that defines a rectangle class able to compute its area."""
BaseGeometry = __import__('7-base_geometry').BaseGeometry


class Rectangle(BaseGeometry):
    """Rectangle with a private width and a private height."""

    def __init__(self, width, height):
        """Create a rectangle after validating its width and its height."""
        self.integer_validator("width", width)
        self.__width = width
        self.integer_validator("height", height)
        self.__height = height

    def area(self):
        """Return the area of the rectangle."""
        return self.__width * self.__height

    def __str__(self):
        """Return the description of the rectangle as [Rectangle] w/h."""
        return "[Rectangle] {}/{}".format(self.__width, self.__height)
