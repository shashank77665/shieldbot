from backend.utils.http_client import make_request
from backend.utils.response_parser import format_log
from .utils import create_result

def dos_attack_test(base_url, options):
    """
    Simulate a DoS attack by sending multiple requests.
    
    Args:
        base_url (str): Target URL.
        options (dict): Should include "request_count".
    
    Returns:
        dict: Standardized result dictionary.
    """
    request_count = options.get("request_count", 10)
    result_logs = []
    for i in range(request_count):
        try:
            response = make_request(base_url)
            result_logs.append(format_log(f"Sent DoS request {i+1}", {"status_code": response.status_code}))
        except Exception as e:
            result_logs.append(format_log(f"Error during DoS request {i+1}", {"error": str(e)}))
    return create_result(
        logs=result_logs,
        score=8,
        success=True if request_count > 0 else False
    )
