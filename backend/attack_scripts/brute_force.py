import requests
from .utils import create_result

def brute_force_test(base_url, options):
    """
    Perform a brute force attack on the given URL using the specified options.
    
    Args:
        base_url (str): Target URL.
        options (dict): Should include "username", "password_list", optional "login_endpoint", and "timeout".
    
    Returns:
        dict: Standardized result dictionary.
    """
    username = options.get("username")
    password_list = options.get("password_list", [])
    login_endpoint = options.get("login_endpoint", "/login")
    timeout = options.get("timeout", 5)

    if not username or not password_list:
        return create_result(
            logs=["Username and password list are required"],
            score=0,
            success=False,
            error="Missing username or password list"
        )

    url = f"{base_url.rstrip('/')}{login_endpoint}"
    result_logs = []
    found = False
    found_details = None
    attempted = 0

    for password in password_list:
        try:
            response = requests.post(
                url,
                json={"username": username, "password": password},
                timeout=timeout
            )
            attempted += 1
            result_logs.append(f"Attempt {attempted}: Tried password '{password}'")
            if response.status_code == 200 and "Login successful" in response.text:
                found = True
                found_details = {
                    "username": username,
                    "password": password,
                    "response": response.text
                }
                result_logs.append("Login successful!")
                break

        except requests.RequestException as e:
            result_logs.append(f"Request error: {str(e)}")
            return create_result(
                logs=result_logs,
                score=0,
                success=False,
                error=str(e)
            )
        except Exception as e:
            result_logs.append(f"Unexpected error: {str(e)}")
            return create_result(
                logs=result_logs,
                score=0,
                success=False,
                error=str(e)
            )

    if found:
        return create_result(
            logs=result_logs + [f"Successful login: {found_details}"],
            score=10,
            success=True
        )
    else:
        return create_result(
            logs=result_logs + ["Brute force attack failed. No valid credentials found."],
            score=5,
            success=False
        )
