#!/bin/bash
# Sends a DELETE request to the URL given as first argument and displays the body of the response
curl -s -X DELETE "$1"
