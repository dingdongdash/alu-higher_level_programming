#!/usr/bin/python3
"""Module that defines a geometry class able to validate integers."""


class BaseGeometry:
    """Base class that is meant to describe geometric shapes."""

    def area(self):
        """Raise an exception because the area is not implemented here."""
        raise Exception("area() is not implemented")

    def integer_validator(self, name, value):
        """Check that value is a strictly positive integer named name.

        Raise a TypeError if value is not an integer and a ValueError if
        value is not greater than zero.
        """
        if type(value) is not int:
            raise TypeError("{} must be an integer".format(name))
        if value <= 0:
            raise ValueError("{} must be greater than 0".format(name))
