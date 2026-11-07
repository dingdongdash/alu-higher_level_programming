#!/usr/bin/python3
"""Module that defines the Base class, the foundation of all the shapes.

The Base class manages the identifier of every object and offers helpers
to convert objects to JSON text, to save them in files and to rebuild them.
"""
import json


class Base:
    """Base class that manages the id attribute of all its subclasses.

    A private class attribute counts the objects created without an explicit
    id, so that each of them receives a unique and increasing identifier.
    """

    __nb_objects = 0

    def __init__(self, id=None):
        """Set the id of the instance or generate the next available one."""
        if id is not None:
            self.id = id
        else:
            Base.__nb_objects += 1
            self.id = Base.__nb_objects

    @staticmethod
    def to_json_string(list_dictionaries):
        """Return the JSON string that represents a list of dictionaries."""
        if list_dictionaries is None or len(list_dictionaries) == 0:
            return "[]"
        return json.dumps(list_dictionaries)

    @classmethod
    def save_to_file(cls, list_objs):
        """Write the JSON string of a list of objects in a file.

        The file is named after the class and its content is overwritten.
        """
        if list_objs is None:
            list_objs = []
        list_dictionaries = [obj.to_dictionary() for obj in list_objs]
        with open(cls.__name__ + ".json", "w") as file:
            file.write(cls.to_json_string(list_dictionaries))

    @staticmethod
    def from_json_string(json_string):
        """Return the list represented by a JSON string."""
        if json_string is None or len(json_string) == 0:
            return []
        return json.loads(json_string)

    @classmethod
    def create(cls, **dictionary):
        """Return a new instance with all its attributes already set.

        A dummy instance is built first and then updated with the dictionary.
        """
        if cls.__name__ == "Square":
            dummy = cls(1)
        else:
            dummy = cls(1, 1)
        dummy.update(**dictionary)
        return dummy

    @classmethod
    def load_from_file(cls):
        """Return the list of instances stored in the file of the class.

        An empty list is returned when the file does not exist.
        """
        try:
            with open(cls.__name__ + ".json", "r") as file:
                json_string = file.read()
        except FileNotFoundError:
            return []
        list_dictionaries = cls.from_json_string(json_string)
        return [cls.create(**dictionary) for dictionary in list_dictionaries]
