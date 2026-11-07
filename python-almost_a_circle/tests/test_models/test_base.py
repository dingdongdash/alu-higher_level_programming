#!/usr/bin/python3
"""Unit tests for the Base class of the models package.

The tests cover the identifier management and the JSON helpers, the file
methods and the creation of instances of the Base class and its subclasses.
"""
import inspect
import io
import json
import os
import re
import unittest
from unittest.mock import patch

from models import base as base_module
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


class TestBaseId(unittest.TestCase):
    """Tests of the identifier management of Base."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_first_id_is_one(self):
        """Check that the first object receives the id 1."""
        b1 = Base()
        self.assertEqual(b1.id, 1)

    def test_ids_are_consecutive(self):
        """Check that the generated ids increase by one."""
        b1 = Base()
        b2 = Base()
        b3 = Base()
        self.assertEqual((b1.id, b2.id, b3.id), (1, 2, 3))

    def test_explicit_id_is_kept(self):
        """Check that an explicit id is assigned."""
        b4 = Base(12)
        self.assertEqual(b4.id, 12)

    def test_explicit_id_keyword(self):
        """Check that the id can be given by keyword."""
        b1 = Base(id=77)
        self.assertEqual(b1.id, 77)

    def test_negative_explicit_id(self):
        """Check that a negative explicit id is kept."""
        b1 = Base(-5)
        self.assertEqual(b1.id, -5)

    def test_explicit_id_keeps_counter(self):
        """Check that an explicit id does not use the counter."""
        Base(12)
        b2 = Base()
        self.assertEqual(b2.id, 1)

    def test_mixed_ids_sequence(self):
        """Check the sequence of ids mixing explicit and generated
        values."""
        ids = [Base().id, Base().id, Base().id, Base(12).id, Base().id]
        self.assertEqual(ids, [1, 2, 3, 12, 4])

    def test_counter_starts_at_zero(self):
        """Check that the private counter can be reset to zero."""
        self.assertEqual(Base._Base__nb_objects, 0)

    def test_counter_increments(self):
        """Check that the private counter counts the generated ids."""
        Base()
        Base()
        self.assertEqual(Base._Base__nb_objects, 2)

    def test_counter_ignores_explicit_ids(self):
        """Check that the private counter ignores explicit ids."""
        Base(5)
        Base(6)
        self.assertEqual(Base._Base__nb_objects, 0)

    def test_counter_is_private(self):
        """Check that the counter is not a public attribute."""
        self.assertFalse(hasattr(Base, "__nb_objects"))
        self.assertFalse(hasattr(Base, "nb_objects"))
        self.assertTrue(hasattr(Base, "_Base__nb_objects"))

    def test_id_is_instance_attribute(self):
        """Check that the id is stored in the instance."""
        b1 = Base()
        self.assertIn("id", b1.__dict__)
        self.assertNotIn("id", Base.__dict__)

    def test_id_can_be_reassigned(self):
        """Check that the public id can be changed."""
        b1 = Base()
        b1.id = 50
        self.assertEqual(b1.id, 50)

    def test_instances_have_different_ids(self):
        """Check that two generated ids are different."""
        self.assertNotEqual(Base().id, Base().id)

    def test_no_argument_constructor(self):
        """Check that the constructor works without any argument."""
        self.assertIsInstance(Base(), Base)

    def test_constructor_signature(self):
        """Check the parameters of the constructor."""
        params = inspect.signature(Base.__init__).parameters
        self.assertEqual(list(params), ["self", "id"])
        self.assertIsNone(params["id"].default)

    def test_instances_are_not_equal(self):
        """Check that two instances are not equal."""
        self.assertFalse(Base(1) == Base(1))

    def test_rectangle_shares_counter(self):
        """Check that Rectangle and Square use the counter of Base."""
        r1 = Rectangle(1, 1)
        b2 = Base()
        s3 = Square(1)
        self.assertEqual((r1.id, b2.id, s3.id), (1, 2, 3))

    def test_subclass_explicit_id_keeps_counter(self):
        """Check that explicit ids of subclasses do not use the counter."""
        Rectangle(1, 1, 0, 0, 40)
        Square(1, 0, 0, 41)
        self.assertEqual(Base().id, 1)

    def test_class_counter_after_subclasses(self):
        """Check that the counter counts subclass instances too."""
        Rectangle(1, 1)
        Square(2)
        self.assertEqual(Base._Base__nb_objects, 2)


class TestToJsonString(unittest.TestCase):
    """Tests of the to_json_string static method."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_none_gives_empty_list(self):
        """Check that None gives the string of an empty list."""
        self.assertEqual(Base.to_json_string(None), "[]")

    def test_empty_list_gives_empty_list(self):
        """Check that an empty list gives the string of an empty list."""
        self.assertEqual(Base.to_json_string([]), "[]")

    def test_returns_a_string(self):
        """Check that the result is a string."""
        result = Base.to_json_string([{"id": 1}])
        self.assertIs(type(result), str)

    def test_none_result_is_a_string(self):
        """Check that the result for None is a string."""
        self.assertIs(type(Base.to_json_string(None)), str)

    def test_single_dictionary_text(self):
        """Check the exact text of a single dictionary."""
        self.assertEqual(Base.to_json_string([{"id": 1}]), '[{"id": 1}]')

    def test_two_dictionaries_text(self):
        """Check the exact text of two dictionaries."""
        text = Base.to_json_string([{"id": 1}, {"id": 2}])
        self.assertEqual(text, '[{"id": 1}, {"id": 2}]')

    def test_empty_dictionary_in_list(self):
        """Check that a list holding an empty dictionary is not empty."""
        self.assertEqual(Base.to_json_string([{}]), "[{}]")

    def test_string_values(self):
        """Check that string values are quoted."""
        self.assertEqual(Base.to_json_string([{"a": "b"}]), '[{"a": "b"}]')

    def test_rectangle_dictionary_round_trip(self):
        """Check that a rectangle dictionary survives the conversion."""
        dictionary = Rectangle(10, 7, 2, 8).to_dictionary()
        text = Base.to_json_string([dictionary])
        self.assertEqual(json.loads(text), [dictionary])

    def test_square_dictionary_round_trip(self):
        """Check that a square dictionary survives the conversion."""
        dictionary = Square(3, 1, 2).to_dictionary()
        text = Base.to_json_string([dictionary])
        self.assertEqual(json.loads(text), [dictionary])

    def test_many_dictionaries_round_trip(self):
        """Check that several dictionaries keep their order."""
        dictionaries = [{"id": 89, "width": 10, "height": 4},
                        {"id": 7, "width": 1, "height": 7},
                        {"id": 3, "width": 2, "height": 2}]
        text = Base.to_json_string(dictionaries)
        self.assertEqual(json.loads(text), dictionaries)

    def test_input_is_not_modified(self):
        """Check that the given list is not modified."""
        dictionaries = [{"id": 1}]
        Base.to_json_string(dictionaries)
        self.assertEqual(dictionaries, [{"id": 1}])

    def test_is_static_method(self):
        """Check that the method is a static method."""
        self.assertIsInstance(Base.__dict__["to_json_string"], staticmethod)

    def test_callable_on_subclass(self):
        """Check that the method can be used through a subclass."""
        self.assertEqual(Rectangle.to_json_string([{"id": 1}]), '[{"id": 1}]')
        self.assertEqual(Square.to_json_string(None), "[]")


class TestFromJsonString(unittest.TestCase):
    """Tests of the from_json_string static method."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_none_gives_empty_list(self):
        """Check that None gives an empty list."""
        self.assertEqual(Base.from_json_string(None), [])

    def test_empty_string_gives_empty_list(self):
        """Check that an empty string gives an empty list."""
        self.assertEqual(Base.from_json_string(""), [])

    def test_empty_json_list(self):
        """Check that the text of an empty list gives an empty list."""
        self.assertEqual(Base.from_json_string("[]"), [])

    def test_none_result_is_a_list(self):
        """Check that the result for None is a list."""
        self.assertIs(type(Base.from_json_string(None)), list)

    def test_returns_a_list(self):
        """Check that the result is a list."""
        result = Base.from_json_string('[{"id": 1}]')
        self.assertIs(type(result), list)

    def test_single_dictionary(self):
        """Check the conversion of one dictionary."""
        result = Base.from_json_string('[{"id": 1, "width": 2}]')
        self.assertEqual(result, [{"id": 1, "width": 2}])

    def test_two_dictionaries(self):
        """Check the conversion of two dictionaries."""
        text = '[{"id": 89, "width": 10}, {"id": 7, "width": 1}]'
        expected = [{"id": 89, "width": 10}, {"id": 7, "width": 1}]
        self.assertEqual(Base.from_json_string(text), expected)

    def test_elements_are_dictionaries(self):
        """Check that the elements of the result are dictionaries."""
        result = Base.from_json_string('[{"id": 1}, {"id": 2}]')
        self.assertTrue(all(type(item) is dict for item in result))

    def test_example_round_trip(self):
        """Check the round trip of the project example."""
        data = [{"id": 89, "width": 10, "height": 4},
                {"id": 7, "width": 1, "height": 7}]
        result = Base.from_json_string(Base.to_json_string(data))
        self.assertEqual(result, data)
        self.assertIsNot(result, data)

    def test_rectangle_dictionaries_round_trip(self):
        """Check the round trip of rectangle dictionaries."""
        data = [Rectangle(10, 7, 2, 8).to_dictionary(),
                Rectangle(2, 4).to_dictionary()]
        result = Base.from_json_string(Base.to_json_string(data))
        self.assertEqual(result, data)

    def test_square_dictionaries_round_trip(self):
        """Check the round trip of square dictionaries."""
        data = [Square(5).to_dictionary(), Square(7, 9, 1).to_dictionary()]
        result = Base.from_json_string(Base.to_json_string(data))
        self.assertEqual(result, data)

    def test_is_static_method(self):
        """Check that the method is a static method."""
        self.assertIsInstance(Base.__dict__["from_json_string"], staticmethod)

    def test_callable_on_subclass(self):
        """Check that the method can be used through a subclass."""
        self.assertEqual(Square.from_json_string('[{"id": 1}]'), [{"id": 1}])
        self.assertEqual(Rectangle.from_json_string(None), [])


class TestSaveToFile(unittest.TestCase):
    """Tests of the save_to_file class method."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_rectangle_file_is_created(self):
        """Check that a Rectangle.json file is created."""
        Rectangle.save_to_file([Rectangle(1, 2)])
        self.assertTrue(os.path.exists("Rectangle.json"))

    def test_square_file_is_created(self):
        """Check that a Square.json file is created."""
        Square.save_to_file([Square(1)])
        self.assertTrue(os.path.exists("Square.json"))

    def test_rectangle_content(self):
        """Check the content of the file of rectangles."""
        r1 = Rectangle(10, 7, 2, 8)
        r2 = Rectangle(2, 4)
        Rectangle.save_to_file([r1, r2])
        expected = [r1.to_dictionary(), r2.to_dictionary()]
        self.assertEqual(json.loads(read_file("Rectangle.json")), expected)

    def test_square_content(self):
        """Check the content of the file of squares."""
        s1 = Square(5)
        s2 = Square(7, 9, 1)
        Square.save_to_file([s1, s2])
        expected = [s1.to_dictionary(), s2.to_dictionary()]
        self.assertEqual(json.loads(read_file("Square.json")), expected)

    def test_single_rectangle_content(self):
        """Check the file content for one rectangle."""
        r1 = Rectangle(3, 4, 5, 6, 7)
        Rectangle.save_to_file([r1])
        expected = {"id": 7, "width": 3, "height": 4, "x": 5, "y": 6}
        self.assertEqual(json.loads(read_file("Rectangle.json")), [expected])

    def test_single_square_content(self):
        """Check the file content for one square."""
        s1 = Square(3, 5, 6, 7)
        Square.save_to_file([s1])
        expected = {"id": 7, "size": 3, "x": 5, "y": 6}
        self.assertEqual(json.loads(read_file("Square.json")), [expected])

    def test_rectangle_none(self):
        """Check that None saves an empty list for Rectangle."""
        Rectangle.save_to_file(None)
        self.assertEqual(read_file("Rectangle.json"), "[]")

    def test_square_none(self):
        """Check that None saves an empty list for Square."""
        Square.save_to_file(None)
        self.assertEqual(read_file("Square.json"), "[]")

    def test_rectangle_empty_list(self):
        """Check that an empty list saves an empty list for Rectangle."""
        Rectangle.save_to_file([])
        self.assertEqual(read_file("Rectangle.json"), "[]")

    def test_square_empty_list(self):
        """Check that an empty list saves an empty list for Square."""
        Square.save_to_file([])
        self.assertEqual(read_file("Square.json"), "[]")

    def test_base_file_name(self):
        """Check that Base saves in the file Base.json."""
        r1 = Rectangle(1, 2, 3, 4, 5)
        Base.save_to_file([r1])
        self.assertTrue(os.path.exists("Base.json"))
        self.assertEqual(json.loads(read_file("Base.json")),
                         [r1.to_dictionary()])

    def test_base_none(self):
        """Check that None saves an empty list for Base."""
        Base.save_to_file(None)
        self.assertEqual(read_file("Base.json"), "[]")

    def test_base_empty_list(self):
        """Check that an empty list saves an empty list for Base."""
        Base.save_to_file([])
        self.assertEqual(read_file("Base.json"), "[]")

    def test_rectangle_save_does_not_create_other_files(self):
        """Check that only the file of the class is created."""
        Rectangle.save_to_file([Rectangle(1, 2)])
        self.assertFalse(os.path.exists("Square.json"))
        self.assertFalse(os.path.exists("Base.json"))

    def test_square_save_does_not_create_other_files(self):
        """Check that a Square save does not create the Rectangle file."""
        Square.save_to_file([Square(1)])
        self.assertFalse(os.path.exists("Rectangle.json"))
        self.assertFalse(os.path.exists("Base.json"))

    def test_overwrite_with_fewer_objects(self):
        """Check that an existing file is overwritten and not extended."""
        r1 = Rectangle(1, 2)
        r2 = Rectangle(3, 4)
        Rectangle.save_to_file([r1, r2])
        Rectangle.save_to_file([r2])
        self.assertEqual(json.loads(read_file("Rectangle.json")),
                         [r2.to_dictionary()])

    def test_overwrite_with_same_objects(self):
        """Check that saving twice the same objects does not duplicate
        them."""
        r1 = Rectangle(1, 2)
        Rectangle.save_to_file([r1])
        Rectangle.save_to_file([r1])
        self.assertEqual(len(json.loads(read_file("Rectangle.json"))), 1)

    def test_overwrite_with_none(self):
        """Check that None overwrites an existing file."""
        Rectangle.save_to_file([Rectangle(1, 2)])
        Rectangle.save_to_file(None)
        self.assertEqual(read_file("Rectangle.json"), "[]")

    def test_overwrite_with_empty_list(self):
        """Check that an empty list overwrites an existing file."""
        Square.save_to_file([Square(1)])
        Square.save_to_file([])
        self.assertEqual(read_file("Square.json"), "[]")

    def test_overwrite_unrelated_content(self):
        """Check that unrelated text in the file is replaced."""
        write_file("Rectangle.json", "this is not json and it is quite long")
        r1 = Rectangle(1, 2)
        Rectangle.save_to_file([r1])
        self.assertEqual(json.loads(read_file("Rectangle.json")),
                         [r1.to_dictionary()])

    def test_overwrite_longer_content(self):
        """Check that no leftover remains after a shorter save."""
        r1 = Rectangle(1, 2)
        Rectangle.save_to_file([r1, r1, r1, r1])
        Rectangle.save_to_file([r1])
        text = read_file("Rectangle.json")
        self.assertEqual(json.loads(text), [r1.to_dictionary()])

    def test_file_holds_a_json_list(self):
        """Check that the file holds a JSON list."""
        Rectangle.save_to_file([Rectangle(1, 2)])
        self.assertIs(type(json.loads(read_file("Rectangle.json"))), list)

    def test_uses_to_json_string(self):
        """Check that the file content is built by the to_json_string
        method."""
        with patch.object(Base, "to_json_string",
                          return_value="[1, 2]") as mock:
            Rectangle.save_to_file([Rectangle(1, 2)])
        self.assertEqual(read_file("Rectangle.json"), "[1, 2]")
        self.assertTrue(mock.called)

    def test_to_json_string_receives_dictionaries(self):
        """Check that the dictionaries of the objects are given to
        to_json_string."""
        r1 = Rectangle(1, 2)
        with patch.object(Base, "to_json_string", return_value="[]") as mock:
            Rectangle.save_to_file([r1])
        mock.assert_called_with([r1.to_dictionary()])

    def test_list_of_objects_is_not_modified(self):
        """Check that the given list of objects is not modified."""
        objs = [Rectangle(1, 2), Rectangle(3, 4)]
        Rectangle.save_to_file(objs)
        self.assertEqual(len(objs), 2)

    def test_saved_file_matches_to_json_string(self):
        """Check that the file equals the text built by to_json_string."""
        r1 = Rectangle(1, 2)
        Rectangle.save_to_file([r1])
        expected = Base.to_json_string([r1.to_dictionary()])
        self.assertEqual(read_file("Rectangle.json"), expected)

    def test_is_class_method(self):
        """Check that the method is a class method."""
        self.assertIsInstance(Base.__dict__["save_to_file"], classmethod)

    def test_many_objects(self):
        """Check the file content for many objects."""
        objs = [Rectangle(n + 1, n + 2, n, n) for n in range(6)]
        Rectangle.save_to_file(objs)
        expected = [obj.to_dictionary() for obj in objs]
        self.assertEqual(json.loads(read_file("Rectangle.json")), expected)


class TestCreate(unittest.TestCase):
    """Tests of the create class method."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_rectangle_create_full(self):
        """Check the creation of a full rectangle."""
        r1 = Rectangle.create(id=89, width=3, height=5, x=1, y=2)
        self.assertEqual(r1.to_dictionary(),
                         {"id": 89, "width": 3, "height": 5, "x": 1, "y": 2})

    def test_rectangle_create_string(self):
        """Check the text of a created rectangle."""
        r1 = Rectangle(3, 5, 1)
        r2 = Rectangle.create(**r1.to_dictionary())
        self.assertEqual(str(r2), "[Rectangle] (1) 1/0 - 3/5")

    def test_rectangle_create_type(self):
        """Check that the created object is a Rectangle."""
        r1 = Rectangle.create(width=3, height=5)
        self.assertIs(type(r1), Rectangle)

    def test_rectangle_create_is_new_object(self):
        """Check that the created rectangle is a new object."""
        r1 = Rectangle(3, 5, 1)
        r2 = Rectangle.create(**r1.to_dictionary())
        self.assertIsNot(r1, r2)
        self.assertFalse(r1 == r2)

    def test_rectangle_create_same_dictionary(self):
        """Check that a created rectangle has the same dictionary."""
        r1 = Rectangle(10, 7, 2, 8, 33)
        r2 = Rectangle.create(**r1.to_dictionary())
        self.assertEqual(r1.to_dictionary(), r2.to_dictionary())

    def test_rectangle_create_without_position(self):
        """Check the creation without a position."""
        r1 = Rectangle.create(id=4, width=6, height=7)
        self.assertEqual((r1.x, r1.y, r1.width, r1.height), (0, 0, 6, 7))

    def test_rectangle_create_only_position(self):
        """Check that an update with a position keeps the dummy sides."""
        r1 = Rectangle.create(x=3, y=4)
        self.assertEqual((r1.width, r1.height, r1.x, r1.y), (1, 1, 3, 4))

    def test_rectangle_create_explicit_id(self):
        """Check that the id of the dictionary is applied."""
        r1 = Rectangle.create(id=500, width=2, height=2)
        self.assertEqual(r1.id, 500)

    def test_square_create_full(self):
        """Check the creation of a full square."""
        s1 = Square.create(id=89, size=3, x=1, y=2)
        expected = {"id": 89, "size": 3, "x": 1, "y": 2}
        self.assertEqual(s1.to_dictionary(), expected)

    def test_square_create_string(self):
        """Check the text of a created square."""
        s1 = Square(5, 2, 3, 9)
        s2 = Square.create(**s1.to_dictionary())
        self.assertEqual(str(s2), "[Square] (9) 2/3 - 5")

    def test_square_create_type(self):
        """Check that the created object is a Square."""
        s1 = Square.create(size=4)
        self.assertIs(type(s1), Square)
        self.assertEqual((s1.width, s1.height), (4, 4))

    def test_square_create_is_new_object(self):
        """Check that the created square is a new object."""
        s1 = Square(5, 1, 1)
        s2 = Square.create(**s1.to_dictionary())
        self.assertIsNot(s1, s2)
        self.assertFalse(s1 == s2)

    def test_square_create_only_position(self):
        """Check that an update with a position keeps the dummy size."""
        s1 = Square.create(x=3, y=4)
        self.assertEqual((s1.size, s1.x, s1.y), (1, 3, 4))

    def test_square_create_same_dictionary(self):
        """Check that a created square has the same dictionary."""
        s1 = Square(5, 2, 3, 9)
        s2 = Square.create(**s1.to_dictionary())
        self.assertEqual(s1.to_dictionary(), s2.to_dictionary())

    def test_create_uses_update(self):
        """Check that the dictionary is applied with the update method."""
        original = Rectangle.update
        with patch.object(Rectangle, "update", autospec=True,
                          side_effect=original) as mock:
            r1 = Rectangle.create(id=8, width=3, height=4)
        self.assertTrue(mock.called)
        expected = {"id": 8, "width": 3, "height": 4}
        self.assertEqual(mock.call_args.kwargs, expected)
        self.assertEqual(r1.id, 8)

    def test_create_does_not_use_eval(self):
        """Check that the source of the module does not call the eval
        function."""
        source = inspect.getsource(base_module)
        self.assertIsNone(re.search(r"\beval\s*\(", source))

    def test_create_validates_values(self):
        """Check that created objects are validated by the update method."""
        with self.assertRaises(TypeError):
            Rectangle.create(width="3", height=4)
        with self.assertRaises(ValueError):
            Square.create(size=0)

    def test_is_class_method(self):
        """Check that the method is a class method."""
        self.assertIsInstance(Base.__dict__["create"], classmethod)


class TestLoadFromFile(unittest.TestCase):
    """Tests of the load_from_file class method."""

    def setUp(self):
        """Reset the id counter and remove the JSON files."""
        reset_counter()
        remove_json_files()

    def tearDown(self):
        """Remove the JSON files created by the test."""
        remove_json_files()

    def test_rectangle_missing_file(self):
        """Check that a missing file gives an empty list for Rectangle."""
        self.assertEqual(Rectangle.load_from_file(), [])

    def test_square_missing_file(self):
        """Check that a missing file gives an empty list for Square."""
        self.assertEqual(Square.load_from_file(), [])

    def test_base_missing_file(self):
        """Check that a missing file gives an empty list for Base."""
        self.assertEqual(Base.load_from_file(), [])

    def test_missing_file_result_type(self):
        """Check that the result for a missing file is a list."""
        self.assertIs(type(Rectangle.load_from_file()), list)

    def test_other_class_file_is_ignored(self):
        """Check that the file of another class is not read."""
        Rectangle.save_to_file([Rectangle(1, 2)])
        self.assertEqual(Square.load_from_file(), [])

    def test_rectangle_round_trip_strings(self):
        """Check that loaded rectangles have the same text."""
        r1 = Rectangle(10, 7, 2, 8)
        r2 = Rectangle(2, 4)
        Rectangle.save_to_file([r1, r2])
        loaded = Rectangle.load_from_file()
        self.assertEqual([str(r) for r in loaded], [str(r1), str(r2)])

    def test_rectangle_round_trip_dictionaries(self):
        """Check that loaded rectangles have the same dictionaries."""
        r1 = Rectangle(10, 7, 2, 8)
        r2 = Rectangle(2, 4)
        Rectangle.save_to_file([r1, r2])
        loaded = Rectangle.load_from_file()
        self.assertEqual([r.to_dictionary() for r in loaded],
                         [r1.to_dictionary(), r2.to_dictionary()])

    def test_rectangle_loaded_types(self):
        """Check that the loaded objects are Rectangle instances."""
        Rectangle.save_to_file([Rectangle(1, 2), Rectangle(3, 4)])
        loaded = Rectangle.load_from_file()
        self.assertIs(type(loaded), list)
        self.assertEqual(len(loaded), 2)
        self.assertTrue(all(type(r) is Rectangle for r in loaded))

    def test_rectangle_loaded_are_new_objects(self):
        """Check that the loaded rectangles are new objects."""
        r1 = Rectangle(10, 7, 2, 8)
        Rectangle.save_to_file([r1])
        loaded = Rectangle.load_from_file()
        self.assertIsNot(loaded[0], r1)
        self.assertFalse(loaded[0] == r1)

    def test_square_round_trip_strings(self):
        """Check that loaded squares have the same text."""
        s1 = Square(5)
        s2 = Square(7, 9, 1)
        Square.save_to_file([s1, s2])
        loaded = Square.load_from_file()
        self.assertEqual([str(s) for s in loaded], [str(s1), str(s2)])

    def test_square_round_trip_dictionaries(self):
        """Check that loaded squares have the same dictionaries."""
        s1 = Square(5)
        s2 = Square(7, 9, 1)
        Square.save_to_file([s1, s2])
        loaded = Square.load_from_file()
        self.assertEqual([s.to_dictionary() for s in loaded],
                         [s1.to_dictionary(), s2.to_dictionary()])

    def test_square_loaded_types(self):
        """Check that the loaded objects are Square instances."""
        Square.save_to_file([Square(1), Square(2)])
        loaded = Square.load_from_file()
        self.assertEqual(len(loaded), 2)
        self.assertTrue(all(type(s) is Square for s in loaded))

    def test_square_loaded_are_new_objects(self):
        """Check that the loaded squares are new objects."""
        s1 = Square(5, 1, 2)
        Square.save_to_file([s1])
        loaded = Square.load_from_file()
        self.assertIsNot(loaded[0], s1)
        self.assertFalse(loaded[0] == s1)

    def test_file_with_empty_list(self):
        """Check that a file holding an empty list gives an empty list."""
        write_file("Rectangle.json", "[]")
        self.assertEqual(Rectangle.load_from_file(), [])

    def test_saved_empty_list(self):
        """Check that a saved empty list gives an empty list."""
        Square.save_to_file([])
        self.assertEqual(Square.load_from_file(), [])

    def test_saved_none(self):
        """Check that a saved None gives an empty list."""
        Rectangle.save_to_file(None)
        self.assertEqual(Rectangle.load_from_file(), [])

    def test_handwritten_rectangle_file(self):
        """Check the loading of a file written by hand."""
        text = '[{"id": 9, "width": 4, "height": 3, "x": 2, "y": 1}]'
        write_file("Rectangle.json", text)
        loaded = Rectangle.load_from_file()
        self.assertEqual(str(loaded[0]), "[Rectangle] (9) 2/1 - 4/3")

    def test_handwritten_square_file(self):
        """Check the loading of a square file written by hand."""
        write_file("Square.json", '[{"id": 9, "size": 4, "x": 2, "y": 1}]')
        loaded = Square.load_from_file()
        self.assertEqual(str(loaded[0]), "[Square] (9) 2/1 - 4")

    def test_order_is_preserved(self):
        """Check that the loaded objects keep the saved order."""
        objs = [Rectangle(n + 1, n + 1, 0, 0, 100 + n) for n in range(5)]
        Rectangle.save_to_file(objs)
        loaded = Rectangle.load_from_file()
        self.assertEqual([r.id for r in loaded], [100, 101, 102, 103, 104])

    def test_loading_twice_gives_new_objects(self):
        """Check that two loads give different objects."""
        Rectangle.save_to_file([Rectangle(1, 2)])
        first = Rectangle.load_from_file()
        second = Rectangle.load_from_file()
        self.assertIsNot(first[0], second[0])
        self.assertEqual(str(first[0]), str(second[0]))

    def test_latest_save_is_loaded(self):
        """Check that a load reflects the latest save."""
        Rectangle.save_to_file([Rectangle(1, 2), Rectangle(3, 4)])
        Rectangle.save_to_file([Rectangle(5, 6)])
        loaded = Rectangle.load_from_file()
        self.assertEqual(len(loaded), 1)
        self.assertEqual((loaded[0].width, loaded[0].height), (5, 6))

    def test_uses_from_json_string(self):
        """Check that the file text is converted by from_json_string."""
        write_file("Rectangle.json", "[]")
        data = [{"id": 3, "width": 4, "height": 5}]
        with patch.object(Base, "from_json_string", return_value=data) as mock:
            loaded = Rectangle.load_from_file()
        self.assertTrue(mock.called)
        self.assertEqual(len(loaded), 1)
        self.assertEqual((loaded[0].id, loaded[0].width), (3, 4))

    def test_uses_create(self):
        """Check that each dictionary is turned into an object by create."""
        Rectangle.save_to_file([Rectangle(1, 2, 3, 4, 5), Rectangle(6, 7)])
        with patch.object(Rectangle, "create",
                          side_effect=lambda **d: d) as mock:
            loaded = Rectangle.load_from_file()
        self.assertEqual(mock.call_count, 2)
        self.assertEqual(loaded[0],
                         {"id": 5, "width": 1, "height": 2, "x": 3, "y": 4})

    def test_is_class_method(self):
        """Check that the method is a class method."""
        self.assertIsInstance(Base.__dict__["load_from_file"], classmethod)

    def test_main_example_ids(self):
        """Check the ids of the objects of the project example."""
        r1 = Rectangle(10, 7, 2, 8)
        r2 = Rectangle(2, 4)
        Rectangle.save_to_file([r1, r2])
        loaded = Rectangle.load_from_file()
        s1 = Square(5)
        s2 = Square(7, 9, 1)
        Square.save_to_file([s1, s2])
        loaded_squares = Square.load_from_file()
        expected = ["[Rectangle] (1) 2/8 - 10/7", "[Rectangle] (2) 0/0 - 2/4"]
        self.assertEqual([str(r) for r in loaded], expected)
        self.assertEqual([str(s) for s in loaded_squares],
                         [str(s1), str(s2)])
