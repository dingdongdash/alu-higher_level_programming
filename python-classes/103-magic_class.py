#!/usr/bin/python3
"""This module defines a MagicClass that computes properties of a circle."""
import math


class MagicClass:
    """This class defines a circle that is described by its radius."""

    def __init__(self, radius=0):
        """Initialize a new circle after validating the given radius.

        Args:
            radius: The radius of the circle, an integer or a float.

        Raises:
            TypeError: If the type of radius is neither int nor float.
        """
        self.__radius = 0
        if type(radius) is not int and type(radius) is not float:
            raise TypeError("radius must be a number")
        self.__radius = radius

    def area(self):
        """Return the area of the circle, which is radius squared times pi."""
        return self.__radius ** 2 * math.pi

    def circumference(self):
        """Return the circumference of the circle, 2 times pi times radius."""
        return 2 * math.pi * self.__radius
