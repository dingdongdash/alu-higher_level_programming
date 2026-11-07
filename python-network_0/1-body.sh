#!/bin/bash
# Follows redirects from the URL given as first argument and displays the final body only if the status code is 200
t=$(mktemp) && { [ "$(curl -s -L -o "$t" -w '%{http_code}' "$1")" = "200" ] && cat "$t"; rm -f "$t"; }
