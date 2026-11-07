#!/usr/bin/python3
import sys


def solve(n, row, queens):
    if row == n:
        print([[r, c] for r, c in enumerate(queens)])
        return
    for col in range(n):
        if all(col != c and abs(col - c) != row - r
               for r, c in enumerate(queens)):
            queens.append(col)
            solve(n, row + 1, queens)
            queens.pop()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: nqueens N")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("N must be a number")
        sys.exit(1)
    if n < 4:
        print("N must be at least 4")
        sys.exit(1)
    solve(n, 0, [])
