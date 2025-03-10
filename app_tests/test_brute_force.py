import unittest
from unittest.mock import patch, MagicMock
from backend.attack_scripts.brute_force import brute_force_test

class TestBruteForce(unittest.TestCase):
    @patch("requests.post")
    def test_brute_force_success(self, mock_post):
        """
        Simulate a successful login on the first password attempt.
        """
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = "Login successful"

        result = brute_force_test("http://example.com", {
            "username": "admin",
            "password_list": ["admin", "password123"],
            "login_endpoint": "/login"
        })
        self.assertEqual(result["attempted"], 1)
        self.assertTrue(result["success"])
        self.assertIn("username", result["details"])
        self.assertEqual(result["details"]["password"], "admin")

    @patch("requests.post")
    def test_brute_force_no_match(self, mock_post):
        """
        Simulate no matching credentials found.
        """
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = "Login failed"  # Not recognized as success

        result = brute_force_test("http://example.com", {
            "username": "admin",
            "password_list": ["pass1", "pass2"],
            "login_endpoint": "/login"
        })
        self.assertEqual(result["attempted"], 2)
        self.assertFalse(result["success"])
        self.assertIn("Brute force attack failed", result["details"])

    @patch("requests.post")
    def test_brute_force_missing_username(self, mock_post):
        """
        Test missing required fields like 'username'.
        This should return an error in the result dictionary.
        """
        result = brute_force_test("http://example.com", {
            "password_list": ["admin", "password123"]
        })
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Username and password list are required")

    @patch("requests.post")
    def test_brute_force_exception(self, mock_post):
        """
        Simulate an exception from requests (e.g., ConnectionError).
        """
        mock_post.side_effect = Exception("Connection Error")
        result = brute_force_test("http://example.com", {
            "username": "admin",
            "password_list": ["admin", "password123"]
        })
        self.assertIn("error", result["details"])
        self.assertFalse(result["success"])

if __name__ == "__main__":
    unittest.main()
