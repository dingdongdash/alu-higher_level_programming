#!/usr/bin/python3
"""Unit tests for the Square class of the models package.

The tests cover the constructor, the size property, the validation rules, the
inherited methods, the update, the dictionary representation, the text
description and the JSON helpers and file methods used by squares.
"""
import inspect
import io
import json
import os
import unittest
from unittest.mock import patch

from models.base import Base
from models.rectangle import Rectangle
from models.square import Square


def reset_counter():
    """Reset the private counter of the Base class to zero."""
    Base._Base__nb_objects = 0


def remove_json_files():
    """Delete the JSON files that the save methods may have created."""
    for name in ("Base.json", "Rectangle.json", "Square.json"):
        if os.path.exists(name):
            os.remove(name)


def captured(function):
    """Return the text that a function prints in the standard output."""
    buffer = io.StringIO()
    with patch("sys.stdout", new=buffer):
        function()
    return buffer.getvalue()


def read_file(name):
    """Return the whole text stored in a file."""
    with open(name, "r") as file:
        return file.read()


def write_file(name, text):
    """Replace the content of a file with a text."""
    with open(name, "w") as file:
        file.write(text)


class SpySquare(Square):
    """Square that records the order in which its sides are assigned."""

    calls = []

    def _set_width(self, value):
        """Record the assignment of the width and then perform it."""
        SpySquare.calls.append("width")
        Rectangle.width.fset(self, value)

    def _set_height(self, value):
        """Record the assignment of the height and then perform it."""
        SpySquare.calls.append("height")
        Rectangle.height.fset(self, value)

    width = property(Rectangle.width.fget, _set_width)
    height = property(Rectangle.height.fget, _set_height)


class TestSquareInit(unittest.TestCase):
    """Tests of the constructor of Square."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_main_example_ids(self):
        """Check the ids of the project example."""
        s1 = Square(5)
        s2 = Square(2, 2)
        s3 = Square(3, 1, 3)
        self.assertEqual((s1.id, s2.id, s3.id), (1, 2, 3))

    def test_attribute_order(self):
        """Check that the arguments go to the right attributes."""
        s1 = Square(1, 2, 3, 4)
        self.assertEqual((s1.size, s1.x, s1.y, s1.id), (1, 2, 3, 4))

    def test_width_and_height_equal_size(self):
        """Check that width and height receive the size."""
        s1 = Square(7)
        self.assertEqual((s1.width, s1.height, s1.size), (7, 7, 7))

    def test_default_position(self):
        """Check that x and y default to zero."""
        s1 = Square(5)
        self.assertEqual((s1.x, s1.y), (0, 0))

    def test_default_y(self):
        """Check that y defaults to zero when x is given."""
        s1 = Square(5, 2)
        self.assertEqual((s1.x, s1.y), (2, 0))

    def test_keyword_arguments(self):
        """Check that the constructor accepts keyword arguments."""
        s1 = Square(id=4, y=3, x=2, size=1)
        self.assertEqual((s1.size, s1.x, s1.y, s1.id), (1, 2, 3, 4))

    def test_generated_ids(self):
        """Check that generated ids increase by one."""
        ids = [Square(1).id for _ in range(4)]
        self.assertEqual(ids, [1, 2, 3, 4])

    def test_explicit_id_keeps_counter(self):
        """Check that an explicit id does not use the counter."""
        Square(1, 0, 0, 12)
        self.assertEqual(Square(1).id, 1)

    def test_shares_counter_with_rectangle(self):
        """Check that Square and Rectangle share the id counter."""
        r1 = Rectangle(1, 1)
        s1 = Square(1)
        r2 = Rectangle(1, 1)
        self.assertEqual((r1.id, s1.id, r2.id), (1, 2, 3))

    def test_is_a_rectangle_and_a_base(self):
        """Check the inheritance chain of an instance."""
        s1 = Square(1)
        self.assertIsInstance(s1, Square)
        self.assertIsInstance(s1, Rectangle)
        self.assertIsInstance(s1, Base)

    def test_subclass_relations(self):
        """Check the inheritance chain of the class."""
        self.assertTrue(issubclass(Square, Rectangle))
        self.assertTrue(issubclass(Square, Base))
        self.assertIs(Square.__bases__[0], Rectangle)

    def test_rectangle_is_not_a_square(self):
        """Check that a rectangle is not a Square."""
        self.assertNotIsInstance(Rectangle(1, 1), Square)

    def test_constructor_signature(self):
        """Check the parameters of the constructor."""
        params = inspect.signature(Square.__init__).parameters
        self.assertEqual(list(params), ["self", "size", "x", "y", "id"])
        self.assertEqual(params["x"].default, 0)
        self.assertEqual(params["y"].default, 0)
        self.assertIsNone(params["id"].default)

    def test_no_new_attributes(self):
        """Check that Square has only the attributes of Rectangle and
        Base."""
        s1 = Square(1, 2, 3, 4)
        expected = {"id", "_Rectangle__width", "_Rectangle__height",
                    "_Rectangle__x", "_Rectangle__y"}
        self.assertEqual(set(s1.__dict__), expected)

    def test_no_private_square_attributes(self):
        """Check that no attribute is private to Square."""
        s1 = Square(1)
        self.assertFalse(any(key.startswith("_Square") for key in s1.__dict__))
        self.assertNotIn("size", s1.__dict__)

    def test_private_values(self):
        """Check the values kept in the private attributes of Rectangle."""
        s1 = Square(6, 7, 8)
        self.assertEqual(s1._Rectangle__width, 6)
        self.assertEqual(s1._Rectangle__height, 6)
        self.assertEqual(s1._Rectangle__x, 7)
        self.assertEqual(s1._Rectangle__y, 8)

    def test_missing_size(self):
        """Check that the size is required."""
        with self.assertRaises(TypeError):
            Square()

    def test_instances_are_not_equal(self):
        """Check that two squares are not equal."""
        s1 = Square(1, 0, 0, 1)
        s2 = Square(1, 0, 0, 1)
        self.assertFalse(s1 == s2)
        self.assertTrue(s1 == s1)

    def test_minimal_values(self):
        """Check the smallest valid size and position."""
        s1 = Square(1, 0, 0)
        self.assertEqual((s1.size, s1.x, s1.y), (1, 0, 0))

    def test_large_values(self):
        """Check that large integers are accepted."""
        s1 = Square(10 ** 9, 10 ** 10, 10 ** 11)
        self.assertEqual((s1.size, s1.x, s1.y), (10 ** 9, 10 ** 10, 10 ** 11))

    def test_inherited_width_and_height_getters(self):
        """Check that width and height come with the inheritance."""
        s1 = Square(4)
        self.assertEqual(s1.width, 4)
        self.assertEqual(s1.height, 4)


class TestSquareSize(unittest.TestCase):
    """Tests of the size property."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_size_is_a_property(self):
        """Check that size is a property."""
        self.assertIsInstance(Square.size, property)
        self.assertIsNotNone(Square.size.fset)

    def test_size_getter(self):
        """Check the getter of the size."""
        self.assertEqual(Square(5).size, 5)

    def test_size_setter(self):
        """Check the setter of the size."""
        s = Square(5)
        s.size = 10
        self.assertEqual(s.size, 10)

    def test_size_setter_changes_width_and_height(self):
        """Check that the setter changes the width and the height."""
        s = Square(5)
        s.size = 10
        self.assertEqual((s.width, s.height), (10, 10))

    def test_size_setter_text(self):
        """Check the text after the size changed."""
        s = Square(5)
        s.size = 10
        self.assertEqual(str(s), "[Square] (1) 0/0 - 10")

    def test_size_setter_keeps_position_and_id(self):
        """Check that the setter keeps the position and the id."""
        s = Square(5, 1, 2, 3)
        s.size = 8
        self.assertEqual((s.x, s.y, s.id), (1, 2, 3))

    def test_size_setter_order(self):
        """Check that the setter assigns the width and then the height."""
        s = SpySquare(3)
        del SpySquare.calls[:]
        s.size = 4
        self.assertEqual(SpySquare.calls, ["width", "height"])
        self.assertEqual((s.width, s.height), (4, 4))

    def test_size_follows_width(self):
        """Check that the size reads the width."""
        s = Square(5)
        s.width = 6
        self.assertEqual(s.size, 6)

    def test_size_follows_update(self):
        """Check that the size follows an update."""
        s = Square(5)
        s.update(1, 9)
        self.assertEqual((s.size, s.width, s.height), (9, 9, 9))

    def test_size_setter_str(self):
        """Check that a string is rejected by the size setter."""
        s = Square(5)

        with self.assertRaises(TypeError) as cm:
            s.size = "1"
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_size_setter_float(self):
        """Check that a float is rejected by the size setter."""
        s = Square(5)

        with self.assertRaises(TypeError) as cm:
            s.size = 1.5
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_size_setter_none(self):
        """Check that None is rejected by the size setter."""
        s = Square(5)

        with self.assertRaises(TypeError) as cm:
            s.size = None
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_size_setter_list(self):
        """Check that a list is rejected by the size setter."""
        s = Square(5)

        with self.assertRaises(TypeError) as cm:
            s.size = [1]
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_size_setter_dict(self):
        """Check that a dictionary is rejected by the size setter."""
        s = Square(5)

        with self.assertRaises(TypeError) as cm:
            s.size = {}
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_size_setter_tuple(self):
        """Check that a tuple is rejected by the size setter."""
        s = Square(5)

        with self.assertRaises(TypeError) as cm:
            s.size = (1,)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_size_setter_set(self):
        """Check that a set is rejected by the size setter."""
        s = Square(5)

        with self.assertRaises(TypeError) as cm:
            s.size = {1}
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_size_setter_inf(self):
        """Check that an infinite float is rejected by the size setter."""
        s = Square(5)

        with self.assertRaises(TypeError) as cm:
            s.size = float("inf")
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_size_setter_nan(self):
        """Check that a NaN float is rejected by the size setter."""
        s = Square(5)

        with self.assertRaises(TypeError) as cm:
            s.size = float("nan")
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_size_setter_value_0(self):
        """Check that the value 0 is rejected by the size setter."""
        s = Square(5)

        with self.assertRaises(ValueError) as cm:
            s.size = 0
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_size_setter_value_minus_1(self):
        """Check that the value -1 is rejected by the size setter."""
        s = Square(5)

        with self.assertRaises(ValueError) as cm:
            s.size = -1
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_size_setter_value_minus_10(self):
        """Check that the value -10 is rejected by the size setter."""
        s = Square(5)

        with self.assertRaises(ValueError) as cm:
            s.size = -10
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_size_setter_negative_float(self):
        """Check that a negative float fails the type check first."""
        s = Square(5)

        with self.assertRaises(TypeError) as cm:
            s.size = -2.5
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_size_setter_numeric_string(self):
        """Check that a numeric string is rejected."""
        s = Square(5)

        with self.assertRaises(TypeError) as cm:
            s.size = "9"
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_size_setter_main_example(self):
        """Check the message of the project example."""
        s = Square(5)

        with self.assertRaises(TypeError) as cm:
            s.size = "9"
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_size_keeps_old_value_after_type_error(self):
        """Check that a rejected type leaves the size unchanged."""
        s = Square(5)
        with self.assertRaises(TypeError):
            s.size = "9"
        self.assertEqual((s.size, s.width, s.height), (5, 5, 5))

    def test_size_keeps_old_value_after_value_error(self):
        """Check that a rejected value leaves the size unchanged."""
        s = Square(5)
        with self.assertRaises(ValueError):
            s.size = -9
        self.assertEqual((s.size, s.width, s.height), (5, 5, 5))

    def test_size_boundary_is_valid(self):
        """Check that a size of 1 is accepted."""
        s = Square(5)
        s.size = 1
        self.assertEqual((s.width, s.height), (1, 1))


class TestSquareValidation(unittest.TestCase):
    """Tests of the validation of Square."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_constructor_size_str(self):
        """Check that a string for size is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square("1")
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_constructor_size_float(self):
        """Check that a float for size is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1.5)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_constructor_size_none(self):
        """Check that None for size is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(None)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_constructor_size_list(self):
        """Check that a list for size is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square([1])
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_constructor_size_dict(self):
        """Check that a dictionary for size is rejected by the
        constructor."""
        with self.assertRaises(TypeError) as cm:
            Square({})
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_constructor_size_tuple(self):
        """Check that a tuple for size is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square((1,))
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_constructor_size_set(self):
        """Check that a set for size is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square({1})
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_constructor_size_inf(self):
        """Check that an infinite float for size is rejected by the
        constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(float("inf"))
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_constructor_size_nan(self):
        """Check that a NaN float for size is rejected by the
        constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(float("nan"))
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_constructor_x_str(self):
        """Check that a string for x is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, "1")
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_constructor_x_float(self):
        """Check that a float for x is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, 1.5)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_constructor_x_none(self):
        """Check that None for x is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, None)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_constructor_x_list(self):
        """Check that a list for x is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, [1])
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_constructor_x_dict(self):
        """Check that a dictionary for x is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, {})
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_constructor_x_tuple(self):
        """Check that a tuple for x is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, (1,))
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_constructor_x_set(self):
        """Check that a set for x is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, {1})
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_constructor_x_inf(self):
        """Check that an infinite float for x is rejected by the
        constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, float("inf"))
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_constructor_x_nan(self):
        """Check that a NaN float for x is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, float("nan"))
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_constructor_y_str(self):
        """Check that a string for y is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, 2, "1")
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_constructor_y_float(self):
        """Check that a float for y is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, 2, 1.5)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_constructor_y_none(self):
        """Check that None for y is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, 2, None)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_constructor_y_list(self):
        """Check that a list for y is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, 2, [1])
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_constructor_y_dict(self):
        """Check that a dictionary for y is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, 2, {})
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_constructor_y_tuple(self):
        """Check that a tuple for y is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, 2, (1,))
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_constructor_y_set(self):
        """Check that a set for y is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, 2, {1})
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_constructor_y_inf(self):
        """Check that an infinite float for y is rejected by the
        constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, 2, float("inf"))
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_constructor_y_nan(self):
        """Check that a NaN float for y is rejected by the constructor."""
        with self.assertRaises(TypeError) as cm:
            Square(1, 2, float("nan"))
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_constructor_size_value_0(self):
        """Check that the value 0 for size is rejected by the
        constructor."""
        with self.assertRaises(ValueError) as cm:
            Square(0)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_constructor_size_value_minus_1(self):
        """Check that the value -1 for size is rejected by the
        constructor."""
        with self.assertRaises(ValueError) as cm:
            Square(-1)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_constructor_size_value_minus_10(self):
        """Check that the value -10 for size is rejected by the
        constructor."""
        with self.assertRaises(ValueError) as cm:
            Square(-10)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_constructor_x_value_minus_1(self):
        """Check that the value -1 for x is rejected by the constructor."""
        with self.assertRaises(ValueError) as cm:
            Square(1, -1)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_constructor_x_value_minus_10(self):
        """Check that the value -10 for x is rejected by the constructor."""
        with self.assertRaises(ValueError) as cm:
            Square(1, -10)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_constructor_y_value_minus_1(self):
        """Check that the value -1 for y is rejected by the constructor."""
        with self.assertRaises(ValueError) as cm:
            Square(1, 2, -1)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_constructor_y_value_minus_10(self):
        """Check that the value -10 for y is rejected by the constructor."""
        with self.assertRaises(ValueError) as cm:
            Square(1, 2, -10)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_constructor_size_negative_float(self):
        """Check that a negative float for size fails the type check
        first."""
        with self.assertRaises(TypeError) as cm:
            Square(-1.5)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_constructor_x_negative_float(self):
        """Check that a negative float for x fails the type check first."""
        with self.assertRaises(TypeError) as cm:
            Square(1, -1.5)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_constructor_y_negative_float(self):
        """Check that a negative float for y fails the type check first."""
        with self.assertRaises(TypeError) as cm:
            Square(1, 2, -1.5)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_setter_x_str(self):
        """Check that a string for x is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.x = "1"
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_setter_x_float(self):
        """Check that a float for x is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.x = 1.5
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_setter_x_none(self):
        """Check that None for x is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.x = None
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_setter_x_list(self):
        """Check that a list for x is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.x = [1]
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_setter_x_dict(self):
        """Check that a dictionary for x is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.x = {}
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_setter_x_tuple(self):
        """Check that a tuple for x is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.x = (1,)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_setter_x_value_minus_1(self):
        """Check that the value -1 for x is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.x = -1
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_setter_x_value_minus_10(self):
        """Check that the value -10 for x is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.x = -10
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_setter_x_boundary(self):
        """Check that x of 0 is accepted."""
        s = Square(5, 3, 4)
        s.x = 0
        self.assertEqual(s.x, 0)

    def test_setter_x_keeps_old_value(self):
        """Check that a rejected value leaves x unchanged."""
        s = Square(5, 3, 4)
        with self.assertRaises(ValueError):
            s.x = -1
        self.assertEqual(s.x, 3)

    def test_setter_y_str(self):
        """Check that a string for y is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.y = "1"
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_setter_y_float(self):
        """Check that a float for y is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.y = 1.5
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_setter_y_none(self):
        """Check that None for y is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.y = None
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_setter_y_list(self):
        """Check that a list for y is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.y = [1]
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_setter_y_dict(self):
        """Check that a dictionary for y is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.y = {}
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_setter_y_tuple(self):
        """Check that a tuple for y is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.y = (1,)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_setter_y_value_minus_1(self):
        """Check that the value -1 for y is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.y = -1
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_setter_y_value_minus_10(self):
        """Check that the value -10 for y is rejected by the setter."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.y = -10
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_setter_y_boundary(self):
        """Check that y of 0 is accepted."""
        s = Square(5, 3, 4)
        s.y = 0
        self.assertEqual(s.y, 0)

    def test_setter_y_keeps_old_value(self):
        """Check that a rejected value leaves y unchanged."""
        s = Square(5, 3, 4)
        with self.assertRaises(ValueError):
            s.y = -1
        self.assertEqual(s.y, 4)

    def test_size_boundary_in_constructor(self):
        """Check that a size of 1 is accepted."""
        self.assertEqual(Square(1).size, 1)

    def test_position_boundary_in_constructor(self):
        """Check that a zero position is accepted."""
        s = Square(1, 0, 0)
        self.assertEqual((s.x, s.y), (0, 0))

    def test_validation_order_1(self):
        """Check that the arguments 'a', 'b', 'c' are validated in order."""
        with self.assertRaises(TypeError) as cm:
            Square("a", "b", "c")
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_validation_order_2(self):
        """Check that the arguments 0, 'b', 'c' are validated in order."""
        with self.assertRaises(ValueError) as cm:
            Square(0, "b", "c")
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_validation_order_3(self):
        """Check that the arguments 1, 'b', 'c' are validated in order."""
        with self.assertRaises(TypeError) as cm:
            Square(1, "b", "c")
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_validation_order_4(self):
        """Check that the arguments 1, -1, 'c' are validated in order."""
        with self.assertRaises(ValueError) as cm:
            Square(1, -1, "c")
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_validation_order_5(self):
        """Check that the arguments 1, 0, 'c' are validated in order."""
        with self.assertRaises(TypeError) as cm:
            Square(1, 0, "c")
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_validation_order_6(self):
        """Check that the arguments 1, 0, -1 are validated in order."""
        with self.assertRaises(ValueError) as cm:
            Square(1, 0, -1)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_validation_order_7(self):
        """Check that the arguments -1, -1, -1 are validated in order."""
        with self.assertRaises(ValueError) as cm:
            Square(-1, -1, -1)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_validation_order_8(self):
        """Check that the arguments 1, -1, -1 are validated in order."""
        with self.assertRaises(ValueError) as cm:
            Square(1, -1, -1)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_validation_order_9(self):
        """Check that the arguments 'a', -1 are validated in order."""
        with self.assertRaises(TypeError) as cm:
            Square("a", -1)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_validation_order_10(self):
        """Check that the arguments None, None, None are validated in
        order."""
        with self.assertRaises(TypeError) as cm:
            Square(None, None, None)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_messages_use_width_for_the_size(self):
        """Check that the size problems speak about the width."""
        with self.assertRaises(TypeError) as cm:
            Square("1")
        self.assertEqual(str(cm.exception), "width must be an integer")
        with self.assertRaises(ValueError) as cm:
            Square(0)
        self.assertEqual(str(cm.exception), "width must be > 0")


class TestSquareArea(unittest.TestCase):
    """Tests of the area of a Square."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_area_of_size_5(self):
        """Check the area of a square of size 5."""
        self.assertEqual(Square(5).area(), 25)

    def test_area_of_size_2(self):
        """Check the area of a square of size 2."""
        self.assertEqual(Square(2).area(), 4)

    def test_area_of_size_3(self):
        """Check the area of a square of size 3."""
        self.assertEqual(Square(3).area(), 9)

    def test_area_of_size_1(self):
        """Check the area of a square of size 1."""
        self.assertEqual(Square(1).area(), 1)

    def test_area_of_size_100(self):
        """Check the area of a square of size 100."""
        self.assertEqual(Square(100).area(), 10000)

    def test_area_ignores_position(self):
        """Check that the position does not change the area."""
        self.assertEqual(Square(3, 10, 20).area(), 9)

    def test_area_after_size_change(self):
        """Check that the area follows the size."""
        s = Square(3)
        s.size = 6
        self.assertEqual(s.area(), 36)

    def test_area_after_update(self):
        """Check that the area follows an update."""
        s = Square(3)
        s.update(1, 4)
        self.assertEqual(s.area(), 16)

    def test_area_is_an_integer(self):
        """Check that the area is an integer."""
        self.assertIs(type(Square(3).area()), int)


class TestSquareDisplay(unittest.TestCase):
    """Tests of the display of a Square."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_display_size_five(self):
        """Check the display of a square of size 5."""
        self.assertEqual(captured(Square(5).display), "#####\n" * 5)

    def test_display_with_x(self):
        """Check the display with an x."""
        self.assertEqual(captured(Square(2, 2).display), "  ##\n  ##\n")

    def test_display_with_x_and_y(self):
        """Check the display with x and y, as in the project example."""
        text = captured(Square(3, 1, 3).display)
        self.assertEqual(text, "\n\n\n ###\n ###\n ###\n")

    def test_display_size_one(self):
        """Check the display of the smallest square."""
        self.assertEqual(captured(Square(1).display), "#\n")

    def test_display_with_y_only(self):
        """Check the display with a y and no x."""
        self.assertEqual(captured(Square(2, 0, 2).display), "\n\n##\n##\n")

    def test_display_line_count(self):
        """Check that the number of lines is y plus the size."""
        text = captured(Square(3, 2, 4).display)
        self.assertEqual(text.count("\n"), 7)

    def test_display_after_size_change(self):
        """Check that the display follows the size."""
        s = Square(1)
        s.size = 3
        self.assertEqual(captured(s.display), "###\n###\n###\n")

    def test_display_after_update(self):
        """Check that the display follows an update."""
        s = Square(1)
        s.update(1, 2, 1, 1)
        self.assertEqual(captured(s.display), "\n ##\n ##\n")

    def test_display_is_the_rectangle_display(self):
        """Check that a square displays like the rectangle of the same
        sides."""
        s = Square(3, 2, 1)
        r = Rectangle(3, 3, 2, 1)
        self.assertEqual(captured(s.display), captured(r.display))


class TestSquareStr(unittest.TestCase):
    """Tests of the text description of a Square."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_str_default_position(self):
        """Check the text of a square with defaults."""
        self.assertEqual(str(Square(5)), "[Square] (1) 0/0 - 5")

    def test_str_with_x(self):
        """Check the text of a square with an x."""
        self.assertEqual(str(Square(2, 2)), "[Square] (1) 2/0 - 2")

    def test_str_with_x_and_y(self):
        """Check the text of a square with x and y."""
        self.assertEqual(str(Square(3, 1, 3)), "[Square] (1) 1/3 - 3")

    def test_str_with_id(self):
        """Check the text of a square with an explicit id."""
        self.assertEqual(str(Square(4, 5, 6, 7)), "[Square] (7) 5/6 - 4")

    def test_str_generated_ids(self):
        """Check the ids shown in the text."""
        s1 = Square(1)
        s2 = Square(1)
        self.assertEqual(str(s1), "[Square] (1) 0/0 - 1")
        self.assertEqual(str(s2), "[Square] (2) 0/0 - 1")

    def test_str_after_update(self):
        """Check that the text follows an update."""
        s = Square(5)
        s.update(1, 2, 3, 4)
        self.assertEqual(str(s), "[Square] (1) 3/4 - 2")

    def test_str_prefix(self):
        """Check that the text starts with the class name of the square."""
        text = str(Square(1))
        self.assertTrue(text.startswith("[Square] "))
        self.assertNotIn("Rectangle", text)

    def test_str_has_one_size(self):
        """Check that the text shows a single size."""
        text = str(Square(9, 8, 7, 6))
        self.assertEqual(text, "[Square] (6) 8/7 - 9")
        self.assertNotIn("9/9", text)

    def test_print_uses_str(self):
        """Check that print shows the text description."""
        s = Square(5)
        self.assertEqual(captured(lambda: print(s)), "[Square] (1) 0/0 - 5\n")

    def test_str_returns_a_string(self):
        """Check that the description is a string."""
        self.assertIs(type(str(Square(1))), str)


class TestSquareUpdate(unittest.TestCase):
    """Tests of the update method of a Square."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_update_with_1_arguments(self):
        """Check an update with 1 positional arguments."""
        s = Square(5)

        s.update(10)
        self.assertEqual(str(s), "[Square] (10) 0/0 - 5")

    def test_update_with_2_arguments(self):
        """Check an update with 2 positional arguments."""
        s = Square(5)

        s.update(1, 2)
        self.assertEqual(str(s), "[Square] (1) 0/0 - 2")

    def test_update_with_3_arguments(self):
        """Check an update with 3 positional arguments."""
        s = Square(5)

        s.update(1, 2, 3)
        self.assertEqual(str(s), "[Square] (1) 3/0 - 2")

    def test_update_with_4_arguments(self):
        """Check an update with 4 positional arguments."""
        s = Square(5)

        s.update(1, 2, 3, 4)
        self.assertEqual(str(s), "[Square] (1) 3/4 - 2")

    def test_update_argument_order(self):
        """Check the order of the positional arguments."""
        s = Square(1)
        s.update(11, 22, 33, 44)
        self.assertEqual(s.to_dictionary(),
                         {"id": 11, "size": 22, "x": 33, "y": 44})

    def test_update_positional_sequence(self):
        """Check the positional sequence of the project example."""
        s = Square(5)

        results = []
        for args in ((10,), (1, 2), (1, 2, 3), (1, 2, 3, 4)):
            s.update(*args)
            results.append(str(s))
        self.assertEqual(results, ["[Square] (10) 0/0 - 5",
                                   "[Square] (1) 0/0 - 2",
                                   "[Square] (1) 3/0 - 2",
                                   "[Square] (1) 3/4 - 2"])

    def test_update_keyword_sequence(self):
        """Check the keyword sequence of the project example."""
        s = Square(5)

        s.update(1, 2, 3, 4)
        s.update(x=12)
        self.assertEqual(str(s), "[Square] (1) 12/4 - 2")
        s.update(size=7, y=1)
        self.assertEqual(str(s), "[Square] (1) 12/1 - 7")
        s.update(size=7, id=89, y=1)
        self.assertEqual(str(s), "[Square] (89) 12/1 - 7")

    def test_update_size_changes_width_and_height(self):
        """Check that the size updates both sides."""
        s = Square(5)

        s.update(1, 8)
        self.assertEqual((s.width, s.height), (8, 8))

    def test_update_without_arguments(self):
        """Check that an update without arguments changes nothing."""
        s = Square(5)

        s.update()
        expected = {"id": 1, "size": 5, "x": 0, "y": 0}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_empty_kwargs(self):
        """Check that an update with no values changes nothing."""
        s = Square(5)

        s.update(**{})
        expected = {"id": 1, "size": 5, "x": 0, "y": 0}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_extra_arguments(self):
        """Check that arguments beyond the fourth are not used."""
        s = Square(5)

        s.update(1, 2, 3, 4, 5, 6)
        expected = {"id": 1, "size": 2, "x": 3, "y": 4}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_five_arguments(self):
        """Check an update with five positional arguments."""
        s = Square(5)

        s.update(9, 8, 7, 6, 5)
        self.assertEqual(str(s), "[Square] (9) 7/6 - 8")

    def test_update_only_id(self):
        """Check that one argument changes only the id."""
        s = Square(5)

        s.update(77)
        expected = {"id": 77, "size": 5, "x": 0, "y": 0}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_kwarg_id(self):
        """Check an update with only the keyword id."""
        s = Square(5)

        s.update(id=89)
        expected = {'id': 89, 'size': 5, 'x': 0, 'y': 0}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_kwarg_size(self):
        """Check an update with only the keyword size."""
        s = Square(5)

        s.update(size=7)
        expected = {'id': 1, 'size': 7, 'x': 0, 'y': 0}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_kwarg_x(self):
        """Check an update with only the keyword x."""
        s = Square(5)

        s.update(x=2)
        expected = {'id': 1, 'size': 5, 'x': 2, 'y': 0}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_kwarg_y(self):
        """Check an update with only the keyword y."""
        s = Square(5)

        s.update(y=3)
        expected = {'id': 1, 'size': 5, 'x': 0, 'y': 3}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_all_kwargs(self):
        """Check an update with the four keywords."""
        s = Square(5)

        s.update(id=5, size=6, x=7, y=8)
        expected = {"id": 5, "size": 6, "x": 7, "y": 8}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_all_kwargs_reversed(self):
        """Check that the order of the keywords is not important."""
        s = Square(5)

        s.update(y=8, x=7, size=6, id=5)
        expected = {"id": 5, "size": 6, "x": 7, "y": 8}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_kwargs_shuffled(self):
        """Check a shuffled order of the keywords."""
        s = Square(5)

        s.update(x=7, id=5, y=8, size=6)
        expected = {"id": 5, "size": 6, "x": 7, "y": 8}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_size_and_y_keywords(self):
        """Check an update with the keywords size and y."""
        s = Square(5)

        s.update(size=7, y=1)
        expected = {"id": 1, "size": 7, "x": 0, "y": 1}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_kwargs_skipped_with_one_argument(self):
        """Check that keywords are skipped when an argument exists."""
        s = Square(5)

        s.update(10, size=1, x=2, y=3)
        expected = {"id": 10, "size": 5, "x": 0, "y": 0}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_kwargs_skipped_with_two_arguments(self):
        """Check that keywords are skipped with two arguments."""
        s = Square(5)

        s.update(10, 6, id=50, x=2)
        expected = {"id": 10, "size": 6, "x": 0, "y": 0}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_kwargs_skipped_with_four_arguments(self):
        """Check that keywords are skipped with four arguments."""
        s = Square(5)

        s.update(1, 2, 3, 4, id=50, size=60, x=70, y=80)
        expected = {"id": 1, "size": 2, "x": 3, "y": 4}
        self.assertEqual(s.to_dictionary(), expected)

    def test_update_invalid_kwargs_skipped_with_arguments(self):
        """Check that invalid keywords are not validated when skipped."""
        s = Square(5)

        s.update(10, size="bad", x=-1)
        self.assertEqual((s.id, s.size), (10, 5))

    def test_update_does_not_use_counter(self):
        """Check that an update never generates an id."""
        s = Square(5)

        s.update(5, 2, 2)
        self.assertEqual(Square(1).id, 2)

    def test_update_argument_size_str(self):
        """Check that a string for size is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, "1")
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_argument_size_float(self):
        """Check that a float for size is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, 1.5)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_argument_size_none(self):
        """Check that None for size is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, None)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_argument_size_list(self):
        """Check that a list for size is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, [1])
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_argument_size_dict(self):
        """Check that a dictionary for size is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, {})
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_argument_size_tuple(self):
        """Check that a tuple for size is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, (1,))
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_argument_x_str(self):
        """Check that a string for x is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, 2, "1")
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_argument_x_float(self):
        """Check that a float for x is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, 2, 1.5)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_argument_x_none(self):
        """Check that None for x is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, 2, None)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_argument_x_list(self):
        """Check that a list for x is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, 2, [1])
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_argument_x_dict(self):
        """Check that a dictionary for x is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, 2, {})
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_argument_x_tuple(self):
        """Check that a tuple for x is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, 2, (1,))
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_argument_y_str(self):
        """Check that a string for y is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, 2, 3, "1")
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_argument_y_float(self):
        """Check that a float for y is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, 2, 3, 1.5)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_argument_y_none(self):
        """Check that None for y is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, 2, 3, None)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_argument_y_list(self):
        """Check that a list for y is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, 2, 3, [1])
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_argument_y_dict(self):
        """Check that a dictionary for y is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, 2, 3, {})
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_argument_y_tuple(self):
        """Check that a tuple for y is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(1, 2, 3, (1,))
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_keyword_size_str(self):
        """Check that a string for size is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(size="1")
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_keyword_size_float(self):
        """Check that a float for size is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(size=1.5)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_keyword_size_none(self):
        """Check that None for size is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(size=None)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_keyword_size_list(self):
        """Check that a list for size is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(size=[1])
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_keyword_size_dict(self):
        """Check that a dictionary for size is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(size={})
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_keyword_size_tuple(self):
        """Check that a tuple for size is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(size=(1,))
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_keyword_x_str(self):
        """Check that a string for x is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(x="1")
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_keyword_x_float(self):
        """Check that a float for x is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(x=1.5)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_keyword_x_none(self):
        """Check that None for x is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(x=None)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_keyword_x_list(self):
        """Check that a list for x is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(x=[1])
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_keyword_x_dict(self):
        """Check that a dictionary for x is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(x={})
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_keyword_x_tuple(self):
        """Check that a tuple for x is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(x=(1,))
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_keyword_y_str(self):
        """Check that a string for y is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(y="1")
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_keyword_y_float(self):
        """Check that a float for y is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(y=1.5)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_keyword_y_none(self):
        """Check that None for y is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(y=None)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_keyword_y_list(self):
        """Check that a list for y is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(y=[1])
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_keyword_y_dict(self):
        """Check that a dictionary for y is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(y={})
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_keyword_y_tuple(self):
        """Check that a tuple for y is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(TypeError) as cm:
            s.update(y=(1,))
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_argument_size_value_0(self):
        """Check that the value 0 for size is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.update(1, 0)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_update_keyword_size_value_0(self):
        """Check that the value 0 for size is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.update(size=0)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_update_argument_size_value_minus_4(self):
        """Check that the value -4 for size is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.update(1, -4)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_update_keyword_size_value_minus_4(self):
        """Check that the value -4 for size is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.update(size=-4)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_update_argument_x_value_minus_1(self):
        """Check that the value -1 for x is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.update(1, 2, -1)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_update_keyword_x_value_minus_1(self):
        """Check that the value -1 for x is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.update(x=-1)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_update_argument_x_value_minus_4(self):
        """Check that the value -4 for x is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.update(1, 2, -4)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_update_keyword_x_value_minus_4(self):
        """Check that the value -4 for x is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.update(x=-4)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_update_argument_y_value_minus_1(self):
        """Check that the value -1 for y is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.update(1, 2, 3, -1)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_update_keyword_y_value_minus_1(self):
        """Check that the value -1 for y is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.update(y=-1)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_update_argument_y_value_minus_4(self):
        """Check that the value -4 for y is rejected by an argument."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.update(1, 2, 3, -4)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_update_keyword_y_value_minus_4(self):
        """Check that the value -4 for y is rejected by a keyword."""
        s = Square(5, 3, 4)

        with self.assertRaises(ValueError) as cm:
            s.update(y=-4)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_update_keyword_size_boundary(self):
        """Check that size of 1 is accepted by a keyword."""
        s = Square(5, 3, 4)
        s.update(size=1)
        self.assertEqual(s.size, 1)

    def test_update_keyword_x_boundary(self):
        """Check that x of 0 is accepted by a keyword."""
        s = Square(5, 3, 4)
        s.update(x=0)
        self.assertEqual(s.x, 0)

    def test_update_keyword_y_boundary(self):
        """Check that y of 0 is accepted by a keyword."""
        s = Square(5, 3, 4)
        s.update(y=0)
        self.assertEqual(s.y, 0)


class TestSquareToDictionary(unittest.TestCase):
    """Tests of the to_dictionary method."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_keys(self):
        """Check the keys of the dictionary."""
        keys = set(Square(1).to_dictionary())
        self.assertEqual(keys, {"id", "size", "x", "y"})

    def test_no_width_or_height_keys(self):
        """Check that the dictionary has no width and no height."""
        d = Square(1).to_dictionary()
        self.assertNotIn("width", d)
        self.assertNotIn("height", d)

    def test_values(self):
        """Check the values of the dictionary."""
        s = Square(10, 2, 1)
        expected = {"id": 1, "x": 2, "size": 10, "y": 1}
        self.assertEqual(s.to_dictionary(), expected)

    def test_returns_a_dict(self):
        """Check that the result is a dictionary."""
        self.assertIs(type(Square(1).to_dictionary()), dict)

    def test_distinct_values(self):
        """Check that each value is under its own key."""
        d = Square(11, 22, 33, 44).to_dictionary()
        values = (d["size"], d["x"], d["y"], d["id"])
        self.assertEqual(values, (11, 22, 33, 44))

    def test_default_position_values(self):
        """Check the default position in the dictionary."""
        d = Square(4).to_dictionary()
        self.assertEqual((d["x"], d["y"]), (0, 0))

    def test_after_update(self):
        """Check that the dictionary follows an update."""
        s = Square(1)
        s.update(7, 6, 5, 4)
        expected = {"id": 7, "size": 6, "x": 5, "y": 4}
        self.assertEqual(s.to_dictionary(), expected)

    def test_after_size_change(self):
        """Check that the dictionary follows the size."""
        s = Square(1, 0, 0, 1)
        s.size = 9
        expected = {"id": 1, "size": 9, "x": 0, "y": 0}
        self.assertEqual(s.to_dictionary(), expected)

    def test_new_dictionary_each_time(self):
        """Check that each call builds a new dictionary."""
        s = Square(1)
        self.assertIsNot(s.to_dictionary(), s.to_dictionary())

    def test_changing_the_dictionary_keeps_the_object(self):
        """Check that changing the dictionary does not change the square."""
        s = Square(1)
        d = s.to_dictionary()
        d["size"] = 50
        self.assertEqual(s.size, 1)

    def test_update_with_own_dictionary(self):
        """Check that a dictionary can feed the update method."""
        s1 = Square(10, 2, 1)
        s2 = Square(1, 1)
        s2.update(**s1.to_dictionary())
        self.assertEqual(str(s2), "[Square] (1) 2/1 - 10")
        self.assertFalse(s1 == s2)

    def test_values_are_integers(self):
        """Check that all the values are integers."""
        d = Square(1, 2, 3, 4).to_dictionary()
        self.assertTrue(all(type(value) is int for value in d.values()))

    def test_differs_from_the_rectangle_dictionary(self):
        """Check that the square dictionary is not the rectangle one."""
        s = Square(2, 1, 1, 5)
        r = Rectangle(2, 2, 1, 1, 5)
        self.assertNotEqual(s.to_dictionary(), r.to_dictionary())


class TestSquareJson(unittest.TestCase):
    """Tests of the JSON helpers used by Square."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_to_json_string(self):
        """Check the JSON text of a square dictionary."""
        d = Square(10, 2, 1).to_dictionary()
        text = Base.to_json_string([d])
        self.assertIs(type(text), str)
        self.assertEqual(json.loads(text), [d])

    def test_save_to_file_content(self):
        """Check the content of the saved file."""
        s1 = Square(5)
        s2 = Square(7, 9, 1)
        Square.save_to_file([s1, s2])
        expected = [{"id": 1, "size": 5, "x": 0, "y": 0},
                    {"id": 2, "size": 7, "x": 9, "y": 1}]
        self.assertEqual(json.loads(read_file("Square.json")), expected)

    def test_save_to_file_does_not_create_rectangle_file(self):
        """Check that only Square.json is created."""
        Square.save_to_file([Square(1)])
        self.assertTrue(os.path.exists("Square.json"))
        self.assertFalse(os.path.exists("Rectangle.json"))

    def test_save_to_file_none(self):
        """Check that None saves an empty list."""
        Square.save_to_file(None)
        self.assertEqual(read_file("Square.json"), "[]")

    def test_save_to_file_empty(self):
        """Check that an empty list saves an empty list."""
        Square.save_to_file([])
        self.assertEqual(read_file("Square.json"), "[]")

    def test_save_to_file_overwrites(self):
        """Check that a second save replaces the first one."""
        Square.save_to_file([Square(1), Square(2)])
        Square.save_to_file([Square(3)])
        data = json.loads(read_file("Square.json"))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["size"], 3)

    def test_from_json_string(self):
        """Check the list read for a square dictionary."""
        d = Square(10, 2, 1).to_dictionary()
        self.assertEqual(Base.from_json_string(Base.to_json_string([d])), [d])

    def test_create_full(self):
        """Check that create applies every attribute."""
        s = Square.create(id=5, size=6, x=7, y=8)
        self.assertEqual(str(s), "[Square] (5) 7/8 - 6")

    def test_create_type(self):
        """Check that create returns a Square."""
        s = Square.create(size=3)
        self.assertIs(type(s), Square)
        self.assertEqual((s.width, s.height), (3, 3))

    def test_create_from_dictionary(self):
        """Check the creation with the dictionary of a square."""
        s1 = Square(5, 2, 3, 9)
        s2 = Square.create(**s1.to_dictionary())
        self.assertEqual(str(s2), "[Square] (9) 2/3 - 5")
        self.assertIsNot(s1, s2)
        self.assertFalse(s1 == s2)

    def test_load_from_file_missing(self):
        """Check that a missing file gives an empty list."""
        self.assertEqual(Square.load_from_file(), [])

    def test_load_from_file_example(self):
        """Check the objects loaded by the project example."""
        s1 = Square(5)
        s2 = Square(7, 9, 1)
        Square.save_to_file([s1, s2])
        loaded = Square.load_from_file()
        self.assertEqual([str(s) for s in loaded],
                         ["[Square] (1) 0/0 - 5", "[Square] (2) 9/1 - 7"])
        self.assertTrue(all(o is not s for o, s in zip(loaded, [s1, s2])))

    def test_load_from_file_types(self):
        """Check the types of the loaded objects."""
        Square.save_to_file([Square(1)])
        loaded = Square.load_from_file()
        self.assertIs(type(loaded), list)
        self.assertIs(type(loaded[0]), Square)

    def test_rectangle_file_is_not_loaded(self):
        """Check that the Rectangle file is not read by Square."""
        Rectangle.save_to_file([Rectangle(1, 1)])
        self.assertEqual(Square.load_from_file(), [])
