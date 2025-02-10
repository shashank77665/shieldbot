from celery import Celery
from backend.config import Config
import time
import json
import requests
import logging
from backend.attack_scripts import brute_force_test, sql_injection_test, dos_attack_test, command_injection_test, csrf_attack_test, directory_traversal_test, xss_attack_test
import os
# Create the Celery app instance
celery_app = Celery(
    "tasks",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

# Define individual attack simulation functions.
def simulate_brute_force(base_url):
    return f"Simulated brute force test on {base_url}"

def simulate_sql_injection(base_url):
    return f"Simulated SQL injection test on {base_url}"

def simulate_xss_attack(base_url):
    return f"Simulated XSS test on {base_url}"

def simulate_directory_traversal(base_url):
    return f"Simulated directory traversal test on {base_url}"

def simulate_csrf_attack(base_url):
    return f"Simulated CSRF test on {base_url}"

# You can add more attack simulation functions as needed.

def get_attack_logs(base_url, requested_attacks):
    """
    Run simulations for each requested attack.
    requested_attacks should be a list of strings.
    """
    attack_functions = {
        "brute_force": simulate_brute_force,
        "sql_injection": simulate_sql_injection,
        "xss_attack": simulate_xss_attack,
        "directory_traversal": simulate_directory_traversal,
        "csrf_attack": simulate_csrf_attack,
        # Add additional mapping for other attack tests here.
    }

    logs = {}
    for attack in requested_attacks:
        func = attack_functions.get(attack)
        if func:
            logs[attack] = func(base_url)
        else:
            logs[attack] = f"No simulation available for {attack}"
    return logs

@celery_app.task
def run_cyber_test_task(test_id, base_url, test_options, user_id):
    """
    Celery task to conduct cybersecurity tests.
    test_options should include a list under key 'attacks' indicating which tests to run.
    """
    from backend.models import Test
    from backend.database import db

    test = Test.query.get(test_id)
    if not test:
        return {"error": "Test not found"}

    test.status = "Running"
    db.session.commit()
    
    # Determine which attacks to run. 
    # If test_options doesn't specify, default to some tests.
    requested_attacks = test_options.get("attacks", ["brute_force", "sql_injection", "xss_attack"])
    logs = get_attack_logs(base_url, requested_attacks)
    
    # Simulate a delay to represent running the tests.
    time.sleep(5)
    ai_insights = ai_decision(logs)
    
    test.logs = logs
    test.ai_insights = ai_insights
    test.status = "Completed"
    db.session.commit()
    return {"logs": logs, "ai_insights": ai_insights}

def ai_decision(test_logs):
    """
    Performs a dummy AI decision by invoking a Hugging Face inference API (using model: gpt2).
    In case of errors, returns a default recommendation.
    """
    from backend.config import Config
    hf_key = Config.HF_API_KEY
    prompt = "Analyze test logs: " + json.dumps(test_logs)
    headers = {"Authorization": f"Bearer {hf_key}"}
    payload = {"inputs": prompt}
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            headers=headers,
            json=payload,
            timeout=10
        )
        if response.ok:
            return response.json()
        else:
            logging.error("Hugging Face API error: %s", response.text)
            return {"recommendation": "Error in AI assessment", "confidence": 0.0}
    except Exception as e:
        logging.exception("Exception during AI integration")
        return {"recommendation": "Error in AI assessment", "confidence": 0.0}

# Alias for backward compatibility with routes expecting `run_attacks`
run_attacks = run_cyber_test_task

logger = logging.getLogger(__name__)

def execute_test(test_id, base_url, options, user_id):
    """
    Execute all cybersecurity attack tests.
    Aggregates each test's results (logs, score, and success) and logs them.
    """
    results = {}
    tests = {
        "brute_force": brute_force_test,
        "sql_injection": sql_injection_test,
        "dos_attack": dos_attack_test,
        "command_injection": command_injection_test,
        "csrf_attack": csrf_attack_test,
        "directory_traversal": directory_traversal_test,
        "xss_attack": xss_attack_test,
    }
    for test_name, test_func in tests.items():
        try:
            result = test_func(base_url, options.get(test_name, {}))
        except Exception as e:
            result = {
                "logs": [f"Critical error running {test_name}: {str(e)}"],
                "score": 0,
                "success": False,
                "error": str(e)
            }
        results[test_name] = result

    logger.info("Test results: %s", results)
    return results
