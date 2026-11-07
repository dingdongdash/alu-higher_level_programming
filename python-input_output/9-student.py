#!/usr/bin/python3
"""Module that defines a class describing a student."""


class Student:
    """Class that describes a student by a name, a last name and an age."""

    def __init__(self, first_name, last_name, age):
        """Initialize a student with a first name, a last name and an age."""
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def to_json(self):
        """Return the dictionary representation of the student instance."""
        return self.__dict__
