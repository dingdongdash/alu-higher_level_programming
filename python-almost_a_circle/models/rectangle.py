#!/usr/bin/python3
"""Module that defines the Rectangle class, a shape that inherits Base.

The Rectangle class validates its dimensions and its position and knows how
to describe itself, to compute its area and to display itself with hashes.
"""
from models.base import Base


class Rectangle(Base):
    """Rectangle class with a width, a height and a position.

    Every attribute is private and is exposed through a validated property.
    """

    def __init__(self, width, height, x=0, y=0, id=None):
        """Initialize the rectangle after the identifier of the Base class."""
        super().__init__(id)
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    @property
    def width(self):
        """Get the width of the rectangle."""
        return self.__width

    @width.setter
    def width(self, value):
        """Set the width after checking that it is a positive integer."""
        if type(value) is not int:
            raise TypeError("width must be an integer")
        if value <= 0:
            raise ValueError("width must be > 0")
        self.__width = value

    @property
    def height(self):
        """Get the height of the rectangle."""
        return self.__height

    @height.setter
    def height(self, value):
        """Set the height after checking that it is a positive integer."""
        if type(value) is not int:
            raise TypeError("height must be an integer")
        if value <= 0:
            raise ValueError("height must be > 0")
        self.__height = value

    @property
    def x(self):
        """Get the horizontal position of the rectangle."""
        return self.__x

    @x.setter
    def x(self, value):
        """Set the horizontal position after checking that it is valid."""
        if type(value) is not int:
            raise TypeError("x must be an integer")
        if value < 0:
            raise ValueError("x must be >= 0")
        self.__x = value

    @property
    def y(self):
        """Get the vertical position of the rectangle."""
        return self.__y

    @y.setter
    def y(self, value):
        """Set the vertical position after checking that it is valid."""
        if type(value) is not int:
            raise TypeError("y must be an integer")
        if value < 0:
            raise ValueError("y must be >= 0")
        self.__y = value

    def area(self):
        """Return the area of the rectangle."""
        return self.width * self.height

    def display(self):
        """Print the rectangle with the character # in the standard output.

        The position is respected with empty lines above and spaces before.
        """
        print("\n" * self.y, end="")
        for _ in range(self.height):
            print(" " * self.x + "#" * self.width)

    def __str__(self):
        """Return the text description of the rectangle."""
        return "[Rectangle] ({}) {}/{} - {}/{}".format(
            self.id, self.x, self.y, self.width, self.height)

    def update(self, *args, **kwargs):
        """Assign the arguments to the attributes of the rectangle.

        The positional arguments are used in the order id, width, height, x
        and y. The keyword arguments are skipped if positional ones exist.
        """
        names = ("id", "width", "height", "x", "y")
        if args:
            for name, value in zip(names, args):
                setattr(self, name, value)
            return
        for name in names:
            if name in kwargs:
                setattr(self, name, kwargs[name])

    def to_dictionary(self):
        """Return the dictionary representation of the rectangle."""
        return {"id": self.id, "width": self.width, "height": self.height,
                "x": self.x, "y": self.y}
