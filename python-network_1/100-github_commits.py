#!/usr/bin/python3
"""Print the sha and author name of the ten latest commits of a repository."""
import requests
import sys

if __name__ == "__main__":
    url = "https://api.github.com/repos/{}/{}/commits".format(
        sys.argv[2], sys.argv[1])
    response = requests.get(url, params={"per_page": 10})
    for item in response.json()[:10]:
        print("{}: {}".format(
            item.get("sha"), item.get("commit").get("author").get("name")))
