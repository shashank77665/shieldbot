import os
import logging
import time
from backend.database import db
from backend.models import RequestLog

logger = logging.getLogger(__name__)

def execute_test(test_id, base_url, options, user_id):
    """
    Execute the comprehensive cyber security test on a new thread.
    Sequentially calls all subtests and (if HF_API_KEY is provided)
    integrates AI decision making.
    """
    results = {}
    final_status = "Completed"
    try:
        from backend.attack_scripts import brute_force, sql_injection, dos_attack, xss_attack, directory_traversal, command_injection, csrf_attack
        from backend.attack_scripts import dummy_tests

        results["brute_force"] = brute_force.brute_force_test(base_url, options.get("brute_force", {}))
        results["sql_injection"] = sql_injection.sql_injection_test(base_url, options.get("sql_injection", {}))
        results["dos_attack"] = dos_attack.dos_attack_test(base_url, options.get("dos_attack", {}))
        results["xss_attack"] = xss_attack.xss_attack_test(base_url, options.get("xss_attack", {}))
        results["directory_traversal"] = directory_traversal.directory_traversal_test(
            base_url, options.get("directory_traversal", {}))
        results["command_injection"] = command_injection.command_injection_test(
            base_url, options.get("command_injection", {}))
        results["csrf_attack"] = csrf_attack.csrf_attack_test(base_url, options.get("csrf_attack", {}))
        results["vulnerability_scan"] = dummy_tests.vulnerability_scan_test(
            base_url, options.get("vulnerability_scan", {}))
        results["port_scan"] = dummy_tests.port_scan_test(
            base_url, options.get("port_scan", {}))
        results["social_engineering"] = dummy_tests.social_engineering_test(
            base_url, options.get("social_engineering", {}))
        
        hf_key = os.getenv("HF_API_KEY")
        if hf_key:
            from backend.attack_scripts.ai_integration import ai_decision
            ai_result = ai_decision(results, hf_key)
            results["ai_assessment"] = ai_result

    except Exception as e:
        logger.exception("Error executing test id %s", test_id)
        results = {"error": "Internal error. Please contact support."}
        final_status = "Failed"
    
    # Optionally simulate test duration
    time.sleep(2)
    
    test_log = RequestLog.query.get(test_id)
    if test_log:
        test_log.result = results
        test_log.status = final_status
        db.session.commit()