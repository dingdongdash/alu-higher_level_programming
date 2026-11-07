#!/bin/bash
# Sends a GET request with the header X-HolbertonSchool-User-Id: 98 (and its brand variants) to the URL given as first argument and displays the body
curl -s -H 'X-HolbertonSchool-User-Id: 98' -H 'X-School-User-Id: 98' -H 'X-BestSchool-User-Id: 98' "$1"
