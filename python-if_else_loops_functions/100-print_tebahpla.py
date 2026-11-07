#!/usr/bin/python3
for i in range(25, -1, -1):
    print("{}".format(chr(97 + i - 32 * ((25 - i) % 2))), end="")
