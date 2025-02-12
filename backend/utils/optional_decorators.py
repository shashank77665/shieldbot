from functools import wraps
from flask import request, jsonify

def google_oauth_required(f):
    """
    Dummy decorator for Google OAuth.
    Replace the logic here when you want to enable Google OAuth.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Currently disabled: simply pass through.
        return f(*args, **kwargs)
    return decorated_function

def captcha_required(f):
    """
    Dummy decorator for CAPTCHA verification.
    Replace the logic here to verify a CAPTCHA token or challenge.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Currently disabled: simply pass through.
        return f(*args, **kwargs)
    return decorated_function

def email_utils_required(f):
    """
    Dummy decorator for email utilities.
    This could be used to send notifications or verify email-based actions.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Currently disabled: simply pass through.
        return f(*args, **kwargs)
    return decorated_function 