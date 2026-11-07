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
allowed = (200, 301, 400, 401, 403, 404, 405, 500)

try:
    for line in sys.stdin:
        fields = line.split()
        try:
            status = int(fields[-2])
            size += int(fields[-1])
        except (IndexError, ValueError):
            continue
        if status in allowed:
            codes[status] = codes.get(status, 0) + 1
        count += 1
        if count % 10 == 0:
            print_stats(size, codes)
except KeyboardInterrupt:
    print_stats(size, codes)
    raise
