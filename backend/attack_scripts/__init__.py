# attack_scripts/__init__.py

"""
Dynamic loader for all attack test functions in the attack_scripts package.
Each function ending with '_test' from any submodule is automatically imported
and added to the package namespace.
"""

import pkgutil
import importlib
import inspect
from .ai_integration import ai_decision
from .brute_force import brute_force_test
from .command_injection_test import command_injection_test as command_injection
from .csrf_attack_test import csrf_attack_test
from .custom_api import custom_api_test
from .dos_attack import dos_attack_test
from .directory_traversal_test import directory_traversal_test
from .sql_injection import sql_injection_test
from .xss_attack_test import xss_attack_test
from . import dummy_tests

# Dictionary to store all test functions (e.g., {"brute_force_test": brute_force_test, ...})
test_functions = {}

# Iterate over all modules in this package
for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{__name__}.{module_name}")
    # Find all callables in the module whose names end with '_test'
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and name.endswith("_test"):
            test_functions[name] = obj

# Add discovered functions into the package's namespace
globals().update(test_functions)

__all__ = [
    'brute_force',
    'sql_injection', 
    'dos_attack',
    'command_injection',
    'csrf_attack',
    'dummy_tests',
    'directory_traversal_test',
    'xss_attack_test'
]

# Optionally, expose a variable to let other parts of your app iterate easily over all tests
all_tests = test_functions
