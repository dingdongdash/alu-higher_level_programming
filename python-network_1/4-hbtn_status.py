#!/usr/bin/python3
"""Fetch the status page of the ALU intranet using the requests package."""
import requests

if __name__ == "__main__":
    response = requests.get("https://alu-intranet.hbtn.io/status")
    print("Body response:")
    print("\t- type: {}".format(type(response.text)))
    print("\t- content: {}".format(response.text))
