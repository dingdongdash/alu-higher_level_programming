#!/usr/bin/python3
"""Module that defines a function returning the JSON text of an object."""
import json


def to_json_string(my_obj):
    """Return the JSON representation, as a string, of the given object."""
    return json.dumps(my_obj)
