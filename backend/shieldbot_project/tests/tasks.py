from celery import shared_task
import time
from datetime import timedelta
from django.utils import timezone
from celery.result import AsyncResult
from tests.models import Test
from attacks.brute_force import brute_force_test

@shared_task
def monitor_tests(check_interval=10, timeout_threshold=20):
    """
    Monitor tests and update their status based on Celery task status
    and timeout thresholds.
    
    Args:
        check_interval (int): How often to check tests in seconds
        timeout_threshold (int): How many seconds to wait before marking a stalled test as aborted
    """
    now = timezone.now()
    # Find tests that are still in-progress
    tests_to_check = Test.objects.filter(status__in=["Pending", "Running"])
    tests_updated = False
    
    for test in tests_to_check:
        # Check for timeouts
        last_update = test.last_updated or test.start_time
        if now - last_update > timedelta(seconds=timeout_threshold):
            test.status = "Aborted"
            test.end_time = now
            test.save()
            tests_updated = True
            continue
            
        # Check celery state if a celery_task_id is available
        if test.celery_task_id:
            celery_result = AsyncResult(test.celery_task_id)
            if celery_result.state != test.status:
                test.status = celery_result.state
                # Update end_time if the task has completed
                if celery_result.state in ['SUCCESS', 'FAILURE']:
                    test.end_time = now
                test.save()
                tests_updated = True
    
    return {"updated_tests": tests_updated}

@shared_task
def periodic_monitor_tests():
    """
    A periodic task that runs monitor_tests in a loop with a sleep interval.
    This is meant to be registered as a beat task to continuously monitor tests.
    """
    while True:
        monitor_tests()
        time.sleep(10)  # Check every 10 seconds 

@shared_task
def run_brute_force_test(test_id, base_url, options, user_id):
    result = brute_force_test(base_url, options)
    test = Test.objects.get(id=test_id)
    test.logs = result
    test.status = 'Completed'
    test.end_time = timezone.now()
    test.save()
    return result 

@shared_task
def run_security_test(test_id, test_type, base_url, options=None):
    """
    Run a security test as a Celery task
    """
    try:
        test = Test.objects.get(id=test_id)
        test.status = 'Running'
        test.save()

        # Import the appropriate test function based on test_type
        if test_type == 'brute_force':
            from attacks.brute_force import brute_force_test
            result = brute_force_test(base_url, options)
        elif test_type == 'sql_injection':
            from attacks.sql_injection import sql_injection_test
            result = sql_injection_test(base_url, options)
        # Add other test types as needed

        # Update test results
        test.logs = result
        test.status = 'Completed'
        test.end_time = timezone.now()
        test.save()

        return result

    except Exception as e:
        if test:
            test.status = 'Failed'
            test.logs = {'error': str(e)}
            test.end_time = timezone.now()
            test.save()
        raise 