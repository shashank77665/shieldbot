from celery import Celery
from backend.attack_scripts import brute_force, sql_injection, dos_attack
from backend.attack_scripts import xss_attack, directory_traversal, command_injection, csrf_attack
# optionally csrf_attack

celery = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

@celery.task
def run_attacks(base_url, options):
    results = {}

    # Existing
    results["brute_force"] = brute_force.brute_force_test(base_url, options.get("brute_force", {}))
    results["sql_injection"] = sql_injection.sql_injection_test(base_url, options.get("sql_injection", {}))
    results["dos_attack"]   = dos_attack.dos_attack_test(base_url, options.get("dos_attack", {}))

    # New attacks
    results["xss_attack"] = xss_attack.xss_attack_test(base_url, options.get("xss_attack", {}))
    results["directory_traversal"] = directory_traversal.directory_traversal_test(base_url, options.get("directory_traversal", {}))
    results["command_injection"]   = command_injection.command_injection_test(base_url, options.get("command_injection", {}))
    # optionally csrf_attack
    results["csrf_attack"]         = csrf_attack.csrf_attack_test(base_url, options.get("csrf_attack", {}))

    return results
