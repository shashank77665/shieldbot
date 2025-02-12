from flask import Blueprint, request, jsonify, session
from backend.tasks import run_attacks
from celery.result import AsyncResult
from backend.models import RequestLog, ShieldbotUser
from backend.database import db
import jwt
from dotenv import load_dotenv
import os
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from backend.utils.jwt_utils import create_jwt, decode_and_verify_token
from backend.utils.jwt_utils import decode_and_verify_token as legacy_verify_token
from backend.utils.jwt_utils import decode_and_verify_token
from backend.utils.auth_decorator import authorize
from backend.test_executor import execute_test
import threading
from urllib.parse import urlparse
from backend.tasks import run_attacks
load_dotenv()

# Blueprint for attack routes
attack_bp = Blueprint("attack", __name__, url_prefix="/attack")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")


def is_valid_url(url):
    try:
        result = urlparse(url)
        return result.scheme in ("http", "https") and bool(result.netloc)
    except Exception:
        return False


def verify_token(token):
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    user, error = decode_and_verify_token(token)
    return user, error


@attack_bp.route('/perform-test', methods=['POST'])
def perform_test():
    # Try to obtain token from Authorization header; if not provided, check session.
    token = request.headers.get("Authorization") or session.get("token")
    if not token:
        return jsonify({"error": "Authentication required. Please log in or sign up."}), 401

    shieldbot_user, error = verify_token(token)
    if not shieldbot_user:
        return jsonify({"error": error or "Unauthorized"}), 401

    data = request.json
    base_url = data.get("base_url")
    options = data.get("attack_selection", {})

    if not base_url:
        return jsonify({"error": "Base URL is required"}), 400
    if not is_valid_url(base_url):
        return jsonify({"error": "Invalid URL provided"}), 400

    # Enforce a limit on concurrent tests per user.
    running_tests_count = RequestLog.query.filter_by(
        shieldbot_user_id=shieldbot_user.shieldbot_user_id, status="Running"
    ).count()
    if running_tests_count >= 2:
        return jsonify({
            "error": "You have reached the maximum number of concurrent tests (2). Please wait until one completes."
        }), 403

    # Log the test request.
    new_log = RequestLog(
        shieldbot_user_id=shieldbot_user.shieldbot_user_id,
        base_url=base_url,
        test_type="comprehensive",
        options=options,
        status="Running"
    )
    db.session.add(new_log)
    db.session.commit()

    # Spawn a new thread to run the test.
    thread = threading.Thread(
        target=execute_test,
        args=(new_log.id, base_url, options, shieldbot_user.shieldbot_user_id)
    )
    thread.start()

    return jsonify({"test_id": new_log.id, "message": "Test initiated successfully"}), 202


@attack_bp.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    token = request.headers.get("Authorization") or session.get("token")
    if not token:
        return jsonify({"error": "Authentication required. Please log in or sign up."}), 401

    shieldbot_user, error = verify_token(token)
    if not shieldbot_user:
        return jsonify({"error": error}), 401

    task = AsyncResult(task_id)
    if task.state is None:
        return jsonify({"error": "Invalid task ID"}), 404

    if task.state == 'PENDING':
        return jsonify({"status": "Pending"}), 202
    elif task.state == 'SUCCEDED':
        return jsonify({"status": "Completed", "result": task.result}), 200
    elif task.state == 'FAILURE':
        return jsonify({"status": "Failed", "error": str(task.info)}), 500
    else:
        return jsonify({"status": task.state}), 200


@attack_bp.route('/start', methods=['POST'])
def start_attack():
    data = request.json
    token = request.headers.get("Authorization") or session.get("token")
    if not token:
        return jsonify({"error": "Authentication required. Please log in or sign up."}), 401

    shieldbot_user, error = verify_token(token)
    if not shieldbot_user:
        return jsonify({"error": error}), 401

    base_url = data.get("base_url")
    attack_type = data.get("attack_type")
    options = data.get("options", {})

    if not base_url:
        return jsonify({"error": "Base URL is required."}), 400
    if not is_valid_url(base_url):
        return jsonify({"error": "Invalid URL provided."}), 400
    if not attack_type:
        return jsonify({"error": "Attack type is required."}), 400

    allowed_attacks = [
        "Brute Force Attack",
        "SQL Injection",
        "DoS Attack",
        "XSS Attack",
        "Directory Traversal",
        "Command Injection",
        "CSRF Attack",
        "Vulnerability Scan",
        "Port Scan",
        "Social Engineering Simulation"
    ]

    if attack_type not in allowed_attacks:
        return jsonify({
            "error": "Invalid attack type. Allowed types: " + ", ".join(allowed_attacks)
        }), 400

    # Log the attack request with status "Running".
    new_log = RequestLog(
        shieldbot_user_id=shieldbot_user.shieldbot_user_id,
        base_url=base_url,
        test_type=attack_type,
        options=options,
        status="Running"
    )
    db.session.add(new_log)
    db.session.commit()

    # Spawn a new thread to run the attack.
    thread = threading.Thread(
        target=run_attacks,
        args=(new_log.id, base_url, options, shieldbot_user.shieldbot_user_id, attack_type)
    )
    thread.start()

    return jsonify({"attack_id": new_log.id, "message": "Attack initiated successfully"}), 202
