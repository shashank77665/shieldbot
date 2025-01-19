from utils.http_client import make_request
from utils.response_parser import parse_response, format_log

def brute_force_test(base_url, options):
    passwords = options.get("passwords", ["admin", "password1", "12345"])
    logs = []

    for password in passwords:
        try:
            response = make_request(base_url, data={"user": "admin", "pass": password})
            parsed = parse_response(response)
            logs.append(format_log(f"Tested password '{password}'", parsed))
        except Exception as e:
            logs.append(format_log(f"Error testing password '{password}'", {"error": str(e)}))

    return {"logs": logs, "score": 7}
