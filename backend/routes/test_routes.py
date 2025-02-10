import threading, time, json, requests, logging
from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.models import Test, User
from backend.database import db
from backend.utils.jwt_utils import decode_jwt
from backend.config import Config

test_bp = Blueprint("test", __name__, url_prefix="/test")

def get_user_from_token(req):
    token = req.headers.get("Authorization", "")
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    payload, _ = decode_jwt(token)
    if payload:
        return User.query.get(payload.get("user_id"))
    return None

def ai_decision(test_logs):
    hf_key = Config.HF_API_KEY
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

def run_cyber_test(test_id, base_url, test_options, user_id):
    test = Test.query.get(test_id)
    if not test:
        return
    test.status = "Running"
    db.session.commit()
    
    # Simulate subtests – here we simply generate dummy log messages.
    logs = {
        "brute_force": f"Simulated brute force test on {base_url}.",
        "sql_injection": f"Simulated SQL injection test on {base_url}.",
        "xss_attack": f"Simulated XSS test on {base_url}."
    }
    # Simulate a delay for test execution.
    time.sleep(5)
    
    ai_insights = ai_decision(logs)
    
    test.logs = logs
    test.ai_insights = ai_insights
    test.status = "Completed"
    test.end_time = datetime.utcnow()
    db.session.commit()

@test_bp.route("/create", methods=["POST"])
def create_test():
    user = get_user_from_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    # Enforce max 2 concurrent tests per user.
    running_tests = [t for t in user.tests if t.status == "Running"]
    if len(running_tests) >= 2:
        return jsonify({"error": "Maximum concurrent tests reached (2)."}), 403

    data = request.json
    base_url = data.get("base_url")
    test_name = data.get("test_name", "Cyber Test")
    test_options = data.get("options", {})
    if not base_url:
        return jsonify({"error": "Base URL is required"}), 400

    new_test = Test(
         user_id = user.id,
         test_name = test_name,
         base_url = base_url,
         status = "Pending"
    )
    db.session.add(new_test)
    db.session.commit()
    
    # Spawn a new thread to run the test.
    thread = threading.Thread(target=run_cyber_test, args=(new_test.id, base_url, test_options, user.id))
    thread.start()
    
    return jsonify({"message": "Test initiated", "test_id": new_test.id}), 202

@test_bp.route("/status/<int:test_id>", methods=["GET"])
def test_status(test_id):
    user = get_user_from_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    test = Test.query.get(test_id)
    if not test or test.user_id != user.id:
        return jsonify({"error": "Test not found"}), 404
    return jsonify({
         "test_id": test.id,
         "status": test.status,
         "start_time": test.start_time.isoformat(),
         "end_time": test.end_time.isoformat() if test.end_time else None,
         "logs": test.logs,
         "ai_insights": test.ai_insights
    }), 200