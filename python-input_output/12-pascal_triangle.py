#!/usr/bin/python3
"""Module that defines a function building the Pascal's triangle."""


def pascal_triangle(n):
    """Return a list of lists of integers representing the Pascal's triangle.

    The triangle has n rows and an empty list is returned when n is not
    greater than zero.
    """
    if n <= 0:
        return []
    triangle = [[1]]
    for _ in range(n - 1):
        last = triangle[-1]
        middle = [last[i] + last[i + 1] for i in range(len(last) - 1)]
        triangle.append([1] + middle + [1])
    return triangle
