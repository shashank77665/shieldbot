from flask import Blueprint, request, jsonify, session
from backend.attack_scripts import (
    all_tests  # This now contains all test functions discovered
)
# Import the dummy custom API test function
from backend.attack_scripts.custom_api import custom_api_test
from backend.utils.tool_installer import install_security_tools
from backend.utils.jwt_utils import decode_and_verify_token

custom_tests_bp = Blueprint("custom_tests", __name__, url_prefix="/custom-tests")

@custom_tests_bp.route("/run", methods=["POST"])
def run_custom_tests():
    data = request.json
    token = request.headers.get("Authorization") or session.get("token")
    # Require authentication before proceeding.
    if not token:
        return jsonify({"error": "Authentication required. Please log in or sign up."}), 401

    user, error = decode_and_verify_token(token)
    if error:
        return jsonify({"error": error}), 401
    base_url = data.get("base_url")
    tests_flags = data.get("tests", {})
    results = {}
    for test_name, test_enabled in tests_flags.items():
        if test_enabled:
            if test_name == "custom_api_test":
                custom_opts = data.get("custom_api_options", {})
                api_url = custom_opts.get("api_url")
                payload = custom_opts.get("payload", {})
                if api_url:
                    try:
                        results["custom_api_test"] = custom_api_test(api_url, payload)
                    except Exception as e:
                        results["custom_api_test"] = {"error": str(e)}
                else:
                    results["custom_api_test"] = "api_url not provided."
            else:
                # For example, route to other tests
                test_func = globals().get(f"{test_name}_test")
                if test_func:
                    try:
                        results[test_name] = test_func(base_url, data.get(test_name, {}))
                    except Exception as e:
                        results[test_name] = {"error": str(e)}
                else:
                    results[test_name] = f"Test '{test_name}' not implemented."
        else:
            results[test_name] = "Test skipped."
    return jsonify(results), 200

@custom_tests_bp.route('/list_tests', methods=['GET'])
def list_tests():
    # Return the list of available test names
    return jsonify({"available_tests": list(all_tests.keys())})

@custom_tests_bp.route('/run_test/<test_name>', methods=['POST'])
def run_test(test_name):
    test_func = all_tests.get(test_name)
    if not test_func:
        return jsonify({"error": "Test not found"}), 404

    # Execute the test and return the result (assuming the test function returns something)
    result = test_func()
    return jsonify({"result": result}) 