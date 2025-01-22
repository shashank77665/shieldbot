import unittest
from unittest.mock import patch
from backend.tasks import run_attacks

class TestTasks(unittest.TestCase):
    @patch("backend.attack_scripts.brute_force.brute_force_test")
    @patch("backend.attack_scripts.sql_injection.sql_injection_test")
    @patch("backend.attack_scripts.dos_attack.dos_attack_test")
    def test_run_attacks_all_enabled(self, mock_dos, mock_sql, mock_brute):
        mock_brute.return_value = {
            "attempted": 2,
            "success": True,
            "details": {"username": "admin", "password": "secret"}
        }
        mock_sql.return_value = {"logs": ["SQL test"]}
        mock_dos.return_value = {"logs": ["DoS test"]}
    
        result = run_attacks("http://example.com", {
            "brute_force": {"enabled": True},
            "sql_injection": {"enabled": True},
            "dos": {"enabled": True}
        })
    
        self.assertIn("brute_force", result)
        self.assertTrue(result["brute_force"])

    def test_run_attacks_no_options(self):
        """
        Test if no 'enabled' attack type is provided, 
        or if the dictionary is empty.
        """
        result = run_attacks("http://example.com", {})
        self.assertIn("brute_force", result)  # With default or disabled?
        self.assertIn("sql_injection", result)
        self.assertIn("dos_attack", result)

if __name__ == "__main__":
    unittest.main()
