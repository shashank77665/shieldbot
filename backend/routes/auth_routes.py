# backend/routes/auth_routes.py
import os
from flask import Blueprint, request, jsonify, session, current_app, redirect, url_for
from backend.models import ShieldbotUser
from backend.database import db
from backend.utils.hash_utils import hash_password, verify_password
from backend.utils.jwt_utils import create_jwt, decode_and_verify_token
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, UTC
import jwt
from backend.utils.optional_decorators import google_oauth_required, captcha_required

# Load environment variables
load_dotenv()

auth_bp = Blueprint("auth_v1", __name__, url_prefix="/auth")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
RESET_TOKEN_EXPIRATION = 3600  # 1 hour expiration for reset tokens

def create_reset_token(user_id):
    payload = {
        "shieldbot_user_id": user_id,
        "exp": datetime.now(UTC) + timedelta(seconds=RESET_TOKEN_EXPIRATION)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    """
    Register a new user and automatically log them in.
    If a user is already logged in (active session), redirect to dashboard.
    """
    # Check if a user is already logged in
    if session.get("user_id"):
        return jsonify({"message": "Already logged in", "redirect_url": "/dashboard"}), 200

    data = request.json
    data = ShieldbotUser.validate_fields(data)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validate input
    missing_fields = [field for field in ["username", "email", "password"] if not data.get(field)]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Check if the user already exists
    if ShieldbotUser.query.filter(
        (ShieldbotUser.username == username) | (ShieldbotUser.email == email)
    ).first():
        return jsonify({"error": "User already exists"}), 400

    # Register new user
    shieldbot_user = ShieldbotUser(
        username=username,
        email=email,
        password_hash=hash_password(password),
        profile_picture="user.jpg"
    )
    db.session.add(shieldbot_user)
    db.session.commit()

    # Automatically log in the new user by creating a JWT token and setting session variables.
    token = create_jwt(shieldbot_user.id)
    session["user_id"] = shieldbot_user.id
    session["token"] = token
    session.permanent = True

    # After setting the session, the session cookie is set in the response.
    # You can include the cookie value in the JSON response if desired:
    session_cookie = request.cookies.get(current_app.session_cookie_name)

    return jsonify({
        "message": "User registered and logged in successfully",
        "profile_picture": shieldbot_user.profile_picture,
        "token": token,
        "user": {
            "id": shieldbot_user.id,
            "email": shieldbot_user.email,
            "username": shieldbot_user.username
        },
        "session_id": session_cookie
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Log in an existing user.
    If the user is already logged in (active session), redirect to dashboard.
    """
    # If there is already an active session, do not require a new login.
    if session.get("user_id"):
        return jsonify({"message": "Already logged in", "redirect_url": "/dashboard"}), 200

    # Clear any existing session first (defensive measure)
    session.clear()

    data = request.json
    email = data.get("email", "")[:120]
    password = data.get("password")

    missing_fields = [field for field in ["email", "password"] if not data.get(field)]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Verify user exists and password is correct
    user = ShieldbotUser.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create JWT token
    token = create_jwt(user.id)
    session["user_id"] = user.id
    session["token"] = token
    session.permanent = True

    return jsonify({
        "message": "Logged in successfully",
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    }), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    Log out the user by clearing the session.
    """
    if "user_id" not in session:
        return jsonify({"error": "No active session"}), 400
        
    # Clear the entire session
    session.clear()
    
    # Optionally, you can explicitly expire the session cookie by setting its expiry in the response.
    response = jsonify({
        "message": "Logged out successfully"
    })
    response.delete_cookie(current_app.session_cookie_name)
    return response, 200

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    """
    Reset user password using a valid reset token.
    Expects JSON with: reset_token, new_password.
    """
    data = request.json
    reset_token = data.get("reset_token")
    new_password = data.get("new_password")
    
    if not reset_token or not new_password:
        return jsonify({"error": "reset_token and new_password are required"}), 400

    try:
        payload = jwt.decode(reset_token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("shieldbot_user_id")
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Reset token has expired."}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid reset token."}), 400

    user = ShieldbotUser.query.get(user_id)
    if not user:
        return jsonify({"error": "User does not exist."}), 404

    user.password_hash = hash_password(new_password)
    db.session.commit()
    return jsonify({"message": "Password reset successfully"}), 200

@auth_bp.route("/verify-token", methods=["GET"])
def verify_token_route():
    """
    Verify the current session's JWT token.
    This endpoint checks the session for a stored token rather than relying on the Authorization header.
    """
    # Retrieve the token from the session object.
    token = session.get("token")
    if not token:
        return jsonify({"error": "No active session. Please log in."}), 401

    shieldbot_user, error = decode_and_verify_token(token)
    if error:
        return jsonify({"error": error}), 401

    return jsonify({
        "message": "Token is valid",
        "user_id": shieldbot_user.id,
        "username": shieldbot_user.username
    }), 200

@auth_bp.route("/refresh-token", methods=["POST"])
def refresh_token():
    """
    Refresh the JWT token by decoding the existing token and issuing a new one.
    """
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 400

    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
        # Use the consistent payload key "user_id"
        new_token = create_jwt(payload["user_id"])
        session["token"] = new_token
        return jsonify({"token": new_token}), 200
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401