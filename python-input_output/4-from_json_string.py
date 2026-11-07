#!/usr/bin/python3
"""Module that defines a function building an object out of JSON text."""
import json


def from_json_string(my_str):
    """Return the Python object that the given JSON string represents."""
    return json.loads(my_str)
