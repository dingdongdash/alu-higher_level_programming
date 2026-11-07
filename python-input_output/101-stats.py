#!/usr/bin/python3
"""Script that reads log lines on stdin and prints metrics about them."""
import sys


def print_stats(size, codes):
    """Print the total file size and the number of lines per status code."""
    print("File size: {}".format(size))
    for code in sorted(codes):
        print("{}: {}".format(code, codes[code]))
    sys.stdout.flush()


size = 0
count = 0
codes = {}
allowed = ("200", "301", "400", "401", "403", "404", "405", "500")

try:
    for line in sys.stdin:
        fields = line.split()
        count += 1
        try:
            size += int(fields[-1])
        except (IndexError, ValueError):
            pass
        try:
            if fields[-2] in allowed:
                codes[fields[-2]] = codes.get(fields[-2], 0) + 1
        except IndexError:
            pass
        if count % 10 == 0:
            print_stats(size, codes)
    print_stats(size, codes)
except KeyboardInterrupt:
    print_stats(size, codes)
    raise
