#!/usr/bin/python3
def print_matrix_integer(matrix=[[]]):
    for row in matrix:
        for i, n in enumerate(row):
            if i:
                print(" ", end="")
            print("{:d}".format(n), end="")
        print()
