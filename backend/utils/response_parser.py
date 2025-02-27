from datetime import timezone, datetime

def parse_response(response):
    """
    Parse the HTTP response and extract relevant details.
    
    Args:
        response (requests.Response): The HTTP response object.
    
    Returns:
        dict: Parsed response details (status code, headers, content snippet).
    """
    try:
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content_snippet": response.text[:200],  # Extract first 200 characters
        }
    except AttributeError as e:
        raise ValueError(f"Invalid response object: {e}")
def format_log(message, details=None):
    """
    Format log entries with a timestamp and optional details.

    Args:
        message (str): The log message.
        details (dict, optional): Additional context or metadata for the log.

    Returns:
        dict: A formatted log entry with a timestamp.
    """
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),  # ISO format for better compatibility
        "message": message,
    }
    if details:
        log_entry["details"] = details
    return log_entry
