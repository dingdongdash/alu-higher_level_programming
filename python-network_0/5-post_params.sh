#!/bin/bash
# Sends a POST request with the variables email and subject to the URL given as first argument and displays the body
curl -s -X POST --data-urlencode 'email=test@gmail.com' --data-urlencode 'subject=I will always be here for PLD' "$1"
