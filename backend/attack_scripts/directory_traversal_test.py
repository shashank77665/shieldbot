import requests
from .utils import create_result

def directory_traversal_test(base_url, options=None):
    """
    Tests for directory traversal by sending common file path patterns 
    (e.g., ../../etc/passwd). Returns a standardized result dictionary.
    """
    if options is None:
        options = {}
    
    result_logs = []
    payloads = [
        "../../etc/passwd",
        "../../../boot.ini",
        "../windows/win.ini",
    ]
    
    endpoint = options.get("endpoint", "/download")
    param_name = options.get("param_name", "file")
    
    overall_success = True
    for payload in payloads:
        url = f"{base_url.rstrip('/')}{endpoint}?{param_name}={payload}"
        try:
            response = requests.get(url, timeout=10)
            result_logs.append(f"[DirTraversal Test] Sent payload '{payload}' to {url} (Status: {response.status_code})")
            if "root:x" in response.text or "[extensions]" in response.text:
                result_logs.append(f"Possible directory traversal vulnerability with payload '{payload}'.")
        except Exception as e:
            overall_success = False
            result_logs.append(f"Error while testing directory traversal '{payload}': {str(e)}")
    
    return create_result(
        logs=result_logs,
        score=0,
        success=overall_success
    )
