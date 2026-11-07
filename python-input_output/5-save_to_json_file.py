#!/usr/bin/python3
"""Module that defines a function saving an object to a JSON file."""
import json


def save_to_json_file(my_obj, filename):
    """Write an object to a UTF8 text file using its JSON representation."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(my_obj, f)
