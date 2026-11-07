#!/usr/bin/python3
"""Module for the matrix_divided function.

This module defines a function that divides a matrix by a number.
Every element of the matrix is divided and rounded to two decimals.
A new matrix is returned and the original matrix is left unchanged.
"""


def matrix_divided(matrix, div):
    """Divide all elements of a matrix and return a new matrix.

    The matrix must be a list of lists of integers or floats and all
    rows must have the same size. The divisor must be a non zero number.
    """
    message = "matrix must be a matrix (list of lists) of integers/floats"
    if not isinstance(matrix, list):
        raise TypeError(message)
    for row in matrix:
        if not isinstance(row, list):
            raise TypeError(message)
        for element in row:
            if not isinstance(element, (int, float)):
                raise TypeError(message)
    for row in matrix:
        if len(row) != len(matrix[0]):
            raise TypeError("Each row of the matrix must have the same size")
    if not isinstance(div, (int, float)):
        raise TypeError("div must be a number")
    if div == 0:
        raise ZeroDivisionError("division by zero")
    return [[round(element / div, 2) for element in row] for row in matrix]
