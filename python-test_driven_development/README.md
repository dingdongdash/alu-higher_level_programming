# python-test_driven_development

Python - Test-driven development project: functions written together with their doctests, and unittests for an existing function.

## Requirements

- Ubuntu 20.04 LTS, python3 (version 3.8.5)
- Code style checked with pycodestyle (version 2.7.*)
- All files end with a new line, python files start with `#!/usr/bin/python3` and are executable
- Every module and function has a documentation string
- No module is imported by the implementation files
- Doctests are text files in the `tests` folder, run from this directory with `python3 -m doctest ./tests/*`
- Unittests are run from this directory with `python3 -m unittest tests.6-max_integer_test`

## Files

| File | Description |
| --- | --- |
| `0-add_integer.py` | Function that adds 2 integers |
| `2-matrix_divided.py` | Function that divides all elements of a matrix |
| `3-say_my_name.py` | Function that prints a first name and a last name |
| `4-print_square.py` | Function that prints a square with the character `#` |
| `5-text_indentation.py` | Function that prints a text with 2 new lines after `.`, `?` and `:` |
| `6-max_integer.py` | Function that finds the max integer in a list |
| `tests/0-add_integer.txt` | Doctests for `0-add_integer.py` |
| `tests/2-matrix_divided.txt` | Doctests for `2-matrix_divided.py` |
| `tests/3-say_my_name.txt` | Doctests for `3-say_my_name.py` |
| `tests/4-print_square.txt` | Doctests for `4-print_square.py` |
| `tests/5-text_indentation.txt` | Doctests for `5-text_indentation.py` |
| `tests/6-max_integer_test.py` | Unittests for `6-max_integer.py` |
