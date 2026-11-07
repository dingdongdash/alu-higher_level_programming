#!/bin/bash
# Sends a GET request to the URL given as first argument and displays the body only if the status code is 200
t=$(mktemp) && { [ "$(curl -s -o "$t" -w '%{http_code}' "$1")" = "200" ] && cat "$t"; rm -f "$t"; }
