import os
import logging
import time
from datetime import datetime, UTC
from backend.database import db
from backend.models import Test

# Import callable test functions directly from their modules.
from backend.attack_scripts.brute_force import brute_force_test
from backend.attack_scripts.sql_injection import sql_injection_test
from backend.attack_scripts.dos_attack import dos_attack_test
from backend.attack_scripts.command_injection_test import command_injection_test
from backend.attack_scripts.csrf_attack_test import csrf_attack_test
from backend.attack_scripts.directory_traversal_test import directory_traversal_test
from backend.attack_scripts.xss_attack_test import xss_attack_test
from backend.attack_scripts.dummy_tests import vulnerability_scan_test, port_scan_test, social_engineering_test

logger = logging.getLogger(__name__)

def execute_test(test_id, base_url, options, user_id):
    """
    Execute the comprehensive cybersecurity test on a new thread.
    Sequentially calls all subtests and, if HF_API_KEY is provided, integrates AI decision making.
    
    After each subtest, it updates the test's heartbeat and checks if the test was aborted.
    """
    # Local import to avoid circular dependencies.
    from backend.app import app

    with app.app_context():
        results = {}
        final_status = "Completed"
        try:
            # Define a list of subtests to run.
            # Each tuple: (label, test function, options key)
            subtests = [
                ("brute_force", brute_force_test, "brute_force"),
                ("sql_injection", sql_injection_test, "sql_injection"),
                ("dos_attack", dos_attack_test, "dos_attack"),
                ("xss_attack", xss_attack_test, "xss_attack"),
                ("directory_traversal", directory_traversal_test, "directory_traversal"),
                ("command_injection", command_injection_test, "command_injection"),
                ("csrf_attack", csrf_attack_test, "csrf_attack"),
                ("vulnerability_scan", vulnerability_scan_test, "vulnerability_scan"),
                ("port_scan", port_scan_test, "port_scan"),
                ("social_engineering", social_engineering_test, "social_engineering")
            ]
            
            for label, test_func, opt_key in subtests:
                if check_if_aborted(test_id):
                    final_status = "Aborted"
                    results["abort"] = f"Test aborted before running {label}"
                    logger.info("Aborting test %s before executing %s", test_id, label)
                    break
                # Ensure that the options for the subtest are a dict.
                subtest_opts = options.get(opt_key, {})
                if not isinstance(subtest_opts, dict):
                    logger.warning("Expected options for subtest '%s' to be a dict but got %s. Resetting to empty dict.",
                                   opt_key, type(subtest_opts))
                    subtest_opts = {}
                results[label] = test_func(base_url, subtest_opts)
                update_heartbeat(test_id)
            else:
                # Only if all tests ran without interruption do we run AI integration.
                hf_key = os.getenv("HF_API_KEY")
                if hf_key:
                    from backend.attack_scripts.ai_integration import ai_decision
                    ai_result = ai_decision(results, hf_key)
                    results["ai_assessment"] = ai_result
                update_heartbeat(test_id)
        except Exception as e:
            logger.exception("Error executing test id %s", test_id)
            results = {"error": "Internal error. Please contact support."}
            final_status = "Failed"
        
        # Optionally simulate a delay at the end.
        time.sleep(2)
        update_heartbeat(test_id)
        
        test_record = Test.query.get(test_id)
        if test_record:
            test_record.result = results
            test_record.status = final_status
            test_record.end_time = datetime.now(UTC)
            db.session.commit()

def update_heartbeat(test_id):
    """Helper function to update the last_updated timestamp for the test."""
    test_record = Test.query.get(test_id)
    if test_record:
        test_record.last_updated = datetime.now(UTC)
        db.session.commit()

def check_if_aborted(test_id):
    """Return True if the test has been aborted."""
    test_record = Test.query.get(test_id)
    return test_record and test_record.status == "Aborted"
