#!/usr/bin/python3
"""Module that defines a geometry class with an unimplemented area."""


class BaseGeometry:
    """Base class that is meant to describe geometric shapes."""

    def area(self):
        """Raise an exception because the area is not implemented here."""
        raise Exception("area() is not implemented")
