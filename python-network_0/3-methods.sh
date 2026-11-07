#!/bin/bash
# Sends an OPTIONS request to the URL given as first argument and displays the methods listed in the Allow header
curl -s -I -X OPTIONS "$1" | tr -d '\r' | sed -n 's/^[Aa][Ll][Ll][Oo][Ww]:[[:space:]]*\(.*[^[:space:]]\)[[:space:]]*$/\1/p' | head -n 1
