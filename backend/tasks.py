import time
import json
import requests
import logging
from celery import Celery
from backend.config import Config
from datetime import datetime

# Import your attack functions
from backend.attack_scripts.ddos_attack import ddos_attack_test
from backend.attack_scripts.port_scan import port_scan_test
from backend.attack_scripts.ip_location import ip_location_test
from backend.attack_scripts.brute_force import brute_force_test

import os

# Configure logging
logger = logging.getLogger(__name__)

# Configure the Celery application instance
celery_app = Celery(
    "tasks",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

# Configure Celery to only run one task at a time
celery_app.conf.task_acks_late = True
celery_app.conf.worker_prefetch_multiplier = 1
celery_app.conf.worker_concurrency = 1

# ---------------------------
# Simulation functions for quick testing (optional)
# ---------------------------
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

def get_attack_logs(base_url, requested_attacks):
    """
    Run simulations for each requested attack.
    'requested_attacks' should be a list of strings.
    For actual testing, you can choose to call your real test functions
    (see the execute_test function below) instead of these simulations.
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

# ---------------------------
# Celery Task
# ---------------------------
# ... existing code ...

@celery_app.task(bind=True)
def run_cyber_test_task(self, test_id, base_url, options, user_id):
    """
    Executes a cybersecurity test using the test executor.
    This task is designed to be run asynchronously by Celery.
    
    Args:
        test_id: ID of the test to execute
        base_url: Target URL for the test
        options: Dictionary of test options, including attack_type
        user_id: ID of the user who initiated the test
    """
    from backend.models import Test
    from backend.database import db
    
    # Update task ID in the test record
    with celery_app.app_context():
        test = Test.query.get(test_id)
        if test:
            test.celery_task_id = self.request.id
            test.status = "Running"
            db.session.commit()
    
    # Execute the actual test
    results = execute_test(test_id, base_url, options, user_id)
    
    # Update the test record with results
    with celery_app.app_context():
        test = Test.query.get(test_id)
        if test:
            test.status = "Completed"
            test.end_time = datetime.utcnow()
            test.logs = results
            db.session.commit()
    
    return results

# Alias for backward compatibility - ensure both function signatures match
run_attacks = run_cyber_test_task
# ---------------------------
# Execute Real Tests (Optional)
# ---------------------------
def execute_test(test_id, base_url, options, user_id):
    """
    Executes all cybersecurity attack tests by calling the real functions from your attack scripts.
    Aggregates each test's results (including logs, score, and success) and logs them.
    This function can be used synchronously or be invoked from another Celery task.
    
    Args:
        test_id: ID of the test record
        base_url: Target URL for the test
        options: Dictionary containing test options, including attack_type
        user_id: ID of the user who initiated the test
    """
    from backend.models import Test
    from backend.database import db
    
    # Update test status to Running
    with celery_app.app_context():
        test = Test.query.get(test_id)
        if test:
            test.status = "Running"
            db.session.commit()
    
    results = {}
    attack_type = options.get("attack_type", "")
    test_options = options.get("options", {})
    
    # Map of test types to their respective functions
    tests = {
        "brute_force": brute_force_test,
        "sql_injection": sql_injection_test,
        "dos_attack": dos_attack_test,
        "command_injection": command_injection_test,
        "csrf_attack": csrf_attack_test,
        "directory_traversal": directory_traversal_test,
        "xss_attack": xss_attack_test,
        "port_scan": port_scan_test,
        "ddos": ddos_attack_test,
        "ip_location": ip_location_test,
    }
    
    # Execute the specific test if provided, or all tests if none specified
    if attack_type and attack_type in tests:
        try:
            result = tests[attack_type](base_url, test_options)
            results[attack_type] = result
        except Exception as e:
            results[attack_type] = {
                "logs": [f"Critical error running {attack_type}: {str(e)}"],
                "score": 0,
                "success": False,
                "error": str(e)
            }
    else:
        # Run all tests if no specific test is specified
        for test_name, test_func in tests.items():
            try:
                result = test_func(base_url, test_options.get(test_name, {}))
                results[test_name] = result
            except Exception as e:
                results[test_name] = {
                    "logs": [f"Critical error running {test_name}: {str(e)}"],
                    "score": 0,
                    "success": False,
                    "error": str(e)
                }
    
    # Update test status to Completed
    with celery_app.app_context():
        test = Test.query.get(test_id)
        if test:
            test.status = "Completed"
            test.end_time = datetime.utcnow()
            test.logs = results
            db.session.commit()
    
    logger.info("Test results: %s", results)
    return results

# You can choose to call execute_test() within your tasks instead of or in addition to simulate tests.
