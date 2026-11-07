#!/usr/bin/python3
"""Unittest for max_integer([..])
"""
import unittest
max_integer = __import__('6-max_integer').max_integer


class TestMaxInteger(unittest.TestCase):
    """Test cases for the max_integer function"""

    def test_ordered_ascending(self):
        """Max is at the end of an ascending list"""
        self.assertEqual(max_integer([1, 2, 3, 4]), 4)

    def test_ordered_descending(self):
        """Max is at the beginning of a descending list"""
        self.assertEqual(max_integer([4, 3, 2, 1]), 4)

    def test_unordered(self):
        """Max is found in an unordered list"""
        self.assertEqual(max_integer([1, 3, 4, 2]), 4)
        self.assertEqual(max_integer([3, 1, 4, 1, 5, 9, 2, 6]), 9)

    def test_max_at_beginning(self):
        """Max is at the beginning of the list"""
        self.assertEqual(max_integer([9, 1, 2, 3]), 9)

    def test_max_in_middle(self):
        """Max is in the middle of the list"""
        self.assertEqual(max_integer([1, 2, 9, 3, 4]), 9)
        self.assertEqual(max_integer([1, 9, 3]), 9)

    def test_max_at_end(self):
        """Max is at the end of the list"""
        self.assertEqual(max_integer([1, 2, 3, 9]), 9)

    def test_one_element(self):
        """A list with one element returns that element"""
        self.assertEqual(max_integer([7]), 7)
        self.assertEqual(max_integer([-7]), -7)
        self.assertEqual(max_integer([0]), 0)

    def test_two_elements(self):
        """Lists with two elements in both orders"""
        self.assertEqual(max_integer([1, 2]), 2)
        self.assertEqual(max_integer([2, 1]), 2)

    def test_negative_numbers(self):
        """Max of a list of negative numbers"""
        self.assertEqual(max_integer([-5, -3, -9, -1, -7]), -1)
        self.assertEqual(max_integer([-1, -2, -3]), -1)
        self.assertEqual(max_integer([-3, -2, -1]), -1)

    def test_negative_and_positive_numbers(self):
        """Max of a list with negative and positive numbers"""
        self.assertEqual(max_integer([-10, 5, -3, 2]), 5)
        self.assertEqual(max_integer([-10, 0, -3]), 0)

    def test_zero(self):
        """Zero is the max of a list without positive numbers"""
        self.assertEqual(max_integer([0, 0, 0]), 0)
        self.assertEqual(max_integer([-1, 0, -2]), 0)

    def test_duplicate_max(self):
        """The max can be present several times"""
        self.assertEqual(max_integer([5, 1, 5, 2, 5]), 5)
        self.assertEqual(max_integer([1, 5, 5]), 5)
        self.assertEqual(max_integer([5, 5, 1]), 5)

    def test_all_equal(self):
        """All elements are equal"""
        self.assertEqual(max_integer([3, 3, 3, 3]), 3)
        self.assertEqual(max_integer([-3, -3]), -3)

    def test_floats(self):
        """Max of a list of floats"""
        self.assertEqual(max_integer([1.5, 2.5, 0.5]), 2.5)
        self.assertEqual(max_integer([-1.5, -2.5, -0.5]), -0.5)
        self.assertEqual(max_integer([0.1, 0.2, 0.3]), 0.3)

    def test_ints_and_floats(self):
        """Max of a list that mixes integers and floats"""
        self.assertEqual(max_integer([1, 2.5, 2]), 2.5)
        self.assertEqual(max_integer([3, 2.5, 1.5]), 3)
        self.assertEqual(max_integer([1.5, 2, 1]), 2)

    def test_equal_int_and_float(self):
        """The first of two equal values is returned"""
        self.assertIsInstance(max_integer([1, 1.0]), int)
        self.assertIsInstance(max_integer([1.0, 1]), float)
        self.assertIsInstance(max_integer([0, 1, 1.0]), int)

    def test_negative_zero(self):
        """Negative zero is equal to zero"""
        self.assertEqual(max_integer([-0.0, 0]), 0)
        self.assertEqual(max_integer([0, -0.0]), 0)
        self.assertEqual(max_integer([-1, -0.0]), 0)

    def test_big_numbers(self):
        """Max of a list of very large integers"""
        self.assertEqual(max_integer([10 ** 30, 10 ** 30 + 1, 10 ** 29]),
                         10 ** 30 + 1)
        self.assertEqual(max_integer([-10 ** 30, -10 ** 31]), -10 ** 30)
        self.assertEqual(max_integer([2 ** 100, 2 ** 99]), 2 ** 100)

    def test_long_list(self):
        """Max of a long list"""
        self.assertEqual(max_integer(list(range(1000))), 999)
        self.assertEqual(max_integer(list(range(1000, 0, -1))), 1000)
        self.assertEqual(max_integer([1] * 500 + [2] + [1] * 500), 2)

    def test_empty_list(self):
        """An empty list returns None"""
        self.assertIsNone(max_integer([]))

    def test_no_argument(self):
        """The default argument is an empty list"""
        self.assertIsNone(max_integer())

    def test_keyword_argument(self):
        """The argument is named list"""
        self.assertEqual(max_integer(list=[3, 9, 4]), 9)
        self.assertIsNone(max_integer(list=[]))

    def test_list_is_not_modified(self):
        """The list given is left unchanged"""
        numbers = [3, 1, 4, 1, 5]
        max_integer(numbers)
        self.assertEqual(numbers, [3, 1, 4, 1, 5])

    def test_list_of_strings(self):
        """Strings are compared alphabetically"""
        self.assertEqual(max_integer(["a", "c", "b"]), "c")
        self.assertEqual(max_integer(["abc", "abd", "ab"]), "abd")
        self.assertEqual(max_integer(["z"]), "z")

    def test_tuple(self):
        """A tuple is accepted as it can be indexed"""
        self.assertEqual(max_integer((1, 5, 3)), 5)
        self.assertIsNone(max_integer(()))

    def test_string(self):
        """A string is read character by character"""
        self.assertEqual(max_integer("abc"), "c")
        self.assertEqual(max_integer("cab"), "c")
        self.assertIsNone(max_integer(""))

    def test_list_of_lists(self):
        """Lists are compared element by element"""
        self.assertEqual(max_integer([[1, 2], [1, 3], [0, 9]]), [1, 3])
        self.assertEqual(max_integer([[1], [1, 0]]), [1, 0])

    def test_none_argument(self):
        """None has no length"""
        with self.assertRaises(TypeError):
            max_integer(None)

    def test_integer_argument(self):
        """An integer has no length"""
        with self.assertRaises(TypeError):
            max_integer(5)

    def test_float_argument(self):
        """A float has no length"""
        with self.assertRaises(TypeError):
            max_integer(1.5)

    def test_incomparable_elements(self):
        """Integers and strings can not be compared"""
        with self.assertRaises(TypeError):
            max_integer([1, "a"])
        with self.assertRaises(TypeError):
            max_integer(["a", 1])
        with self.assertRaises(TypeError):
            max_integer([1, 2, "a"])
        with self.assertRaises(TypeError):
            max_integer([1, None])

    def test_integer_and_list_elements(self):
        """Integers and lists can not be compared"""
        with self.assertRaises(TypeError):
            max_integer([1, [2]])


if __name__ == '__main__':
    unittest.main()
