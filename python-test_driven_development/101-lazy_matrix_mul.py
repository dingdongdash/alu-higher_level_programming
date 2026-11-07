#!/usr/bin/python3
"""Module for lazy matrix multiplication.

This module defines a function that multiplies two matrices.
The product is computed by the NumPy module instead of by hand.
Invalid matrices raise the exceptions that NumPy itself raises.
"""
import numpy


def lazy_matrix_mul(m_a, m_b):
    """Multiply two matrices with NumPy and return their product.

    Both arguments are lists of lists of integers or floats.
    The product is a NumPy array computed by the matmul function.
    The inputs are unchanged and NumPy raises the errors.
    """
    return numpy.matmul(m_a, m_b)
