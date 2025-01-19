from flask import request, jsonify
from datetime import datetime
from attack_scripts.brute_force import brute_force_test
from attack_scripts.sql_injection import sql_injection_test
from attack_scripts.dos_attack import dos_attack_test
import logging

logger = logging.getLogger("ShieldBotAPI")

def test_website_route():
    try:
        # Parse the request payload
        data = request.json
        base_url = data.get("base_url")

        if not base_url:
            return jsonify({"error": "base_url is required"}), 400

        # Execute Security Tests
        results = {}

        # Brute Force Test
        logs, score, success = brute_force_test(base_url)
        results["brute_force"] = {
            "logs": logs,
            "score": score,
            "success": success,
        }

        # SQL Injection Test
        logs, score, success = sql_injection_test(base_url)
        results["sql_injection"] = {
            "logs": logs,
            "score": score,
            "success": success,
        }

        # DoS Attack Test
        logs, score, success = dos_attack_test(base_url)
        results["dos_attack"] = {
            "logs": logs,
            "score": score,
            "success": success,
        }

        # Compile Final Response
        response = {
            "timestamp": str(datetime.now()),
            "base_url": base_url,
            "results": results,
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error during testing: {e}")
        return jsonify({"error": "Internal server error"}), 500
