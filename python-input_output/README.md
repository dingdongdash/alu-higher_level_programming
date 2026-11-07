# python-input_output

Python - Input/Output project: reading and writing text files, JSON serialization, saving and reloading objects, and a Pascal's triangle exercise.

## Requirements

- Ubuntu 20.04 LTS, python3 (version 3.8.5)
- Code style checked with pycodestyle (version 2.7.*)
- All files end with a new line, python files start with `#!/usr/bin/python3` and are executable
- Every module, class and function has a documentation string

## Files

| File | Description |
| --- | --- |
| `0-read_file.py` | Function that reads a text file (UTF8) and prints it to stdout |
| `1-write_file.py` | Function that writes a string to a text file (UTF8) and returns the number of characters written |
| `2-append_write.py` | Function that appends a string at the end of a text file (UTF8) and returns the number of characters added |
| `3-to_json_string.py` | Function that returns the JSON representation of an object (string) |
| `4-from_json_string.py` | Function that returns an object represented by a JSON string |
| `5-save_to_json_file.py` | Function that writes an object to a text file using its JSON representation |
| `6-load_from_json_file.py` | Function that creates an object from a JSON file |
| `7-add_item.py` | Script that adds all arguments to a Python list and saves them to a file named `add_item.json` |
| `8-class_to_json.py` | Function that returns the dictionary description of an object for JSON serialization |
| `9-student.py` | Class `Student` with a `to_json` method returning its dictionary representation |
| `10-student.py` | Class `Student` whose `to_json` method can filter the retrieved attributes |
| `11-student.py` | Class `Student` with a `reload_from_json` method replacing its attributes |
| `12-pascal_triangle.py` | Function that returns the Pascal's triangle of n as a list of lists of integers |
