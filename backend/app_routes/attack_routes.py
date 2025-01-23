from flask import Blueprint, request, jsonify
from backend.tasks import run_attacks
from celery.result import AsyncResult
from backend.models import RequestLog, User
from backend.database import db
import jwt
from dotenv import load_dotenv
import os
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# Blueprint for attack routes
attack_bp = Blueprint("attack", __name__, url_prefix="/attack")
load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")

def verify_token(token):
    """Utility to verify JWT token."""
    try:
        # Decode the JWT token
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # Retrieve user based on decoded user_id
        user = db.session.get(User, decoded["user_id"])
        if not user:
            return None, "Invalid user"
        return user, None
    except ExpiredSignatureError:
        return None, "Token has expired"
    except InvalidTokenError:
        return None, "Invalid token"

@attack_bp.route('/perform-test', methods=['POST'])
def perform_test():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 400

    user, error = verify_token(token)
    if not user:
        return jsonify({"error": error}), 401

    data = request.json
    base_url = data.get("base_url")
    attack_selection = data.get("attack_selection", {})

    if not base_url:
        return jsonify({"error": "Base URL is required"}), 400

    if attack_selection.get("brute_force", False) and not data.get("username"):
        return jsonify({"error": "Username is required for brute force attack"}), 400

    task = run_attacks.delay(base_url, {
        "brute_force": {"enabled": attack_selection.get("brute_force", False), "username": data.get("username")},
        "sql_injection": {"enabled": attack_selection.get("sql_injection", False)},
        "dos": {"enabled": attack_selection.get("dos_attack", False)},
    })

    log = RequestLog(user_id=user.id, base_url=base_url, test_type="dynamic", options=attack_selection, status="Pending")
    db.session.add(log)
    db.session.commit()

    return jsonify({"task_id": task.id, "message": "Attack task submitted successfully"}), 202

@attack_bp.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 400

    user, error = verify_token(token)
    if not user:
        return jsonify({"error": error}), 401

    task = AsyncResult(task_id)
    if task.state == 'PENDING':
        return jsonify({"status": "Pending"}), 202
    elif task.state == 'SUCCESS':
        return jsonify({"status": "Completed", "result": task.result}), 200
    elif task.state == 'FAILURE':
        return jsonify({"status": "Failed", "error": str(task.info)}), 500
    else:
        return jsonify({"status": task.state}), 200
