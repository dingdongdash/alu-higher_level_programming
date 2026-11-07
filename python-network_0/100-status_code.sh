#!/bin/bash
# Displays only the HTTP status code of the response from the given URL
curl -s -o /dev/null -w "%{http_code}" "$1"
