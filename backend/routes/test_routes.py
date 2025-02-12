import threading, time, json, requests, logging
from flask import Blueprint, request, jsonify, current_app, session
from datetime import datetime, UTC
from backend.models import Test, User, ShieldbotUser
from backend.database import db
from backend.utils.jwt_utils import decode_jwt
from backend.config import Config
# Import the comprehensive test executor
from backend.test_executor import execute_test

test_bp = Blueprint("test", __name__, url_prefix="/test")
logger = logging.getLogger(__name__)
hf_key = Config.HF_API_KEY

def get_user_from_token(req):
    token = req.headers.get("Authorization") or session.get("token")
    if not token:
        return None
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    payload, _ = decode_jwt(token)
    if payload:
        return User.query.get(payload.get("user_id"))
    return None

def ai_decision(test_logs, hf_key):
    
    prompt = "Analyze these cyber security test logs and provide intrusion suggestions: " + json.dumps(test_logs)
    headers = {"Authorization": f"Bearer {hf_key}"}
    payload = {"inputs": prompt}
    try:
        response = requests.post("https://api-inference.huggingface.co/models/gpt2",
                                 headers=headers, json=payload, timeout=10)
        if response.ok:
            return response.json()
        else:
            logging.error("Hugging Face API error: %s", response.text)
            return {"recommendation": "Error in AI assessment", "confidence": 0.0}
    except Exception as e:
        logging.exception("Exception when calling Hugging Face API")
        return {"recommendation": "Error in AI assessment", "confidence": 0.0}

def run_cyber_test(app, test_id, base_url, options, user_id):
    """
    Wrapper function to push the Flask application context in a background thread 
    and then call execute_test with the expected 4 arguments.
    """
    with app.app_context():
        execute_test(test_id, base_url, options, user_id)

@test_bp.route("/create", methods=["POST"])
def create_test():
    user = get_user_from_token(request)
    if not user:
        return jsonify({"error": "Authentication required. Please log in or sign up."}), 401

    # Enforce a maximum of 2 concurrent tests per user (considering Pending and Running tests)
    concurrent_tests = [t for t in user.tests if t.status in ["Pending", "Running"]]
    if len(concurrent_tests) >= 2:
        return jsonify({"error": "Maximum concurrent tests reached (2)."}), 403

    data = request.json
    base_url = data.get("base_url")
    test_name = data.get("test_name", "Cyber Test")
    test_options = data.get("options", {})
    if not base_url:
        return jsonify({"error": "Base URL is required"}), 400

    new_test = Test(
         user_id=user.id,
         test_name=test_name,
         base_url=base_url,
         status="Pending"
    )
    db.session.add(new_test)
    db.session.commit()
    
    # Get the actual Flask app instance and pass it to the test executor.
    app_instance = current_app._get_current_object()
    thread = threading.Thread(
        target=run_cyber_test, 
        args=(app_instance, new_test.id, base_url, test_options, user.id)
    )
    thread.start()
    
    return jsonify({
         "message": "Test initiated",
         "test_id": new_test.id,
         "redirect_url": f"/test/status/{new_test.id}"
    }), 202

@test_bp.route("/status/<int:test_id>", methods=["GET"])
def test_status(test_id):
    user = get_user_from_token(request)
    if not user:
        return jsonify({"error": "Authentication required. Please log in or sign up."}), 401
    test = Test.query.get(test_id)
    if not test or test.user_id != user.id:
        return jsonify({"error": "Test not found"}), 404
    return jsonify({
         "test_id": test.id,
         "status": test.status,
         "start_time": test.start_time.isoformat() if test.start_time else None,
         "end_time": test.end_time.isoformat() if test.end_time else None,
         "logs": test.logs,
         "ai_insights": test.ai_insights
    }), 200

@test_bp.route("/abort/<int:test_id>", methods=["POST"])
def abort_test(test_id):
    """
    Abort a cybersecurity test that is currently pending or running.
    Only the user who initiated the test may abort it.
    """
    user = get_user_from_token(request)
    if not user:
        return jsonify({"error": "Authentication required. Please log in or sign up."}), 401

    test = Test.query.get(test_id)
    if not test or test.user_id != user.id:
        return jsonify({"error": "Test not found."}), 404

    if test.status not in ["Pending", "Running"]:
        return jsonify({"error": "Test cannot be aborted. It is already completed or aborted."}), 400

    test.status = "Aborted"
    test.end_time = datetime.now(UTC)
    abort_msg = "Test aborted by user on request."
    if test.logs and isinstance(test.logs, dict):
        test.logs["abort"] = abort_msg
    else:
        test.logs = {"abort": abort_msg}
    db.session.commit()

    return jsonify({
        "message": "Test aborted successfully",
        "test_id": test.id,
        "status": test.status
    }), 200
