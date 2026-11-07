# python-network_0

Python - Network #0 project: using `curl` from Bash scripts to send HTTP requests and inspect responses.

## Requirements

- Ubuntu 20.04 LTS
- All Bash scripts are exactly 3 lines long: the `#!/bin/bash` shebang, a comment, and the command
- All files end with a new line and are executable
- All `curl` commands use the `-s` option (silent mode)

## Files

| File | Description |
| --- | --- |
| `0-body_size.sh` | Script that takes a URL, sends a request to it, and displays the size of the response body in bytes |
| `1-body.sh` | Script that takes a URL, sends a GET request to it, and displays the body only for a 200 status code response |
| `2-delete.sh` | Script that sends a DELETE request to the URL passed as first argument and displays the body of the response |
| `3-methods.sh` | Script that takes a URL and displays all HTTP methods the server will accept |
| `4-header.sh` | Script that sends a GET request with the header `X-HolbertonSchool-User-Id: 98` and displays the body of the response |
| `5-post_params.sh` | Script that sends a POST request with the variables `email` and `subject` and displays the body of the response |
