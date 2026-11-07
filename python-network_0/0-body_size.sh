#!/bin/bash
# Sends a request to the URL given as first argument and displays the size in bytes of the response body
curl -s "$1" | wc -c
