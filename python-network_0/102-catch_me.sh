#!/bin/bash
# Makes a PUT request to catch_me with the right header and body to get the You got me message
curl -s -L -X PUT -H "Origin: HolbertonSchool" -d "user_id=98" 0.0.0.0:5000/catch_me
