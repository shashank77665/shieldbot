from utils.http_client import make_request
from utils.response_parser import parse_response, format_log

def sql_injection_test(base_url, options):
    payloads = options.get("payloads", ["' OR '1'='1", "' UNION SELECT NULL--"])
    logs = []

    for payload in payloads:
        try:
            response = make_request(base_url, data={"input": payload})
            parsed = parse_response(response)
            logs.append(format_log(f"Tested SQL payload '{payload}'", parsed))
        except Exception as e:
            logs.append(format_log(f"Error testing payload '{payload}'", {"error": str(e)}))

    return {"logs": logs, "score": 5}
