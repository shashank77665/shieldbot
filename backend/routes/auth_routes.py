import os
from flask import Blueprint, request, jsonify
from backend.models import ShieldbotUser  # Use ShieldbotUser
from backend.database import db
from backend.utils.hash_utils import hash_password, verify_password
from backend.utils.jwt_utils import create_jwt, decode_and_verify_token
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
import jwt

# Load environment variables
load_dotenv()

auth_bp = Blueprint("auth_v1", __name__, url_prefix="/auth")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
RESET_TOKEN_EXPIRATION = 3600  # 1 hour expiration for reset tokens

def create_reset_token(user_id):
    payload = {
        "shieldbot_user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=RESET_TOKEN_EXPIRATION)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    """
    Route to register a new user.
    """
    data = request.json
    data = ShieldbotUser.validate_fields(data)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validate input
    missing_fields = [field for field in ["username", "email", "password"] if not data.get(field)]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Check if user exists
    if ShieldbotUser.query.filter(
        (ShieldbotUser.username == username) | (ShieldbotUser.email == email)
    ).first():
        return jsonify({"error": "User already exists"}), 400

    # Register new user
    shieldbot_user = ShieldbotUser(
        username=username,
        email=email,
        password_hash=hash_password(password),
        profile_picture="user.jpg",
    )
    db.session.add(shieldbot_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "profile_picture": shieldbot_user.profile_picture}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Route to log in a user.
    """
    data = request.json
    email = data.get("email", "")[:120]
    password = data.get("password")

    # Validate input fields
    missing_fields = [field for field in ["email", "password"] if not data.get(field)]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Find user and verify credentials
    shieldbot_user = ShieldbotUser.query.filter_by(email=email).first()
    if not shieldbot_user or not verify_password(shieldbot_user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_jwt(shieldbot_user.shieldbot_user_id)  # Updated to use shieldbot_user_id

    return jsonify({"message": f"Welcome, {shieldbot_user.username}!", "token": token}), 200


@auth_bp.route("/request-password-reset", methods=["POST"])
def request_password_reset():
    """
    Request a password reset token. In production, this should send an email with a link.
    For demonstration, we return the token directly.
    """
    data = request.json
    email = data.get("email")
    
    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = ShieldbotUser.query.filter_by(email=email).first()
    # Do not reveal whether the email exists for security reasons.
    if user:
        reset_token = create_reset_token(user.shieldbot_user_id)
        # In production, an email would be sent containing the reset link.
        return jsonify({"message": "Password reset token generated. (In production, an email would be sent.)", "reset_token": reset_token}), 200
    else:
        return jsonify({"message": "If the email exists, a reset token will be sent."}), 200


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
    Route to verify the JWT token.
    Expects the Authorization header to contain the token.
    """
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 400

    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]

    # Verify the token
    shieldbot_user, error = decode_and_verify_token(token)
    if error:
        return jsonify({"error": error}), 401

    return jsonify({"message": "Token is valid", "user_id": shieldbot_user.shieldbot_user_id}), 200


@auth_bp.route("/refresh-token", methods=["POST"])
def refresh_token():
    """
    Route to refresh the JWT token if it has expired.
    """
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 400

    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]

    try:
        # Decode without verifying expiry
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
        new_token = create_jwt(payload["shieldbot_user_id"])  # Updated to use shieldbot_user_id

        return jsonify({"token": new_token}), 200
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
