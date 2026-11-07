#!/usr/bin/python3
"""Module that defines the Square class, a rectangle with equal sides.

The Square class reuses the attributes of the Rectangle class and exposes
the size of its sides through a single property.
"""
from models.rectangle import Rectangle


class Square(Rectangle):
    """Square class whose width and height are always the same size."""

    def __init__(self, size, x=0, y=0, id=None):
        """Initialize the square with the Rectangle constructor."""
        super().__init__(size, size, x, y, id)

    @property
    def size(self):
        """Get the size of the square."""
        return self.width

    @size.setter
    def size(self, value):
        """Set the width and the height of the square to the same value."""
        self.width = value
        self.height = value

    def __str__(self):
        """Return the text description of the square."""
        return "[Square] ({}) {}/{} - {}".format(
            self.id, self.x, self.y, self.width)

    def update(self, *args, **kwargs):
        """Assign the arguments to the attributes of the square.

        The positional arguments are used in the order id, size, x and y.
        The keyword arguments are skipped if positional ones exist.
        """
        names = ("id", "size", "x", "y")
        if args:
            for name, value in zip(names, args):
                setattr(self, name, value)
            return
        for name in names:
            if name in kwargs:
                setattr(self, name, kwargs[name])

    def to_dictionary(self):
        """Return the dictionary representation of the square."""
        return {"id": self.id, "size": self.size, "x": self.x, "y": self.y}
