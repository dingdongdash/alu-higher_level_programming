#!/usr/bin/python3
"""Send a letter to a search API and display the id and name of the result."""
import requests
import sys

if __name__ == "__main__":
    url = "http://0.0.0.0:5000/search_user"
    letter = sys.argv[1] if len(sys.argv) > 1 else ""
    response = requests.post(url, data={"q": letter})
    try:
        result = response.json()
    except ValueError:
        print("Not a valid JSON")
    else:
        if result:
            print("[{}] {}".format(result.get("id"), result.get("name")))
        else:
            print("No result")
