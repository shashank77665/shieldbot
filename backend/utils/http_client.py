import requests

def make_request(url, data=None, method="POST", timeout=5):
    """Make an HTTP request with centralized error handling."""
    headers = {"User-Agent": "ShieldBot/1.0"}
    try:
        if method == "POST":
            response = requests.post(url, data=data, headers=headers, timeout=timeout)
        elif method == "GET":
            response = requests.get(url, headers=headers, timeout=timeout)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx/5xx)
        return response

    except (requests.RequestException, Exception) as e:
        # Catch both requests exceptions and any other unexpected exception
        raise RuntimeError(f"HTTP request failed: {e}")
