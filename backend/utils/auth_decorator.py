from functools import wraps
from flask import request, jsonify
from backend.models import User
from backend.database import db
from backend.utils.jwt_utils import decode_and_verify_token  # Reuse the JWT decoding logic

def authorize(required_superuser=False):
    """
    Authorization decorator to check for valid JWT and optional superuser privileges.

    Args:
        required_superuser (bool): If True, only superusers can access the route.

    Usage:
        @app.route('/some-route')
        @authorize()
        def some_route():
            pass
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"error": "Token is missing"}), 401

            user, error = decode_and_verify_token(token)
            if error:
                return jsonify({"error": error}), 401

            if required_superuser and not user.is_superuser:
                return jsonify({"error": "Access denied. Superuser privileges required."}), 403

            # Pass the user object to the route
            request.current_user = user
            return f(*args, **kwargs)
        return wrapper
    return decorator
