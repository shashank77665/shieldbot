import os
from flask import Blueprint, request, jsonify
from backend.models import User
from backend.database import db
from backend.utils.hash_utils import hash_password, verify_password
from backend.utils.jwt_utils import create_jwt, decode_and_verify_token
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError

import jwt
load_dotenv()
auth_bp = Blueprint("auth_v1", __name__, url_prefix="/auth")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    data = User.validate_fields(data)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validate input
    missing_fields = [field for field in ["username", "email", "password"] if not data.get(field)]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Check if user exists
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User already exists"}), 400

    # Register new user
    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        profile_picture="user.jpg",
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "profile_picture": user.profile_picture}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email", "")[:120]
    password = data.get("password")

    # Validate input fields
    missing_fields = [field for field in ["email", "password"] if not data.get(field)]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_jwt(user.id)

    return jsonify({"message": f"Welcome, {user.username}!", "token": token}), 200



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
    user, error = decode_and_verify_token(token)
    if error:
        return jsonify({"error": error}), 401

    return jsonify({"message": "Token is valid", "user_id": user.id}), 200


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
        new_token = create_jwt(payload["user_id"])

        # Ensure the token is a string before returning
        if isinstance(new_token, bytes):
            new_token = new_token.decode("utf-8")

        return jsonify({"token": new_token}), 200
    except InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
