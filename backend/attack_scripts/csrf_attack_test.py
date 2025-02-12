import requests
from .utils import create_result

def csrf_attack_test(base_url, options=None):
    """
    Demonstrates a CSRF test.
    
    Args:
        base_url (str): Target URL.
        options (dict, optional): May include "endpoint" and "data" parameters.
    
    Returns:
        dict: Standardized result dictionary.
    """
    if options is None:
        options = {}
    
    result_logs = []
    endpoint = options.get("endpoint", "/transfer")
    data_params = options.get("data", {"amount": "1000"})
    url = f"{base_url.rstrip('/')}{endpoint}"
    
    try:
        response = requests.post(url, data=data_params, timeout=10)
        result_logs.append(f"[CSRF Test] POST to {url} without token (Status: {response.status_code})")
        if "Transfer completed" in response.text:
            result_logs.append("Possible CSRF vulnerability: request succeeded without token.")
            return create_result(
                logs=result_logs,
                score=7,
                success=True
            )
        else:
            return create_result(
                logs=result_logs,
                score=5,
                success=False
            )
    except Exception as e:
        result_logs.append(f"Error while testing CSRF: {str(e)}")
        return create_result(
            logs=result_logs,
            score=0,
            success=False,
            error=str(e)
        )
