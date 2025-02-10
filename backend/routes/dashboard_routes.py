from flask import Blueprint, request, jsonify
from backend.models import RequestLog, ShieldbotUser
from backend.utils.jwt_utils import decode_and_verify_token

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/", methods=["GET"])
def dashboard():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 401
    
    shieldbot_user, error = decode_and_verify_token(token)
    if error:
        return jsonify({"error": error}), 401

    # Get test logs for this user (ordered by most recent)
    tests = RequestLog.query.filter_by(
        shieldbot_user_id=shieldbot_user.shieldbot_user_id
    ).order_by(RequestLog.timestamp.desc()).all()
    tests_summary = [{
        "test_id": test.id,
        "base_url": test.base_url,
        "status": test.status,
        "timestamp": test.timestamp.isoformat(),
        "test_type": test.test_type
    } for test in tests]

    # Count currently running tests
    running_count = RequestLog.query.filter_by(
        shieldbot_user_id=shieldbot_user.shieldbot_user_id, status="Running"
    ).count()
    
    dashboard_info = {
        "username": shieldbot_user.username,
        "total_tests": len(tests),
        "running_tests": running_count,
        "tests": tests_summary
    }
    
    return jsonify(dashboard_info), 200

@dashboard_bp.route("/home", methods=["GET"])
def home():
    available_attacks = [
        {"name": "Brute Force Attack", "description": "Test common credentials using brute force."},
        {"name": "SQL Injection", "description": "Test for SQL injection vulnerabilities."},
        {"name": "DoS Attack", "description": "Simulate denial-of-service conditions."},
        {"name": "XSS Attack", "description": "Check for Cross-Site Scripting vulnerabilities."},
        {"name": "Directory Traversal", "description": "Test for path traversal vulnerabilities."},
        {"name": "Command Injection", "description": "Attempt command injection exploits."},
        {"name": "CSRF Attack", "description": "Test for Cross-Site Request Forgery flaws."},
        {"name": "Vulnerability Scan", "description": "Scan for common vulnerabilities using heuristics."},
        {"name": "Port Scan", "description": "Identify open ports and services."},
        {"name": "Social Engineering Simulation", "description": "Simulate social engineering attack vectors."}
    ]
    return jsonify({"available_attacks": available_attacks}), 200

@dashboard_bp.route("/terms", methods=["GET"])
def terms():
    user_agreement = """
    User Agreement and Disclaimer

    1. Authorized Use Only: The services provided are for authorized, legal security testing of systems you own or have explicit permission to test.
    2. User Responsibility: You are solely responsible for compliance with all applicable laws. Any misuse or illegal activity is your responsibility.
    3. Prohibited Activities: Unauthorized penetration testing, malicious attacks, or any illegal use of these tools is strictly prohibited.
    4. Indemnification: You agree to hold harmless the website owners and developers from any claims arising from your misuse.
    5. Superuser/Administrator Protection: Administrative functions are secured via strong authentication.
    6. AI-Based Vulnerability Scanning: AI integrations are provided for research purposes only and should not be solely relied upon.
    """
    return jsonify({"user_agreement": user_agreement}), 200