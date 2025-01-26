from flask import Blueprint, request, jsonify
from backend.tasks import run_attacks
from celery.result import AsyncResult
from backend.models import RequestLog, ShieldbotUser
from backend.database import db
import jwt
from dotenv import load_dotenv
import os
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

load_dotenv()

# Blueprint for attack routes
attack_bp = Blueprint("attack", __name__, url_prefix="/attack")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")


def verify_token(token):
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]  # Remove "Bearer" prefix
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        shieldbot_user = db.session.get(ShieldbotUser, decoded["shieldbot_user_id"])
        if not shieldbot_user:
            return None, "Invalid user"
        return shieldbot_user, None
    except ExpiredSignatureError:
        return None, "Token has expired"
    except InvalidTokenError:
        return None, "Invalid token"


@attack_bp.route('/perform-test', methods=['POST'])
def perform_test():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 400

    shieldbot_user, error = verify_token(token)
    if not shieldbot_user:
        return jsonify({"error": error}), 401

    data = request.json
    base_url = data.get("base_url")
    attack_selection = data.get("attack_selection", {})

    if not base_url:
        return jsonify({"error": "Base URL is required"}), 400

    if not isinstance(attack_selection, dict):
        return jsonify({"error": "Invalid attack_selection format. It must be a dictionary."}), 400

    if attack_selection.get("brute_force", False) and not data.get("username"):
        return jsonify({"error": "Username is required for brute force attack"}), 400

    try:
        task = run_attacks.delay(base_url, {
            "brute_force": {"enabled": attack_selection.get("brute_force", False), "username": data.get("username")},
            "sql_injection": {"enabled": attack_selection.get("sql_injection", False)},
            "dos": {"enabled": attack_selection.get("dos_attack", False)},
        })
    except Exception as e:
        return jsonify({"error": "Failed to submit the task", "details": str(e)}), 500

    try:
        log = RequestLog(
            shieldbot_user_id=shieldbot_user.shieldbot_user_id,  # Updated user field
            base_url=base_url,
            test_type="dynamic",
            options=attack_selection,
            status="Pending"
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": "Failed to log the request", "details": str(e)}), 500

    return jsonify({"task_id": task.id, "message": "Attack task submitted successfully"}), 202


@attack_bp.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 400

    shieldbot_user, error = verify_token(token)
    if not shieldbot_user:
        return jsonify({"error": error}), 401

    task = AsyncResult(task_id)
    if task.state is None:
        return jsonify({"error": "Invalid task ID"}), 404

    if task.state == 'PENDING':
        return jsonify({"status": "Pending"}), 202
    elif task.state == 'SUCCESS':
        return jsonify({"status": "Completed", "result": task.result}), 200
    elif task.state == 'FAILURE':
        return jsonify({"status": "Failed", "error": str(task.info)}), 500
    else:
        return jsonify({"status": task.state}), 200
