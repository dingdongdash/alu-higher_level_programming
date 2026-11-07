#!/usr/bin/python3
"""This module defines a Rectangle class that counts its instances."""


class Rectangle:
    """A rectangle with a width and a height."""

    number_of_instances = 0

    def __init__(self, width=0, height=0):
        """Initialize a rectangle and count it as a new instance."""
        Rectangle.number_of_instances += 1
        self.width = width
        self.height = height

    @property
    def width(self):
        """Get the width of the rectangle."""
        return self.__width

    @width.setter
    def width(self, value):
        """Set the width, which must be an integer >= 0."""
        if not isinstance(value, int):
            raise TypeError("width must be an integer")
        if value < 0:
            raise ValueError("width must be >= 0")
        self.__width = value

    @property
    def height(self):
        """Get the height of the rectangle."""
        return self.__height

    @height.setter
    def height(self, value):
        """Set the height, which must be an integer >= 0."""
        if not isinstance(value, int):
            raise TypeError("height must be an integer")
        if value < 0:
            raise ValueError("height must be >= 0")
        self.__height = value

    def area(self):
        """Return the area of the rectangle."""
        return self.width * self.height

    def perimeter(self):
        """Return the perimeter of the rectangle, 0 if a side is 0."""
        if self.width == 0 or self.height == 0:
            return 0
        return 2 * (self.width + self.height)

    def __str__(self):
        """Return the rectangle drawn with # characters."""
        if self.width == 0 or self.height == 0:
            return ""
        return "\n".join(["#" * self.width] * self.height)

    def __repr__(self):
        """Return a string that eval() turns into a new rectangle."""
        return "Rectangle({:d}, {:d})".format(self.width, self.height)

    def __del__(self):
        """Print a message and count one instance less."""
        Rectangle.number_of_instances -= 1
        print("Bye rectangle...")
