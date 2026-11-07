#!/usr/bin/python3
"""Module that defines a class describing a student able to be reloaded."""


class Student:
    """Class that describes a student by a name, a last name and an age."""

    def __init__(self, first_name, last_name, age):
        """Initialize a student with a first name, a last name and an age."""
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def to_json(self, attrs=None):
        """Return the dictionary representation of the student instance.

        When attrs is a list of strings, only the attributes named in that
        list are retrieved, otherwise every attribute is retrieved.
        """
        if isinstance(attrs, list) and all(isinstance(a, str) for a in attrs):
            return {k: v for k, v in self.__dict__.items() if k in attrs}
        return self.__dict__

    def reload_from_json(self, json):
        """Replace the attributes of the student with the ones of a dictionary.

        Each key of the dictionary is the name of a public attribute and each
        value is the new value of that attribute.
        """
        for name, value in json.items():
            setattr(self, name, value)
