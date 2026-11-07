#!/bin/bash
# Sends a GET request with the header X-HolbertonSchool-User-Id: 98 to the URL given as first argument and displays the body
curl -s -H 'X-HolbertonSchool-User-Id: 98' "$1"
