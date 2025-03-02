from flask import Blueprint, request, jsonify, session
from backend.models import Test, ShieldbotUser
from backend.utils.jwt_utils import decode_and_verify_token
import logging

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")
logger = logging.getLogger(__name__)

def get_authenticated_user():
    """
    First, try to obtain the user based on the session.  If not in session,
    then try to decode the bearer token from the Authorization header.
    """
    # Check if session holds the user ID.
    user_id = session.get("user_id")
    if user_id:
        user = ShieldbotUser.query.get(user_id)
        if user:
            return user, None
        else:
            return None, "User not found in session."
    
    # Next, try to retrieve and decode a bearer token from the header.
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    if token:
        user, error = decode_and_verify_token(token)
        if error:
            return None, error
        return user, None
    
    return None, "Authentication required. Please log in or sign up."

@dashboard_bp.route("/", methods=["GET"])
def dashboard():
    shieldbot_user, error = get_authenticated_user()
    if error:
        return jsonify({"error": error}), 401

    try:
        # Query all tests for the current user, ordering by the most recent.
        tests = Test.query.filter_by(user_id=shieldbot_user.id).order_by(Test.start_time.desc()).all()
        logger.debug("Fetched %d tests for user_id %s", len(tests), shieldbot_user.id)
    except Exception as err:
        logger.exception("Error fetching tests for user_id %s: %s", shieldbot_user.id, err)
        return jsonify({"error": "Error fetching tests"}), 500

    tests_summary = [{
        "test_id": test.id,
        "test_name": test.test_name,
        "base_url": test.base_url,
        "status": test.status,
        "start_time": test.start_time.isoformat() if test.start_time else None,
        "end_time": test.end_time.isoformat() if test.end_time else None,
        "logs": test.logs,
        "ai_insights": test.ai_insights
    } for test in tests]

    running_count = Test.query.filter(
        Test.user_id == shieldbot_user.id,
        Test.status.in_(["Pending", "Running"])
    ).count()
    
    dashboard_info = {
        "username": shieldbot_user.username,
        "profile_picture": shieldbot_user.profile_picture,
        "total_tests": len(tests),
        "running_tests": running_count,
        "tests": tests_summary
    }
    
    return jsonify(dashboard_info), 200

@dashboard_bp.route("/home", methods=["GET"])
def home():
    shieldbot_user, error = get_authenticated_user()
    if error:
        return jsonify({"error": error}), 401

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