from utils.http_client import make_request
from utils.response_parser import format_log

def dos_attack_test(base_url, options):
    request_count = options.get("request_count", 10)
    logs = []

    for i in range(request_count):
        try:
            response = make_request(base_url)
            logs.append(format_log(f"Sent DoS request {i+1}", {"status_code": response.status_code}))
        except Exception as e:
            logs.append(format_log(f"Error during DoS request {i+1}", {"error": str(e)}))

    return {"logs": logs, "score": 8}
