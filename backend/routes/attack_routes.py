from flask import Blueprint, request, jsonify, session, redirect, url_for
from backend.tasks import run_attacks
from celery.result import AsyncResult
from backend.models import Test, ShieldbotUser, RequestLog
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
from datetime import datetime
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
    if token and token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    return decode_and_verify_token(token)


@attack_bp.route('/perform-test', methods=['POST'])
def perform_test():
    # Try to obtain token from Authorization header or session
    token = request.headers.get("Authorization") or session.get("token")
    if not token:
        # Redirect to login if no token
        return jsonify({
            "error": "Authentication required",
            "redirect": "/auth/login"
        }), 401

    # Verify token
    user, error = verify_token(token)
    if error:
        return jsonify({
            "error": error,
            "redirect": "/auth/login"
        }), 401

    # Get data from request
    data = request.json
    base_url = data.get("base_url")
    test_type = data.get("test_type", "comprehensive")
    test_name = data.get("test_name", f"Test {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}")
    options = data.get("options", {})
    attack_type = options.get("attack_type", "")

    # Validate URL
    if not base_url:
        return jsonify({"error": "Base URL is required"}), 400
    if not is_valid_url(base_url):
        return jsonify({"error": "Invalid URL provided"}), 400

    # Check for any running tests by this user
    running_tests = Test.query.filter_by(user_id=user.id, status="Running").all()
    if running_tests:
        return jsonify({
            "error": "You already have a test running. Only one test can run at a time."
        }), 403

    # Create new test record
    new_test = Test(
        user_id=user.id,
        base_url=base_url,
        test_type=test_type,
        # test_name=test_name,
        status="Pending"
    )
    db.session.add(new_test)
    db.session.commit()

    # Start Celery task
    test_options = {
        "attack_type": attack_type,
        "options": options
    }
    task = run_attacks.delay(new_test.id, base_url, test_options, user.id)
    
    # Update test with task ID
    new_test.task_id = task.id
    new_test.celery_task_id = task.id
    db.session.commit()

    return jsonify({
        "test_id": new_test.id,
        "task_id": task.id,
        "message": "Test initiated successfully"
    }), 202


@attack_bp.route('/test-status/<test_id>', methods=['GET'])
def test_status(test_id):
    # Check authentication
    token = request.headers.get("Authorization") or session.get("token")
    if not token:
        return jsonify({
            "error": "Authentication required",
            "redirect": "/auth/login"
        }), 401

    user, error = verify_token(token)
    if error:
        return jsonify({
            "error": error,
            "redirect": "/auth/login"
        }), 401

    # Get test by ID
    test = Test.query.get(test_id)
    if not test:
        return jsonify({"error": "Test not found"}), 404

    # Ensure user owns this test
    if test.user_id != user.id:
        return jsonify({"error": "You don't have permission to view this test"}), 403

    # Return test status and logs
    return jsonify({
        "id": test.id,
        "status": test.status,
        "type": test.test_type,
        "base_url": test.base_url,
        "start_time": test.start_time.isoformat() if test.start_time else None,
        "end_time": test.end_time.isoformat() if test.end_time else None,
        "logs": test.logs
    }), 200


@attack_bp.route('/list-tests', methods=['GET'])
def list_tests():
    # Check authentication
    token = request.headers.get("Authorization") or session.get("token")
    if not token:
        return jsonify({
            "error": "Authentication required",
            "redirect": "/auth/login"
        }), 401

    user, error = verify_token(token)
    if error:
        return jsonify({
            "error": error,
            "redirect": "/auth/login"
        }), 401

    # Get all tests for this user
    tests = Test.query.filter_by(user_id=user.id).order_by(Test.start_time.desc()).all()
    
    # Format test data
    test_list = [{
        "id": test.id,
        "status": test.status,
        "type": test.test_type,
        "base_url": test.base_url,
        "start_time": test.start_time.isoformat() if test.start_time else None,
        "end_time": test.end_time.isoformat() if test.end_time else None
    } for test in tests]

    return jsonify({"tests": test_list}), 200


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

@attack_bp.route('/stop-ddos', methods=['POST'])
def stop_ddos():
    token = request.headers.get("Authorization") or session.get("token")
    if not token:
        return jsonify({"error": "Authentication required. Please log in or sign up."}), 401

    shieldbot_user, error = verify_token(token)
    if not shieldbot_user:
        return jsonify({"error": error}), 401

    data = request.json
    agents = data.get("agents")
    if not agents:
        return jsonify({"error": "Agents list is required."}), 400

    # Call the ddos_stop_attack_test function from ddos_attack.py
    from backend.attack_scripts.ddos_attack_test import ddos_stop_attack_test
    options = {"agents": agents}
    result = ddos_stop_attack_test(options)
    return jsonify(result), 200

@attack_bp.route('/stop-all-ddos', methods=['POST'])
def stop_all_ddos():
    token = request.headers.get("Authorization") or session.get("token")
    if not token:
        return jsonify({"error": "Authentication required. Please log in or sign up."}), 401

    shieldbot_user, error = verify_token(token)
    if not shieldbot_user:
        return jsonify({"error": error}), 401

    # Default list of all known agent addresses.
    default_agents = ["192.168.1.101:5000", "192.168.1.102:5000", "192.168.1.103:5000"]

    from backend.attack_scripts.ddos_attack_test import ddos_stop_attack_test
    options = {"agents": default_agents}
    result = ddos_stop_attack_test(options)
    return jsonify(result), 200

@attack_bp.route('/get_command', methods=['GET'])
def get_command():
    """
    Endpoint for agents to poll for a new command.
    In this basic implementation, we return that no command is scheduled.
    In production, you might query a database or command queue.
    """
    return jsonify({"execute": False}), 200


@attack_bp.route('/execute', methods=['POST'])
def attack_execute():
    """
    Endpoint to initiate an attack command from the central server.
    Expected JSON payload:
    {
      "command": "ddos_attack",
      "params": {
          "base_url": "http://example.com",
          "workers": 5,
          "processes_per_worker": 10,
          "agents": ["192.168.1.101:5000", "192.168.1.102:5000"]
      }
    }
    If the command is recognized, it uses ddos_attack_test to dispatch the command to all agents.
    """
    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"error": "Missing command in payload."}), 400

    command = data.get("command")
    if command == "ddos_attack":
        from backend.attack_scripts.ddos_attack_test import ddos_attack_test
        result = ddos_attack_test("", data.get("params", {}))
        return jsonify(result), 200
    else:
        return jsonify({"error": "Unsupported command."}), 400
