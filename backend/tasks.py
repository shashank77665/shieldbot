from celery import Celery
from backend.attack_scripts import brute_force, sql_injection, dos_attack

celery = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")


@celery.task
def run_attacks(base_url, options):
    results = {}

    # Run Brute Force
    results["brute_force"] = brute_force.brute_force_test(base_url, options.get("brute_force", {}))

    # Run SQL Injection
    results["sql_injection"] = sql_injection.sql_injection_test(base_url, options.get("sql_injection", {}))

    # Run DoS Attack
    results["dos_attack"] = dos_attack.dos_attack_test(base_url, options.get("dos", {}))

    return results
