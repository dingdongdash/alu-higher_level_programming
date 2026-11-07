#!/usr/bin/python3
"""Unit tests for the Rectangle class of the models package.

The tests cover the constructor, the validation rules and their messages,
the area, the display, the text description, the update and the dictionary
representation, the JSON helpers and the file methods used by rectangles.
"""
import csv
import inspect
import io
import json
import os
import unittest
from unittest.mock import patch

from models.base import Base
from models.rectangle import Rectangle


def reset_counter():
    """Reset the private counter of the Base class to zero."""
    Base._Base__nb_objects = 0


def remove_json_files():
    """Delete the JSON files that the save methods may have created."""
    for name in ("Base.json", "Rectangle.json", "Square.json"):
        if os.path.exists(name):
            os.remove(name)


def remove_csv_files():
    """Delete the CSV files that the CSV save methods may have created."""
    for name in ("Base.csv", "Rectangle.csv", "Square.csv"):
        if os.path.exists(name):
            os.remove(name)


def csv_lines(name):
    """Return the list of the lines stored in a CSV file."""
    with open(name, "r", newline="") as file:
        return file.read().splitlines()


def write_raw(name, text):
    """Replace the content of a file with a text, keeping every newline."""
    with open(name, "w", newline="") as file:
        file.write(text)


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


class TestRectangleInit(unittest.TestCase):
    """Tests of the constructor of Rectangle."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_main_example_ids(self):
        """Check the ids of the project example."""
        r1 = Rectangle(10, 2)
        r2 = Rectangle(2, 10)
        r3 = Rectangle(10, 2, 0, 0, 12)
        self.assertEqual((r1.id, r2.id, r3.id), (1, 2, 12))

    def test_attribute_order(self):
        """Check that the arguments go to the right attributes."""
        r1 = Rectangle(1, 2, 3, 4, 5)
        values = (r1.width, r1.height, r1.x, r1.y, r1.id)
        self.assertEqual(values, (1, 2, 3, 4, 5))

    def test_default_position(self):
        """Check that x and y default to zero."""
        r1 = Rectangle(5, 6)
        self.assertEqual((r1.x, r1.y), (0, 0))

    def test_default_y(self):
        """Check that y defaults to zero when x is given."""
        r1 = Rectangle(5, 6, 7)
        self.assertEqual((r1.x, r1.y), (7, 0))

    def test_keyword_arguments(self):
        """Check that the constructor accepts keyword arguments."""
        r1 = Rectangle(height=2, width=1, y=4, x=3, id=5)
        values = (r1.width, r1.height, r1.x, r1.y, r1.id)
        self.assertEqual(values, (1, 2, 3, 4, 5))

    def test_generated_ids(self):
        """Check that generated ids increase by one."""
        ids = [Rectangle(1, 1).id for _ in range(4)]
        self.assertEqual(ids, [1, 2, 3, 4])

    def test_explicit_id_keeps_counter(self):
        """Check that an explicit id does not use the counter."""
        Rectangle(1, 1, 0, 0, 12)
        self.assertEqual(Rectangle(1, 1).id, 1)

    def test_mixed_ids_with_base(self):
        """Check that Rectangle and Base share the id counter."""
        b1 = Base()
        r1 = Rectangle(1, 1)
        b2 = Base()
        self.assertEqual((b1.id, r1.id, b2.id), (1, 2, 3))

    def test_is_a_base(self):
        """Check that a rectangle is a Base instance."""
        r1 = Rectangle(1, 1)
        self.assertIsInstance(r1, Base)
        self.assertIsInstance(r1, Rectangle)

    def test_subclass_of_base(self):
        """Check that Rectangle is a subclass of Base."""
        self.assertTrue(issubclass(Rectangle, Base))
        self.assertIs(Rectangle.__bases__[0], Base)

    def test_constructor_signature(self):
        """Check the parameters of the constructor."""
        params = inspect.signature(Rectangle.__init__).parameters
        self.assertEqual(list(params),
                         ["self", "width", "height", "x", "y", "id"])
        self.assertEqual(params["x"].default, 0)
        self.assertEqual(params["y"].default, 0)
        self.assertIsNone(params["id"].default)

    def test_private_attribute_names(self):
        """Check that the attributes are private."""
        r1 = Rectangle(1, 2, 3, 4, 5)
        keys = set(r1.__dict__)
        expected = {"id", "_Rectangle__width", "_Rectangle__height",
                    "_Rectangle__x", "_Rectangle__y"}
        self.assertEqual(keys, expected)

    def test_private_attribute_values(self):
        """Check the values stored in the private attributes."""
        r1 = Rectangle(1, 2, 3, 4, 5)
        self.assertEqual(r1._Rectangle__width, 1)
        self.assertEqual(r1._Rectangle__height, 2)
        self.assertEqual(r1._Rectangle__x, 3)
        self.assertEqual(r1._Rectangle__y, 4)

    def test_width_is_a_property(self):
        """Check that width is a property."""
        self.assertIsInstance(Rectangle.width, property)
        self.assertIsNotNone(Rectangle.width.fset)

    def test_height_is_a_property(self):
        """Check that height is a property."""
        self.assertIsInstance(Rectangle.height, property)
        self.assertIsNotNone(Rectangle.height.fset)

    def test_x_is_a_property(self):
        """Check that x is a property."""
        self.assertIsInstance(Rectangle.x, property)
        self.assertIsNotNone(Rectangle.x.fset)

    def test_y_is_a_property(self):
        """Check that y is a property."""
        self.assertIsInstance(Rectangle.y, property)
        self.assertIsNotNone(Rectangle.y.fset)

    def test_getters(self):
        """Check that the getters return the given values."""
        r1 = Rectangle(8, 9, 10, 11)
        self.assertEqual([r1.width, r1.height, r1.x, r1.y], [8, 9, 10, 11])

    def test_setters(self):
        """Check that the setters change the values."""
        r1 = Rectangle(1, 1)
        r1.width = 2
        r1.height = 3
        r1.x = 4
        r1.y = 5
        self.assertEqual([r1.width, r1.height, r1.x, r1.y], [2, 3, 4, 5])

    def test_id_is_public(self):
        """Check that the id can be read and changed."""
        r1 = Rectangle(1, 1)
        r1.id = 90
        self.assertEqual(r1.id, 90)

    def test_missing_arguments(self):
        """Check that width and height are required."""
        with self.assertRaises(TypeError):
            Rectangle()
        with self.assertRaises(TypeError):
            Rectangle(1)

    def test_instances_are_not_equal(self):
        """Check that two rectangles are not equal."""
        r1 = Rectangle(1, 1, 0, 0, 1)
        r2 = Rectangle(1, 1, 0, 0, 1)
        self.assertFalse(r1 == r2)
        self.assertTrue(r1 == r1)

    def test_large_values(self):
        """Check that large integers are accepted."""
        r1 = Rectangle(10 ** 9, 10 ** 10, 10 ** 11, 10 ** 12)
        self.assertEqual([r1.width, r1.height, r1.x, r1.y],
                         [10 ** 9, 10 ** 10, 10 ** 11, 10 ** 12])

    def test_minimal_values(self):
        """Check the smallest valid dimensions and position."""
        r1 = Rectangle(1, 1, 0, 0)
        self.assertEqual([r1.width, r1.height, r1.x, r1.y], [1, 1, 0, 0])


class TestRectangleValidationConstructor(unittest.TestCase):
    """Tests of the validation done by the constructor."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_width_str(self):
        """Check that a string for width is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle("1", 2)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_float(self):
        """Check that a float for width is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1.5, 2)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_none(self):
        """Check that None for width is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(None, 2)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_list(self):
        """Check that a list for width is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle([1], 2)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_dict(self):
        """Check that a dictionary for width is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle({}, 2)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_tuple(self):
        """Check that a tuple for width is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle((1,), 2)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_set(self):
        """Check that a set for width is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle({1}, 2)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_inf(self):
        """Check that an infinite float for width is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(float("inf"), 2)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_nan(self):
        """Check that a NaN float for width is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(float("nan"), 2)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_height_str(self):
        """Check that a string for height is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, "1")
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_float(self):
        """Check that a float for height is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 1.5)
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_none(self):
        """Check that None for height is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, None)
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_list(self):
        """Check that a list for height is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, [1])
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_dict(self):
        """Check that a dictionary for height is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, {})
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_tuple(self):
        """Check that a tuple for height is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, (1,))
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_set(self):
        """Check that a set for height is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, {1})
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_inf(self):
        """Check that an infinite float for height is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, float("inf"))
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_nan(self):
        """Check that a NaN float for height is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, float("nan"))
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_x_str(self):
        """Check that a string for x is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, "1")
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_float(self):
        """Check that a float for x is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, 1.5)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_none(self):
        """Check that None for x is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, None)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_list(self):
        """Check that a list for x is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, [1])
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_dict(self):
        """Check that a dictionary for x is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, {})
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_tuple(self):
        """Check that a tuple for x is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, (1,))
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_set(self):
        """Check that a set for x is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, {1})
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_inf(self):
        """Check that an infinite float for x is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, float("inf"))
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_nan(self):
        """Check that a NaN float for x is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, float("nan"))
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_y_str(self):
        """Check that a string for y is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, 3, "1")
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_float(self):
        """Check that a float for y is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, 3, 1.5)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_none(self):
        """Check that None for y is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, 3, None)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_list(self):
        """Check that a list for y is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, 3, [1])
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_dict(self):
        """Check that a dictionary for y is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, 3, {})
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_tuple(self):
        """Check that a tuple for y is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, 3, (1,))
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_set(self):
        """Check that a set for y is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, 3, {1})
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_inf(self):
        """Check that an infinite float for y is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, 3, float("inf"))
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_nan(self):
        """Check that a NaN float for y is rejected."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, 3, float("nan"))
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_width_value_0(self):
        """Check that the value 0 for width is rejected."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(0, 2)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_width_value_minus_1(self):
        """Check that the value -1 for width is rejected."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(-1, 2)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_width_value_minus_10(self):
        """Check that the value -10 for width is rejected."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(-10, 2)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_height_value_0(self):
        """Check that the value 0 for height is rejected."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(1, 0)
        self.assertEqual(str(cm.exception), "height must be > 0")

    def test_height_value_minus_1(self):
        """Check that the value -1 for height is rejected."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(1, -1)
        self.assertEqual(str(cm.exception), "height must be > 0")

    def test_height_value_minus_10(self):
        """Check that the value -10 for height is rejected."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(1, -10)
        self.assertEqual(str(cm.exception), "height must be > 0")

    def test_x_value_minus_1(self):
        """Check that the value -1 for x is rejected."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(1, 2, -1)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_x_value_minus_10(self):
        """Check that the value -10 for x is rejected."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(1, 2, -10)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_y_value_minus_1(self):
        """Check that the value -1 for y is rejected."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(1, 2, 3, -1)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_y_value_minus_10(self):
        """Check that the value -10 for y is rejected."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(1, 2, 3, -10)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_width_negative_float_is_a_type_error(self):
        """Check that a negative float for width fails the type check
        first."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(-1.5, 2)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_numeric_string_is_a_type_error(self):
        """Check that a numeric string for width fails the type check."""
        with self.assertRaises(TypeError) as cm:
            Rectangle("-1", 2)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_height_negative_float_is_a_type_error(self):
        """Check that a negative float for height fails the type check
        first."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, -1.5)
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_numeric_string_is_a_type_error(self):
        """Check that a numeric string for height fails the type check."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, "-1")
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_x_negative_float_is_a_type_error(self):
        """Check that a negative float for x fails the type check first."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, -1.5)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_numeric_string_is_a_type_error(self):
        """Check that a numeric string for x fails the type check."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, "-1")
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_y_negative_float_is_a_type_error(self):
        """Check that a negative float for y fails the type check first."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, 3, -1.5)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_numeric_string_is_a_type_error(self):
        """Check that a numeric string for y fails the type check."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 2, 3, "-1")
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_width_one_is_valid(self):
        """Check that a width of 1 is accepted."""
        self.assertEqual(Rectangle(1, 5).width, 1)

    def test_height_one_is_valid(self):
        """Check that a height of 1 is accepted."""
        self.assertEqual(Rectangle(5, 1).height, 1)

    def test_x_zero_is_valid(self):
        """Check that an x of 0 is accepted."""
        self.assertEqual(Rectangle(5, 5, 0).x, 0)

    def test_y_zero_is_valid(self):
        """Check that a y of 0 is accepted."""
        self.assertEqual(Rectangle(5, 5, 0, 0).y, 0)

    def test_validation_order_1(self):
        """Check that the arguments 'a', 'b', 'c', 'd' are validated in
        order."""
        with self.assertRaises(TypeError) as cm:
            Rectangle("a", "b", "c", "d")
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_validation_order_2(self):
        """Check that the arguments 0, 'b', 'c', 'd' are validated in
        order."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(0, "b", "c", "d")
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_validation_order_3(self):
        """Check that the arguments 1, 'b', 'c', 'd' are validated in
        order."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, "b", "c", "d")
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_validation_order_4(self):
        """Check that the arguments 1, 0, 'c', 'd' are validated in
        order."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(1, 0, "c", "d")
        self.assertEqual(str(cm.exception), "height must be > 0")

    def test_validation_order_5(self):
        """Check that the arguments 1, 1, 'c', 'd' are validated in
        order."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 1, "c", "d")
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_validation_order_6(self):
        """Check that the arguments 1, 1, -1, 'd' are validated in order."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(1, 1, -1, "d")
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_validation_order_7(self):
        """Check that the arguments 1, 1, 0, 'd' are validated in order."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(1, 1, 0, "d")
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_validation_order_8(self):
        """Check that the arguments 1, 1, 0, -1 are validated in order."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(1, 1, 0, -1)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_validation_order_9(self):
        """Check that the arguments -1, -1, -1, -1 are validated in
        order."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(-1, -1, -1, -1)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_validation_order_10(self):
        """Check that the arguments 1, -1, -1, -1 are validated in order."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(1, -1, -1, -1)
        self.assertEqual(str(cm.exception), "height must be > 0")

    def test_validation_order_11(self):
        """Check that the arguments 1, 1, -1, -1 are validated in order."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(1, 1, -1, -1)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_validation_order_12(self):
        """Check that the arguments 'a', 0 are validated in order."""
        with self.assertRaises(TypeError) as cm:
            Rectangle("a", 0)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_validation_order_13(self):
        """Check that the arguments 0, 'b' are validated in order."""
        with self.assertRaises(ValueError) as cm:
            Rectangle(0, "b")
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_validation_order_14(self):
        """Check that the arguments None, None are validated in order."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(None, None)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_exception_is_not_a_value_error(self):
        """Check that a type problem is not a value error."""
        with self.assertRaises(TypeError):
            Rectangle("1", -1)

    def test_invalid_construction_message_main_example(self):
        """Check the messages of the project example."""
        with self.assertRaises(TypeError) as cm:
            Rectangle(10, "2")
        self.assertEqual(str(cm.exception), "height must be an integer")
        with self.assertRaises(ValueError) as cm:
            Rectangle(10, 2, 3, -1)
        self.assertEqual(str(cm.exception), "y must be >= 0")


class TestRectangleValidationSetters(unittest.TestCase):
    """Tests of the validation done by the setters."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_width_str(self):
        """Check that a string for width is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.width = "1"
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_float(self):
        """Check that a float for width is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.width = 1.5
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_none(self):
        """Check that None for width is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.width = None
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_list(self):
        """Check that a list for width is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.width = [1]
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_dict(self):
        """Check that a dictionary for width is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.width = {}
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_tuple(self):
        """Check that a tuple for width is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.width = (1,)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_set(self):
        """Check that a set for width is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.width = {1}
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_inf(self):
        """Check that an infinite float for width is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.width = float("inf")
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_nan(self):
        """Check that a NaN float for width is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.width = float("nan")
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_height_str(self):
        """Check that a string for height is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.height = "1"
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_float(self):
        """Check that a float for height is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.height = 1.5
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_none(self):
        """Check that None for height is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.height = None
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_list(self):
        """Check that a list for height is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.height = [1]
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_dict(self):
        """Check that a dictionary for height is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.height = {}
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_tuple(self):
        """Check that a tuple for height is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.height = (1,)
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_set(self):
        """Check that a set for height is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.height = {1}
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_inf(self):
        """Check that an infinite float for height is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.height = float("inf")
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_nan(self):
        """Check that a NaN float for height is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.height = float("nan")
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_x_str(self):
        """Check that a string for x is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.x = "1"
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_float(self):
        """Check that a float for x is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.x = 1.5
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_none(self):
        """Check that None for x is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.x = None
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_list(self):
        """Check that a list for x is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.x = [1]
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_dict(self):
        """Check that a dictionary for x is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.x = {}
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_tuple(self):
        """Check that a tuple for x is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.x = (1,)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_set(self):
        """Check that a set for x is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.x = {1}
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_inf(self):
        """Check that an infinite float for x is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.x = float("inf")
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_nan(self):
        """Check that a NaN float for x is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.x = float("nan")
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_y_str(self):
        """Check that a string for y is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.y = "1"
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_float(self):
        """Check that a float for y is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.y = 1.5
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_none(self):
        """Check that None for y is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.y = None
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_list(self):
        """Check that a list for y is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.y = [1]
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_dict(self):
        """Check that a dictionary for y is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.y = {}
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_tuple(self):
        """Check that a tuple for y is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.y = (1,)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_set(self):
        """Check that a set for y is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.y = {1}
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_inf(self):
        """Check that an infinite float for y is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.y = float("inf")
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_nan(self):
        """Check that a NaN float for y is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.y = float("nan")
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_width_value_0(self):
        """Check that the value 0 for width is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.width = 0
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_width_value_minus_1(self):
        """Check that the value -1 for width is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.width = -1
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_width_value_minus_10(self):
        """Check that the value -10 for width is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.width = -10
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_height_value_0(self):
        """Check that the value 0 for height is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.height = 0
        self.assertEqual(str(cm.exception), "height must be > 0")

    def test_height_value_minus_1(self):
        """Check that the value -1 for height is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.height = -1
        self.assertEqual(str(cm.exception), "height must be > 0")

    def test_height_value_minus_10(self):
        """Check that the value -10 for height is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.height = -10
        self.assertEqual(str(cm.exception), "height must be > 0")

    def test_x_value_minus_1(self):
        """Check that the value -1 for x is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.x = -1
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_x_value_minus_10(self):
        """Check that the value -10 for x is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.x = -10
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_y_value_minus_1(self):
        """Check that the value -1 for y is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.y = -1
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_y_value_minus_10(self):
        """Check that the value -10 for y is rejected."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.y = -10
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_width_negative_float_is_a_type_error(self):
        """Check that a negative float for width fails the type check
        first."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.width = -1.5
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_width_keeps_old_value_after_type_error(self):
        """Check that a rejected type leaves width unchanged."""
        r = Rectangle(10, 2, 3, 4)
        with self.assertRaises(TypeError):
            r.width = "bad"
        self.assertEqual(r.width, 10)

    def test_width_keeps_old_value_after_value_error(self):
        """Check that a rejected value leaves width unchanged."""
        r = Rectangle(10, 2, 3, 4)
        with self.assertRaises(ValueError):
            r.width = -5
        self.assertEqual(r.width, 10)

    def test_height_negative_float_is_a_type_error(self):
        """Check that a negative float for height fails the type check
        first."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.height = -1.5
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_height_keeps_old_value_after_type_error(self):
        """Check that a rejected type leaves height unchanged."""
        r = Rectangle(10, 2, 3, 4)
        with self.assertRaises(TypeError):
            r.height = "bad"
        self.assertEqual(r.height, 2)

    def test_height_keeps_old_value_after_value_error(self):
        """Check that a rejected value leaves height unchanged."""
        r = Rectangle(10, 2, 3, 4)
        with self.assertRaises(ValueError):
            r.height = -5
        self.assertEqual(r.height, 2)

    def test_x_negative_float_is_a_type_error(self):
        """Check that a negative float for x fails the type check first."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.x = -1.5
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_x_keeps_old_value_after_type_error(self):
        """Check that a rejected type leaves x unchanged."""
        r = Rectangle(10, 2, 3, 4)
        with self.assertRaises(TypeError):
            r.x = "bad"
        self.assertEqual(r.x, 3)

    def test_x_keeps_old_value_after_value_error(self):
        """Check that a rejected value leaves x unchanged."""
        r = Rectangle(10, 2, 3, 4)
        with self.assertRaises(ValueError):
            r.x = -5
        self.assertEqual(r.x, 3)

    def test_y_negative_float_is_a_type_error(self):
        """Check that a negative float for y fails the type check first."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.y = -1.5
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_y_keeps_old_value_after_type_error(self):
        """Check that a rejected type leaves y unchanged."""
        r = Rectangle(10, 2, 3, 4)
        with self.assertRaises(TypeError):
            r.y = "bad"
        self.assertEqual(r.y, 4)

    def test_y_keeps_old_value_after_value_error(self):
        """Check that a rejected value leaves y unchanged."""
        r = Rectangle(10, 2, 3, 4)
        with self.assertRaises(ValueError):
            r.y = -5
        self.assertEqual(r.y, 4)

    def test_width_boundary_is_valid(self):
        """Check that width of 1 is accepted."""
        r = Rectangle(10, 2, 3, 4)
        r.width = 1
        self.assertEqual(r.width, 1)

    def test_height_boundary_is_valid(self):
        """Check that height of 1 is accepted."""
        r = Rectangle(10, 2, 3, 4)
        r.height = 1
        self.assertEqual(r.height, 1)

    def test_x_boundary_is_valid(self):
        """Check that x of 0 is accepted."""
        r = Rectangle(10, 2, 3, 4)
        r.x = 0
        self.assertEqual(r.x, 0)

    def test_y_boundary_is_valid(self):
        """Check that y of 0 is accepted."""
        r = Rectangle(10, 2, 3, 4)
        r.y = 0
        self.assertEqual(r.y, 0)

    def test_setter_main_example(self):
        """Check the messages of the project example."""
        r = Rectangle(10, 2)
        with self.assertRaises(ValueError) as cm:
            r.width = -10
        self.assertEqual(str(cm.exception), "width must be > 0")
        with self.assertRaises(TypeError) as cm:
            r.x = {}
        self.assertEqual(str(cm.exception), "x must be an integer")


class TestRectangleArea(unittest.TestCase):
    """Tests of the area method."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_area_3_by_2(self):
        """Check the area of a 3 by 2 rectangle."""
        self.assertEqual(Rectangle(3, 2).area(), 6)

    def test_area_2_by_10(self):
        """Check the area of a 2 by 10 rectangle."""
        self.assertEqual(Rectangle(2, 10).area(), 20)

    def test_area_8_by_7(self):
        """Check the area of a 8 by 7 rectangle."""
        self.assertEqual(Rectangle(8, 7).area(), 56)

    def test_area_1_by_1(self):
        """Check the area of a 1 by 1 rectangle."""
        self.assertEqual(Rectangle(1, 1).area(), 1)

    def test_area_100_by_100(self):
        """Check the area of a 100 by 100 rectangle."""
        self.assertEqual(Rectangle(100, 100).area(), 10000)

    def test_area_ignores_position(self):
        """Check that the position does not change the area."""
        self.assertEqual(Rectangle(3, 2, 10, 20).area(), 6)

    def test_area_with_explicit_id(self):
        """Check that the id does not change the area."""
        self.assertEqual(Rectangle(8, 7, 0, 0, 12).area(), 56)

    def test_area_after_width_change(self):
        """Check that the area follows the width."""
        r = Rectangle(3, 2)
        r.width = 5
        self.assertEqual(r.area(), 10)

    def test_area_after_height_change(self):
        """Check that the area follows the height."""
        r = Rectangle(3, 2)
        r.height = 7
        self.assertEqual(r.area(), 21)

    def test_area_after_update(self):
        """Check that the area follows an update."""
        r = Rectangle(3, 2)
        r.update(1, 4, 5)
        self.assertEqual(r.area(), 20)

    def test_area_is_an_integer(self):
        """Check that the area is an integer."""
        self.assertIs(type(Rectangle(3, 2).area()), int)

    def test_area_large(self):
        """Check the area of large rectangles."""
        self.assertEqual(Rectangle(10 ** 6, 10 ** 6).area(), 10 ** 12)


class TestRectangleDisplay(unittest.TestCase):
    """Tests of the display method."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_display_four_by_six(self):
        """Check the display of a 4 by 6 rectangle."""
        self.assertEqual(captured(Rectangle(4, 6).display), "####\n" * 6)

    def test_display_two_by_two(self):
        """Check the display of a 2 by 2 rectangle."""
        self.assertEqual(captured(Rectangle(2, 2).display), "##\n##\n")

    def test_display_one_by_one(self):
        """Check the display of a 1 by 1 rectangle."""
        self.assertEqual(captured(Rectangle(1, 1).display), "#\n")

    def test_display_wide(self):
        """Check the display of a one row rectangle."""
        self.assertEqual(captured(Rectangle(10, 1).display), "##########\n")

    def test_display_tall(self):
        """Check the display of a one column rectangle."""
        self.assertEqual(captured(Rectangle(1, 4).display), "#\n" * 4)

    def test_display_with_x_and_y(self):
        """Check the display with x and y, as in the project example."""
        text = captured(Rectangle(2, 3, 2, 2).display)
        self.assertEqual(text, "\n\n  ##\n  ##\n  ##\n")

    def test_display_with_x_only(self):
        """Check the display with an x and no y."""
        text = captured(Rectangle(3, 2, 1, 0).display)
        self.assertEqual(text, " ###\n ###\n")

    def test_display_with_y_only(self):
        """Check the display with a y and no x."""
        text = captured(Rectangle(3, 2, 0, 1).display)
        self.assertEqual(text, "\n###\n###\n")

    def test_display_one_by_one_moved(self):
        """Check the display of a moved 1 by 1 rectangle."""
        self.assertEqual(captured(Rectangle(1, 1, 1, 1).display), "\n #\n")

    def test_display_big_offset(self):
        """Check the display with large offsets."""
        text = captured(Rectangle(2, 1, 5, 3).display)
        self.assertEqual(text, "\n\n\n     ##\n")

    def test_display_without_position_has_no_blank_line(self):
        """Check that no blank line is printed without y."""
        text = captured(Rectangle(2, 2).display)
        self.assertFalse(text.startswith("\n"))
        self.assertFalse(text.endswith("\n\n"))

    def test_display_line_count(self):
        """Check that the number of lines is y plus the height."""
        text = captured(Rectangle(3, 4, 1, 2).display)
        self.assertEqual(text.count("\n"), 6)

    def test_display_rows_have_no_trailing_spaces(self):
        """Check that rows end with the last hash."""
        text = captured(Rectangle(3, 3, 2, 0).display)
        self.assertTrue(all(line.endswith("#") for line in text.splitlines()))

    def test_display_after_update(self):
        """Check that the display follows an update."""
        r = Rectangle(1, 1)
        r.update(1, 2, 2, 1, 1)
        self.assertEqual(captured(r.display), "\n ##\n ##\n")

    def test_display_after_setters(self):
        """Check that the display follows the setters."""
        r = Rectangle(1, 1)
        r.width = 3
        r.height = 2
        r.x = 1
        r.y = 1
        self.assertEqual(captured(r.display), "\n ###\n ###\n")

    def test_display_prints_and_does_not_return(self):
        """Check that display prints its result and returns nothing."""
        r = Rectangle(2, 1)
        buffer = io.StringIO()
        with patch("sys.stdout", new=buffer):
            result = r.display()
        self.assertIsNone(result)
        self.assertEqual(buffer.getvalue(), "##\n")

    def test_display_does_not_change_the_object(self):
        """Check that display keeps the attributes."""
        r = Rectangle(2, 3, 4, 5, 6)
        captured(r.display)
        self.assertEqual(r.to_dictionary(),
                         {"id": 6, "width": 2, "height": 3, "x": 4, "y": 5})


class TestRectangleStr(unittest.TestCase):
    """Tests of the text description."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_str_full(self):
        """Check the text of a rectangle with every attribute."""
        r1 = Rectangle(4, 6, 2, 1, 12)
        self.assertEqual(str(r1), "[Rectangle] (12) 2/1 - 4/6")

    def test_str_default_y(self):
        """Check the text of a rectangle with a default y."""
        self.assertEqual(str(Rectangle(5, 5, 1)), "[Rectangle] (1) 1/0 - 5/5")

    def test_str_defaults(self):
        """Check the text of a rectangle with defaults."""
        self.assertEqual(str(Rectangle(2, 3)), "[Rectangle] (1) 0/0 - 2/3")

    def test_str_generated_ids(self):
        """Check the ids shown in the text."""
        r1 = Rectangle(1, 1)
        r2 = Rectangle(1, 1)
        self.assertEqual(str(r1), "[Rectangle] (1) 0/0 - 1/1")
        self.assertEqual(str(r2), "[Rectangle] (2) 0/0 - 1/1")

    def test_str_distinct_values(self):
        """Check that every value appears at its place."""
        r1 = Rectangle(11, 22, 33, 44, 55)
        self.assertEqual(str(r1), "[Rectangle] (55) 33/44 - 11/22")

    def test_str_after_update(self):
        """Check that the text follows an update."""
        r1 = Rectangle(10, 10, 10, 10)
        r1.update(89, 2, 3, 4, 5)
        self.assertEqual(str(r1), "[Rectangle] (89) 4/5 - 2/3")

    def test_str_after_setters(self):
        """Check that the text follows the setters."""
        r1 = Rectangle(1, 1)
        r1.width = 6
        r1.x = 7
        self.assertEqual(str(r1), "[Rectangle] (1) 7/0 - 6/1")

    def test_print_uses_str(self):
        """Check that print shows the text description."""
        r1 = Rectangle(4, 6, 2, 1, 12)
        self.assertEqual(captured(lambda: print(r1)),
                         "[Rectangle] (12) 2/1 - 4/6\n")

    def test_str_returns_a_string(self):
        """Check that the description is a string."""
        self.assertIs(type(str(Rectangle(1, 1))), str)

    def test_format_uses_str(self):
        """Check that formatting uses the description."""
        r1 = Rectangle(1, 2, 3, 4, 5)
        self.assertEqual("{}".format(r1), "[Rectangle] (5) 3/4 - 1/2")


class TestRectangleUpdate(unittest.TestCase):
    """Tests of the update method."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_update_with_1_arguments(self):
        """Check an update with 1 positional arguments."""
        r = Rectangle(10, 10, 10, 10)

        r.update(89)
        self.assertEqual(str(r), "[Rectangle] (89) 10/10 - 10/10")

    def test_update_with_2_arguments(self):
        """Check an update with 2 positional arguments."""
        r = Rectangle(10, 10, 10, 10)

        r.update(89, 2)
        self.assertEqual(str(r), "[Rectangle] (89) 10/10 - 2/10")

    def test_update_with_3_arguments(self):
        """Check an update with 3 positional arguments."""
        r = Rectangle(10, 10, 10, 10)

        r.update(89, 2, 3)
        self.assertEqual(str(r), "[Rectangle] (89) 10/10 - 2/3")

    def test_update_with_4_arguments(self):
        """Check an update with 4 positional arguments."""
        r = Rectangle(10, 10, 10, 10)

        r.update(89, 2, 3, 4)
        self.assertEqual(str(r), "[Rectangle] (89) 4/10 - 2/3")

    def test_update_with_5_arguments(self):
        """Check an update with 5 positional arguments."""
        r = Rectangle(10, 10, 10, 10)

        r.update(89, 2, 3, 4, 5)
        self.assertEqual(str(r), "[Rectangle] (89) 4/5 - 2/3")

    def test_update_argument_order(self):
        """Check the order of the positional arguments."""
        r = Rectangle(1, 1)
        r.update(11, 22, 33, 44, 55)
        self.assertEqual(r.to_dictionary(),
                         {"id": 11, "width": 22, "height": 33,
                          "x": 44, "y": 55})

    def test_update_main_example_sequence(self):
        """Check the whole sequence of the project example."""
        r = Rectangle(10, 10, 10, 10)

        results = []
        steps = ((89,), (89, 2), (89, 2, 3), (89, 2, 3, 4), (89, 2, 3, 4, 5))
        for args in steps:
            r.update(*args)
            results.append(str(r))
        self.assertEqual(results, ["[Rectangle] (89) 10/10 - 10/10",
                                   "[Rectangle] (89) 10/10 - 2/10",
                                   "[Rectangle] (89) 10/10 - 2/3",
                                   "[Rectangle] (89) 4/10 - 2/3",
                                   "[Rectangle] (89) 4/5 - 2/3"])

    def test_update_only_id(self):
        """Check that one argument changes only the id."""
        r = Rectangle(10, 10, 10, 10)

        r.update(5)
        self.assertEqual(r.to_dictionary(),
                         {"id": 5, "width": 10, "height": 10,
                          "x": 10, "y": 10})

    def test_update_without_arguments(self):
        """Check that an update without arguments changes nothing."""
        r = Rectangle(10, 10, 10, 10)

        r.update()
        self.assertEqual(r.to_dictionary(),
                         {"id": 1, "width": 10, "height": 10,
                          "x": 10, "y": 10})

    def test_update_empty_kwargs(self):
        """Check that an update with no values changes nothing."""
        r = Rectangle(10, 10, 10, 10)

        r.update(**{})
        self.assertEqual(r.to_dictionary(),
                         {"id": 1, "width": 10, "height": 10,
                          "x": 10, "y": 10})

    def test_update_extra_arguments(self):
        """Check that arguments beyond the fifth are not used."""
        r = Rectangle(1, 1)
        r.update(1, 2, 3, 4, 5, 6, 7)
        self.assertEqual(r.to_dictionary(),
                         {"id": 1, "width": 2, "height": 3, "x": 4, "y": 5})

    def test_update_six_arguments(self):
        """Check an update with six positional arguments."""
        r = Rectangle(1, 1)
        r.update(9, 8, 7, 6, 5, 4)
        self.assertEqual(str(r), "[Rectangle] (9) 6/5 - 8/7")

    def test_update_can_be_repeated(self):
        """Check that updates can follow each other."""
        r = Rectangle(1, 1)
        r.update(2, 3, 4)
        r.update(5)
        self.assertEqual(str(r), "[Rectangle] (5) 0/0 - 3/4")

    def test_update_kwarg_id(self):
        """Check an update with only the keyword id."""
        r = Rectangle(10, 10, 10, 10)

        r.update(id=89)
        self.assertEqual(str(r), "[Rectangle] (89) 10/10 - 10/10")

    def test_update_kwarg_width(self):
        """Check an update with only the keyword width."""
        r = Rectangle(10, 10, 10, 10)

        r.update(width=1)
        self.assertEqual(str(r), "[Rectangle] (1) 10/10 - 1/10")

    def test_update_kwarg_height(self):
        """Check an update with only the keyword height."""
        r = Rectangle(10, 10, 10, 10)

        r.update(height=1)
        self.assertEqual(str(r), "[Rectangle] (1) 10/10 - 10/1")

    def test_update_kwarg_x(self):
        """Check an update with only the keyword x."""
        r = Rectangle(10, 10, 10, 10)

        r.update(x=2)
        self.assertEqual(str(r), "[Rectangle] (1) 2/10 - 10/10")

    def test_update_kwarg_y(self):
        """Check an update with only the keyword y."""
        r = Rectangle(10, 10, 10, 10)

        r.update(y=3)
        self.assertEqual(str(r), "[Rectangle] (1) 10/3 - 10/10")

    def test_update_kwargs_width_and_x(self):
        """Check an update with the keywords width and x."""
        r = Rectangle(10, 10, 10, 10)

        r.update(width=1, x=2)
        self.assertEqual(str(r), "[Rectangle] (1) 2/10 - 1/10")

    def test_update_kwargs_main_example(self):
        """Check the keyword updates of the project example."""
        r = Rectangle(10, 10, 10, 10)

        r.update(height=1)
        self.assertEqual(str(r), "[Rectangle] (1) 10/10 - 10/1")
        r.update(width=1, x=2)
        self.assertEqual(str(r), "[Rectangle] (1) 2/10 - 1/1")
        r.update(y=1, width=2, x=3, id=89)
        self.assertEqual(str(r), "[Rectangle] (89) 3/1 - 2/1")
        r.update(x=1, height=2, y=3, width=4)
        self.assertEqual(str(r), "[Rectangle] (89) 1/3 - 4/2")

    def test_update_all_kwargs(self):
        """Check an update with the five keywords."""
        r = Rectangle(1, 1)
        r.update(id=5, width=6, height=7, x=8, y=9)
        self.assertEqual(r.to_dictionary(),
                         {"id": 5, "width": 6, "height": 7, "x": 8, "y": 9})

    def test_update_all_kwargs_reversed(self):
        """Check that the order of the keywords is not important."""
        r = Rectangle(1, 1)
        r.update(y=9, x=8, height=7, width=6, id=5)
        self.assertEqual(r.to_dictionary(),
                         {"id": 5, "width": 6, "height": 7, "x": 8, "y": 9})

    def test_update_kwargs_shuffled(self):
        """Check a shuffled order of the keywords."""
        r = Rectangle(1, 1)
        r.update(height=7, id=5, y=9, width=6, x=8)
        self.assertEqual(r.to_dictionary(),
                         {"id": 5, "width": 6, "height": 7, "x": 8, "y": 9})

    def test_update_kwargs_keep_other_attributes(self):
        """Check that keywords keep the other attributes."""
        r = Rectangle(10, 10, 10, 10)

        r.update(height=2)
        self.assertEqual(r.to_dictionary(),
                         {"id": 1, "width": 10, "height": 2, "x": 10, "y": 10})

    def test_update_kwargs_skipped_with_one_argument(self):
        """Check that keywords are skipped when an argument exists."""
        r = Rectangle(10, 10, 10, 10)

        r.update(89, height=1, width=2, x=3, y=4)
        self.assertEqual(r.to_dictionary(),
                         {"id": 89, "width": 10, "height": 10,
                          "x": 10, "y": 10})

    def test_update_kwargs_skipped_with_two_arguments(self):
        """Check that keywords are skipped with two arguments."""
        r = Rectangle(10, 10, 10, 10)

        r.update(89, 2, id=5, x=3)
        self.assertEqual(r.to_dictionary(),
                         {"id": 89, "width": 2, "height": 10,
                          "x": 10, "y": 10})

    def test_update_kwargs_skipped_with_five_arguments(self):
        """Check that keywords are skipped with five arguments."""
        r = Rectangle(10, 10, 10, 10)

        r.update(1, 2, 3, 4, 5, id=50, width=60, height=70, x=80, y=90)
        self.assertEqual(r.to_dictionary(),
                         {"id": 1, "width": 2, "height": 3, "x": 4, "y": 5})

    def test_update_invalid_kwargs_skipped_with_arguments(self):
        """Check that invalid keywords are not validated when skipped."""
        r = Rectangle(10, 10, 10, 10)

        r.update(89, width="bad", x=-1)
        self.assertEqual(r.id, 89)
        self.assertEqual(r.width, 10)

    def test_update_kwargs_id_only(self):
        """Check that the id keyword alone is applied."""
        r = Rectangle(10, 10, 10, 10)

        r.update(id=77)
        self.assertEqual(r.id, 77)

    def test_update_does_not_use_counter(self):
        """Check that an update never generates an id."""
        r = Rectangle(10, 10, 10, 10)

        r.update(5, 2, 2)
        self.assertEqual(Rectangle(1, 1).id, 2)

    def test_update_argument_width_str(self):
        """Check that a string for width is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, "1")
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_argument_width_float(self):
        """Check that a float for width is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 1.5)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_argument_width_none(self):
        """Check that None for width is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, None)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_argument_width_list(self):
        """Check that a list for width is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, [1])
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_argument_width_dict(self):
        """Check that a dictionary for width is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, {})
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_argument_width_tuple(self):
        """Check that a tuple for width is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, (1,))
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_argument_height_str(self):
        """Check that a string for height is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, "1")
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_update_argument_height_float(self):
        """Check that a float for height is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, 1.5)
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_update_argument_height_none(self):
        """Check that None for height is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, None)
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_update_argument_height_list(self):
        """Check that a list for height is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, [1])
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_update_argument_height_dict(self):
        """Check that a dictionary for height is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, {})
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_update_argument_height_tuple(self):
        """Check that a tuple for height is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, (1,))
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_update_argument_x_str(self):
        """Check that a string for x is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, 3, "1")
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_argument_x_float(self):
        """Check that a float for x is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, 3, 1.5)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_argument_x_none(self):
        """Check that None for x is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, 3, None)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_argument_x_list(self):
        """Check that a list for x is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, 3, [1])
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_argument_x_dict(self):
        """Check that a dictionary for x is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, 3, {})
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_argument_x_tuple(self):
        """Check that a tuple for x is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, 3, (1,))
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_argument_y_str(self):
        """Check that a string for y is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, 3, 4, "1")
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_argument_y_float(self):
        """Check that a float for y is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, 3, 4, 1.5)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_argument_y_none(self):
        """Check that None for y is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, 3, 4, None)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_argument_y_list(self):
        """Check that a list for y is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, 3, 4, [1])
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_argument_y_dict(self):
        """Check that a dictionary for y is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, 3, 4, {})
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_argument_y_tuple(self):
        """Check that a tuple for y is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(1, 2, 3, 4, (1,))
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_keyword_width_str(self):
        """Check that a string for width is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(width="1")
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_keyword_width_float(self):
        """Check that a float for width is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(width=1.5)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_keyword_width_none(self):
        """Check that None for width is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(width=None)
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_keyword_width_list(self):
        """Check that a list for width is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(width=[1])
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_keyword_width_dict(self):
        """Check that a dictionary for width is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(width={})
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_keyword_width_tuple(self):
        """Check that a tuple for width is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(width=(1,))
        self.assertEqual(str(cm.exception), "width must be an integer")

    def test_update_keyword_height_str(self):
        """Check that a string for height is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(height="1")
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_update_keyword_height_float(self):
        """Check that a float for height is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(height=1.5)
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_update_keyword_height_none(self):
        """Check that None for height is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(height=None)
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_update_keyword_height_list(self):
        """Check that a list for height is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(height=[1])
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_update_keyword_height_dict(self):
        """Check that a dictionary for height is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(height={})
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_update_keyword_height_tuple(self):
        """Check that a tuple for height is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(height=(1,))
        self.assertEqual(str(cm.exception), "height must be an integer")

    def test_update_keyword_x_str(self):
        """Check that a string for x is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(x="1")
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_keyword_x_float(self):
        """Check that a float for x is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(x=1.5)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_keyword_x_none(self):
        """Check that None for x is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(x=None)
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_keyword_x_list(self):
        """Check that a list for x is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(x=[1])
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_keyword_x_dict(self):
        """Check that a dictionary for x is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(x={})
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_keyword_x_tuple(self):
        """Check that a tuple for x is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(x=(1,))
        self.assertEqual(str(cm.exception), "x must be an integer")

    def test_update_keyword_y_str(self):
        """Check that a string for y is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(y="1")
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_keyword_y_float(self):
        """Check that a float for y is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(y=1.5)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_keyword_y_none(self):
        """Check that None for y is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(y=None)
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_keyword_y_list(self):
        """Check that a list for y is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(y=[1])
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_keyword_y_dict(self):
        """Check that a dictionary for y is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(y={})
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_keyword_y_tuple(self):
        """Check that a tuple for y is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(TypeError) as cm:
            r.update(y=(1,))
        self.assertEqual(str(cm.exception), "y must be an integer")

    def test_update_argument_width_value_0(self):
        """Check that the value 0 for width is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(1, 0)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_update_keyword_width_value_0(self):
        """Check that the value 0 for width is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(width=0)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_update_argument_width_value_minus_4(self):
        """Check that the value -4 for width is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(1, -4)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_update_keyword_width_value_minus_4(self):
        """Check that the value -4 for width is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(width=-4)
        self.assertEqual(str(cm.exception), "width must be > 0")

    def test_update_argument_height_value_0(self):
        """Check that the value 0 for height is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(1, 2, 0)
        self.assertEqual(str(cm.exception), "height must be > 0")

    def test_update_keyword_height_value_0(self):
        """Check that the value 0 for height is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(height=0)
        self.assertEqual(str(cm.exception), "height must be > 0")

    def test_update_argument_height_value_minus_4(self):
        """Check that the value -4 for height is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(1, 2, -4)
        self.assertEqual(str(cm.exception), "height must be > 0")

    def test_update_keyword_height_value_minus_4(self):
        """Check that the value -4 for height is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(height=-4)
        self.assertEqual(str(cm.exception), "height must be > 0")

    def test_update_argument_x_value_minus_1(self):
        """Check that the value -1 for x is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(1, 2, 3, -1)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_update_keyword_x_value_minus_1(self):
        """Check that the value -1 for x is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(x=-1)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_update_argument_x_value_minus_4(self):
        """Check that the value -4 for x is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(1, 2, 3, -4)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_update_keyword_x_value_minus_4(self):
        """Check that the value -4 for x is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(x=-4)
        self.assertEqual(str(cm.exception), "x must be >= 0")

    def test_update_argument_y_value_minus_1(self):
        """Check that the value -1 for y is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(1, 2, 3, 4, -1)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_update_keyword_y_value_minus_1(self):
        """Check that the value -1 for y is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(y=-1)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_update_argument_y_value_minus_4(self):
        """Check that the value -4 for y is rejected by an argument."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(1, 2, 3, 4, -4)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_update_keyword_y_value_minus_4(self):
        """Check that the value -4 for y is rejected by a keyword."""
        r = Rectangle(10, 2, 3, 4)

        with self.assertRaises(ValueError) as cm:
            r.update(y=-4)
        self.assertEqual(str(cm.exception), "y must be >= 0")

    def test_update_keyword_width_boundary(self):
        """Check that width of 1 is accepted by a keyword."""
        r = Rectangle(10, 2, 3, 4)
        r.update(width=1)
        self.assertEqual(r.width, 1)

    def test_update_keyword_height_boundary(self):
        """Check that height of 1 is accepted by a keyword."""
        r = Rectangle(10, 2, 3, 4)
        r.update(height=1)
        self.assertEqual(r.height, 1)

    def test_update_keyword_x_boundary(self):
        """Check that x of 0 is accepted by a keyword."""
        r = Rectangle(10, 2, 3, 4)
        r.update(x=0)
        self.assertEqual(r.x, 0)

    def test_update_keyword_y_boundary(self):
        """Check that y of 0 is accepted by a keyword."""
        r = Rectangle(10, 2, 3, 4)
        r.update(y=0)
        self.assertEqual(r.y, 0)


class TestRectangleToDictionary(unittest.TestCase):
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
        keys = set(Rectangle(1, 2).to_dictionary())
        self.assertEqual(keys, {"id", "width", "height", "x", "y"})

    def test_values(self):
        """Check the values of the dictionary."""
        r = Rectangle(10, 2, 1, 9)
        self.assertEqual(r.to_dictionary(),
                         {"x": 1, "y": 9, "id": 1, "height": 2, "width": 10})

    def test_returns_a_dict(self):
        """Check that the result is a dictionary."""
        self.assertIs(type(Rectangle(1, 1).to_dictionary()), dict)

    def test_explicit_id_value(self):
        """Check that an explicit id is in the dictionary."""
        self.assertEqual(Rectangle(1, 1, 0, 0, 99).to_dictionary()["id"], 99)

    def test_distinct_values(self):
        """Check that each value is under its own key."""
        d = Rectangle(11, 22, 33, 44, 55).to_dictionary()
        self.assertEqual(d["width"], 11)
        self.assertEqual(d["height"], 22)
        self.assertEqual(d["x"], 33)
        self.assertEqual(d["y"], 44)
        self.assertEqual(d["id"], 55)

    def test_default_position_values(self):
        """Check the default position in the dictionary."""
        d = Rectangle(1, 2).to_dictionary()
        self.assertEqual((d["x"], d["y"]), (0, 0))

    def test_after_update(self):
        """Check that the dictionary follows an update."""
        r = Rectangle(1, 1)
        r.update(7, 6, 5, 4, 3)
        self.assertEqual(r.to_dictionary(),
                         {"id": 7, "width": 6, "height": 5, "x": 4, "y": 3})

    def test_after_setters(self):
        """Check that the dictionary follows the setters."""
        r = Rectangle(1, 1, 0, 0, 1)
        r.width = 5
        r.y = 2
        self.assertEqual(r.to_dictionary(),
                         {"id": 1, "width": 5, "height": 1, "x": 0, "y": 2})

    def test_new_dictionary_each_time(self):
        """Check that each call builds a new dictionary."""
        r = Rectangle(1, 1)
        self.assertIsNot(r.to_dictionary(), r.to_dictionary())

    def test_changing_the_dictionary_keeps_the_object(self):
        """Check that changing the dictionary does not change the
        rectangle."""
        r = Rectangle(1, 1, 0, 0, 1)
        d = r.to_dictionary()
        d["width"] = 50
        self.assertEqual(r.width, 1)

    def test_dictionary_does_not_use_private_names(self):
        """Check that the keys are not the private names."""
        keys = Rectangle(1, 1).to_dictionary()
        self.assertFalse(any(key.startswith("_") for key in keys))

    def test_update_with_own_dictionary(self):
        """Check that a dictionary can feed the update method."""
        r1 = Rectangle(10, 2, 1, 9)
        r2 = Rectangle(1, 1)
        r2.update(**r1.to_dictionary())
        self.assertEqual(str(r2), "[Rectangle] (1) 1/9 - 10/2")
        self.assertFalse(r1 == r2)

    def test_values_are_integers(self):
        """Check that all the values are integers."""
        d = Rectangle(1, 2, 3, 4, 5).to_dictionary()
        self.assertTrue(all(type(value) is int for value in d.values()))


class TestRectangleJson(unittest.TestCase):
    """Tests of the JSON helpers used by Rectangle."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_to_json_string_example(self):
        """Check the JSON text of the project example."""
        d = Rectangle(10, 7, 2, 8).to_dictionary()
        text = Base.to_json_string([d])
        self.assertIs(type(text), str)
        self.assertEqual(json.loads(text),
                         [{"x": 2, "width": 10, "id": 1, "height": 7, "y": 8}])

    def test_save_to_file_example(self):
        """Check the file saved by the project example."""
        Rectangle.save_to_file([Rectangle(10, 7, 2, 8), Rectangle(2, 4)])
        expected = [{"y": 8, "x": 2, "id": 1, "width": 10, "height": 7},
                    {"y": 0, "x": 0, "id": 2, "width": 2, "height": 4}]
        self.assertEqual(json.loads(read_file("Rectangle.json")), expected)

    def test_save_to_file_none(self):
        """Check that None saves an empty list."""
        Rectangle.save_to_file(None)
        self.assertEqual(read_file("Rectangle.json"), "[]")

    def test_save_to_file_empty(self):
        """Check that an empty list saves an empty list."""
        Rectangle.save_to_file([])
        self.assertEqual(read_file("Rectangle.json"), "[]")

    def test_save_to_file_overwrites(self):
        """Check that a second save replaces the first one."""
        Rectangle.save_to_file([Rectangle(1, 1), Rectangle(2, 2)])
        Rectangle.save_to_file([Rectangle(3, 3)])
        data = json.loads(read_file("Rectangle.json"))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["width"], 3)

    def test_from_json_string_example(self):
        """Check the list read by the project example."""
        data = [{"id": 89, "width": 10, "height": 4},
                {"id": 7, "width": 1, "height": 7}]
        text = Base.to_json_string(data)
        self.assertEqual(Base.from_json_string(text), data)

    def test_create_example(self):
        """Check the creation of the project example."""
        r1 = Rectangle(3, 5, 1)
        r2 = Rectangle.create(**r1.to_dictionary())
        self.assertEqual(str(r1), "[Rectangle] (1) 1/0 - 3/5")
        self.assertEqual(str(r2), "[Rectangle] (1) 1/0 - 3/5")
        self.assertIsNot(r1, r2)
        self.assertFalse(r1 == r2)

    def test_create_type(self):
        """Check that create returns a Rectangle."""
        self.assertIs(type(Rectangle.create(width=2, height=3)), Rectangle)

    def test_create_with_all_attributes(self):
        """Check that create applies every attribute."""
        r = Rectangle.create(id=5, width=6, height=7, x=8, y=9)
        self.assertEqual(str(r), "[Rectangle] (5) 8/9 - 6/7")

    def test_load_from_file_missing(self):
        """Check that a missing file gives an empty list."""
        self.assertEqual(Rectangle.load_from_file(), [])

    def test_load_from_file_example(self):
        """Check the objects loaded by the project example."""
        r1 = Rectangle(10, 7, 2, 8)
        r2 = Rectangle(2, 4)
        Rectangle.save_to_file([r1, r2])
        loaded = Rectangle.load_from_file()
        self.assertEqual([str(r) for r in loaded], [str(r1), str(r2)])
        self.assertTrue(all(o is not s for o, s in zip(loaded, [r1, r2])))

    def test_load_from_file_types(self):
        """Check the types of the loaded objects."""
        Rectangle.save_to_file([Rectangle(1, 1)])
        loaded = Rectangle.load_from_file()
        self.assertIs(type(loaded), list)
        self.assertIs(type(loaded[0]), Rectangle)


class TestRectangleCsv(unittest.TestCase):
    """Tests of the CSV methods used by Rectangle."""

    def setUp(self):
        """Reset the id counter and remove the generated files."""
        reset_counter()
        remove_json_files()
        remove_csv_files()

    def tearDown(self):
        """Remove the files created by the test."""
        remove_json_files()
        remove_csv_files()

    def test_save_example_rows(self):
        """Check the rows saved for the project example."""
        Rectangle.save_to_file_csv([Rectangle(10, 7, 2, 8), Rectangle(2, 4)])
        self.assertEqual(csv_lines("Rectangle.csv"),
                         ["1,10,7,2,8", "2,2,4,0,0"])

    def test_save_filename(self):
        """Check that the file is named Rectangle.csv."""
        Rectangle.save_to_file_csv([Rectangle(1, 1)])
        self.assertTrue(os.path.exists("Rectangle.csv"))
        self.assertFalse(os.path.exists("Square.csv"))

    def test_save_column_order(self):
        """Check the order id, width, height, x, y of the columns."""
        Rectangle.save_to_file_csv([Rectangle(2, 3, 4, 5, 1)])
        self.assertEqual(csv_lines("Rectangle.csv"), ["1,2,3,4,5"])

    def test_save_distinct_values(self):
        """Check that every value goes to its own column."""
        Rectangle.save_to_file_csv([Rectangle(11, 22, 33, 44, 55)])
        with open("Rectangle.csv", "r", newline="") as file:
            row = list(csv.reader(file))[0]
        self.assertEqual(row, ["55", "11", "22", "33", "44"])

    def test_save_default_x_and_y(self):
        """Check the zero values written for the default x and y."""
        Rectangle.save_to_file_csv([Rectangle(3, 4, id=6)])
        self.assertEqual(csv_lines("Rectangle.csv"), ["6,3,4,0,0"])

    def test_save_none(self):
        """Check that None writes an empty file."""
        Rectangle.save_to_file_csv(None)
        self.assertEqual(read_file("Rectangle.csv"), "")

    def test_save_empty_list(self):
        """Check that an empty list writes an empty file."""
        Rectangle.save_to_file_csv([])
        self.assertEqual(read_file("Rectangle.csv"), "")

    def test_save_one_object(self):
        """Check that one object gives exactly one line."""
        Rectangle.save_to_file_csv([Rectangle(5, 6, 7, 8, 9)])
        self.assertEqual(csv_lines("Rectangle.csv"), ["9,5,6,7,8"])

    def test_save_several_objects(self):
        """Check that several objects give one line each, in order."""
        Rectangle.save_to_file_csv(
            [Rectangle(i + 1, i + 2, i, i, i + 10) for i in range(4)])
        self.assertEqual(csv_lines("Rectangle.csv"),
                         ["10,1,2,0,0", "11,2,3,1,1",
                          "12,3,4,2,2", "13,4,5,3,3"])

    def test_save_overwrites(self):
        """Check that a second save replaces the first one."""
        Rectangle.save_to_file_csv([Rectangle(1, 1), Rectangle(2, 2)])
        Rectangle.save_to_file_csv([Rectangle(3, 3)])
        self.assertEqual(csv_lines("Rectangle.csv"), ["3,3,3,0,0"])

    def test_save_does_not_append(self):
        """Check that saving the same object twice gives one line."""
        r = Rectangle(1, 2)
        Rectangle.save_to_file_csv([r])
        Rectangle.save_to_file_csv([r])
        self.assertEqual(csv_lines("Rectangle.csv"), ["1,1,2,0,0"])

    def test_save_has_no_header(self):
        """Check that the first line is the first object."""
        Rectangle.save_to_file_csv([Rectangle(4, 5, 6, 7, 8)])
        self.assertEqual(csv_lines("Rectangle.csv")[0], "8,4,5,6,7")

    def test_save_is_not_json(self):
        """Check that the file does not hold JSON text."""
        Rectangle.save_to_file_csv([Rectangle(4, 5, 6, 7, 8)])
        self.assertNotIn("width", read_file("Rectangle.csv"))
        self.assertNotIn("{", read_file("Rectangle.csv"))

    def test_load_missing_file(self):
        """Check that a missing file gives an empty list."""
        self.assertEqual(Rectangle.load_from_file_csv(), [])

    def test_load_example(self):
        """Check the objects loaded by the project example."""
        r1 = Rectangle(10, 7, 2, 8)
        r2 = Rectangle(2, 4)
        Rectangle.save_to_file_csv([r1, r2])
        loaded = Rectangle.load_from_file_csv()
        self.assertEqual([str(r) for r in loaded],
                         ["[Rectangle] (1) 2/8 - 10/7",
                          "[Rectangle] (2) 0/0 - 2/4"])
        self.assertTrue(all(o is not s for o, s in zip(loaded, [r1, r2])))

    def test_load_types(self):
        """Check the types of the loaded objects."""
        Rectangle.save_to_file_csv([Rectangle(1, 1), Rectangle(2, 2)])
        loaded = Rectangle.load_from_file_csv()
        self.assertIs(type(loaded), list)
        self.assertEqual(len(loaded), 2)
        self.assertTrue(all(type(r) is Rectangle for r in loaded))

    def test_load_values_are_integers(self):
        """Check that the loaded values are integers and not text."""
        Rectangle.save_to_file_csv([Rectangle(10, 7, 2, 8, 3)])
        r = Rectangle.load_from_file_csv()[0]
        for value in (r.id, r.width, r.height, r.x, r.y):
            self.assertIs(type(value), int)
        self.assertEqual(r.area(), 70)

    def test_load_columns(self):
        """Check which column goes to which attribute."""
        write_raw("Rectangle.csv", "55,11,22,33,44\r\n")
        r = Rectangle.load_from_file_csv()[0]
        self.assertEqual((r.id, r.width, r.height, r.x, r.y),
                         (55, 11, 22, 33, 44))

    def test_load_empty_file(self):
        """Check that an empty file gives an empty list."""
        write_raw("Rectangle.csv", "")
        self.assertEqual(Rectangle.load_from_file_csv(), [])

    def test_load_trailing_blank_row(self):
        """Check that a trailing blank row gives no extra object."""
        write_raw("Rectangle.csv", "1,10,7,2,8\r\n2,2,4,0,0\r\n\r\n")
        self.assertEqual(len(Rectangle.load_from_file_csv()), 2)

    def test_load_without_final_newline(self):
        """Check that a last row without a line ending is read."""
        write_raw("Rectangle.csv", "1,10,7,2,8\n2,2,4,0,0")
        self.assertEqual(len(Rectangle.load_from_file_csv()), 2)

    def test_load_does_not_read_square_file(self):
        """Check that Rectangle does not read Square.csv."""
        write_raw("Square.csv", "5,5,0,0\r\n6,6,0,0\r\n")
        self.assertEqual(Rectangle.load_from_file_csv(), [])

    def test_load_does_not_read_json_file(self):
        """Check that Rectangle does not read Rectangle.json."""
        Rectangle.save_to_file([Rectangle(1, 2)])
        self.assertEqual(Rectangle.load_from_file_csv(), [])

    def test_load_after_empty_save(self):
        """Check that an empty save is loaded as an empty list."""
        Rectangle.save_to_file_csv(None)
        self.assertEqual(Rectangle.load_from_file_csv(), [])
        Rectangle.save_to_file_csv([])
        self.assertEqual(Rectangle.load_from_file_csv(), [])

    def test_round_trip_attributes(self):
        """Check that the attributes survive a save and a load."""
        r1 = Rectangle(10, 7, 2, 8, 41)
        r2 = Rectangle(2, 4, 0, 0, 42)
        Rectangle.save_to_file_csv([r1, r2])
        loaded = Rectangle.load_from_file_csv()
        for original, copy in zip([r1, r2], loaded):
            self.assertEqual(copy.id, original.id)
            self.assertEqual(copy.width, original.width)
            self.assertEqual(copy.height, original.height)
            self.assertEqual(copy.x, original.x)
            self.assertEqual(copy.y, original.y)
            self.assertEqual(copy.to_dictionary(), original.to_dictionary())

    def test_round_trip_identity(self):
        """Check that the loaded objects are new objects."""
        r1 = Rectangle(10, 7, 2, 8)
        Rectangle.save_to_file_csv([r1])
        copy = Rectangle.load_from_file_csv()[0]
        self.assertIsNot(copy, r1)
        self.assertNotEqual(id(copy), id(r1))
        self.assertFalse(copy == r1)
        self.assertEqual(str(copy), str(r1))

    def test_loaded_objects_are_usable(self):
        """Check that a loaded object works like any Rectangle."""
        Rectangle.save_to_file_csv([Rectangle(3, 2, 1, 4)])
        r = Rectangle.load_from_file_csv()[0]
        self.assertEqual(r.area(), 6)
        r.update(width=5)
        self.assertEqual(str(r), "[Rectangle] (1) 1/4 - 5/2")

    def test_round_trip_keeps_file_content(self):
        """Check that saving the loaded objects keeps the same file."""
        Rectangle.save_to_file_csv([Rectangle(10, 7, 2, 8), Rectangle(2, 4)])
        before = read_file("Rectangle.csv")
        Rectangle.save_to_file_csv(Rectangle.load_from_file_csv())
        self.assertEqual(read_file("Rectangle.csv"), before)
