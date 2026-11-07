#!/usr/bin/python3
"""Send a POST request with an email to a URL and display the response body."""
import sys
import urllib.parse
import urllib.request

if __name__ == "__main__":
    data = urllib.parse.urlencode({"email": sys.argv[2]}).encode("utf-8")
    request = urllib.request.Request(sys.argv[1], data)
    with urllib.request.urlopen(request) as response:
        print(response.read().decode("utf-8"))
