#!/usr/bin/python3
"""Send a request to a URL and display the body or the HTTP error code."""
import requests
import sys

if __name__ == "__main__":
    response = requests.get(sys.argv[1])
    if response.status_code >= 400:
        print("Error code: {}".format(response.status_code))
    else:
        print(response.text)
