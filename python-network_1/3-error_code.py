#!/usr/bin/python3
"""Send a request to a URL and display the body or the HTTP error code."""
import sys
import urllib.error
import urllib.request

if __name__ == "__main__":
    try:
        with urllib.request.urlopen(sys.argv[1]) as response:
            print(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        print("Error code: {}".format(error.code))
