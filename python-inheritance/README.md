# python-inheritance

Python - Inheritance project: classes, subclasses, class and instance checks, validation and shapes built on a geometry base class.

## Requirements

- Ubuntu 20.04 LTS, python3 (version 3.8.5)
- Code style checked with pycodestyle (version 2.7.*)
- All files end with a new line, python files start with `#!/usr/bin/python3` and are executable
- Every module, class and function has a documentation string
- Tests are text files in the `tests` folder, run from this directory with `python3 -m doctest ./tests/*`

## Files

| File | Description |
| --- | --- |
| `0-lookup.py` | Function that returns the list of attributes and methods of an object |
| `1-my_list.py` | `MyList`, a subclass of `list` with a `print_sorted` method |
| `2-is_same_class.py` | Function that checks if an object is exactly an instance of a class |
| `3-is_kind_of_class.py` | Function that checks if an object is an instance of a class or of a subclass |
| `4-inherits_from.py` | Function that checks if an object is an instance of a strict subclass of a class |
| `5-base_geometry.py` | Empty `BaseGeometry` class |
| `6-base_geometry.py` | `BaseGeometry` with an `area` method that is not implemented |
| `7-base_geometry.py` | `BaseGeometry` with an `integer_validator` method |
| `8-rectangle.py` | `Rectangle` subclass with a private width and a private height |
| `9-rectangle.py` | `Rectangle` with an `area` method and a text description |
| `10-square.py` | `Square` subclass of `Rectangle` with a private size |
| `11-square.py` | `Square` with its own text description |
| `tests/1-my_list.txt` | Doctests for `1-my_list.py` |
| `tests/7-base_geometry.txt` | Doctests for `7-base_geometry.py` |
