# python-almost_a_circle

Python - Almost a circle project: a small geometry package built around a `Base` class that manages identifiers and JSON serialization, a `Rectangle` class and a `Square` class, all covered by unit tests.

## Requirements

- Ubuntu 20.04 LTS, python3 (version 3.8.5)
- Code style checked with pycodestyle (version 2.7.*)
- All files end with a new line, python files start with `#!/usr/bin/python3` and are executable
- Every module, class and function has a documentation string
- Unit tests use the `unittest` module and live in the `tests` folder

## Files

| File | Description |
| --- | --- |
| `models/__init__.py` | Makes `models` a package |
| `models/base.py` | `Base` class: id management, JSON string helpers, `save_to_file`, `create` and `load_from_file` |
| `models/rectangle.py` | `Rectangle` class: validated width, height, x and y, `area`, `display`, `update` and `to_dictionary` |
| `models/square.py` | `Square` class: a `Rectangle` with a single `size` |
| `tests/__init__.py` | Makes `tests` a package |
| `tests/test_models/__init__.py` | Makes `tests/test_models` a package |
| `tests/test_models/test_base.py` | Unit tests of the `Base` class |
| `tests/test_models/test_rectangle.py` | Unit tests of the `Rectangle` class |
| `tests/test_models/test_square.py` | Unit tests of the `Square` class |

## Usage

```python
from models.rectangle import Rectangle
from models.square import Square

r = Rectangle(10, 2, 1, 9)
print(r)                       # [Rectangle] (1) 1/9 - 10/2
Rectangle.save_to_file([r])    # writes Rectangle.json
print(Rectangle.load_from_file()[0])

s = Square(5, 1, 2)
print(s)                       # [Square] (2) 1/2 - 5
```

## Tests

Run all the tests from this directory:

```
python3 -m unittest discover tests
```

Run the tests of one file:

```
python3 -m unittest tests/test_models/test_base.py
```
