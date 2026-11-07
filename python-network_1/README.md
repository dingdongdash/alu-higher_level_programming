# python-network_1

Python - Network #1: scripts that use `urllib` and `requests` to send HTTP requests and handle responses.

| File | Description |
| --- | --- |
| `0-hbtn_status.py` | Fetches `https://alu-intranet.hbtn.io/status` with `urllib` and displays the body, its type and its utf-8 content. |
| `1-hbtn_header.py` | Sends a request to a URL with `urllib` and displays the `X-Request-Id` response header. |
| `2-post_email.py` | Sends a POST request with an email to a URL with `urllib` and displays the response body. |
| `3-error_code.py` | Sends a request with `urllib`, displaying the body or `Error code: <status>` on an `HTTPError`. |
| `4-hbtn_status.py` | Fetches `https://alu-intranet.hbtn.io/status` with `requests` and displays the body and its type. |
| `5-hbtn_header.py` | Sends a request to a URL with `requests` and displays the `X-Request-Id` response header. |
| `6-post_email.py` | Sends a POST request with an email to a URL with `requests` and displays the response body. |
| `7-error_code.py` | Sends a request with `requests`, displaying the body or `Error code: <status>` when the status is 400 or more. |
| `8-json_api.py` | Posts a letter as `q` to `http://0.0.0.0:5000/search_user` and displays `[<id>] <name>`, `Not a valid JSON` or `No result`. |
| `10-my_github.py` | Uses the GitHub API with basic authentication (username and personal access token) to display the user id. |

All Python scripts are interpreted on Ubuntu 14.04 LTS with python3 (3.4.3), follow the pycodestyle (version 1.7) style and are executable.
