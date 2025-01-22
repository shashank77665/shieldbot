
import unittest
from unittest.mock import patch, MagicMock
from backend.attack_scripts.dos_attack import dos_attack_test

class TestDosAttack(unittest.TestCase):
    @patch("backend.attack_scripts.dos_attack.make_request")
    def test_dos_attack_success(self, mock_make_request):
        """
        Simulate a DoS test with multiple requests.
        Each request call is successful (status_code 200).
        """
        mock_response = MagicMock()
        mock_response.status_code = 200

        # Return same mock response on every call
        mock_make_request.return_value = mock_response

        result = dos_attack_test("http://example.com", {"request_count": 3})

        # We expect 3 logs
        self.assertEqual(len(result["logs"]), 3)
        self.assertEqual(result["score"], 8)

        # Check each log message
        for i, log_item in enumerate(result["logs"], start=1):
            self.assertIn(f"Sent DoS request {i}", log_item["message"])
            self.assertIn("status_code", log_item["details"])
            self.assertEqual(log_item["details"]["status_code"], 200)

    @patch("backend.attack_scripts.dos_attack.make_request")
    def test_dos_attack_with_exception(self, mock_make_request):
        """
        Simulate an HTTP request failure in the middle of the loop.
        The first call is successful, the second raises an exception,
        the third is successful again.
        """
        mock_response_ok = MagicMock()
        mock_response_ok.status_code = 200

        # side_effect array: [1st call result, 2nd call exception, 3rd call result]
        mock_make_request.side_effect = [
            mock_response_ok,
            Exception("Network error"),
            mock_response_ok
        ]

        result = dos_attack_test("http://example.com", {"request_count": 3})

        self.assertEqual(len(result["logs"]), 3)
        self.assertEqual(result["score"], 8)

        # 1st log => success
        self.assertIn("Sent DoS request 1", result["logs"][0]["message"])
        self.assertEqual(result["logs"][0]["details"]["status_code"], 200)

        # 2nd log => error
        self.assertIn("Error during DoS request 2", result["logs"][1]["message"])
        self.assertIn("Network error", result["logs"][1]["details"]["error"])

        # 3rd log => success
        self.assertIn("Sent DoS request 3", result["logs"][2]["message"])
        self.assertEqual(result["logs"][2]["details"]["status_code"], 200)

    @patch("backend.attack_scripts.dos_attack.make_request")
    def test_dos_attack_default_count(self, mock_make_request):
        """
        If no 'request_count' is provided, it defaults to 10.
        Let's confirm that all 10 calls are made.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_make_request.return_value = mock_response

        result = dos_attack_test("http://example.com", {})
        self.assertEqual(len(result["logs"]), 10)
        self.assertEqual(result["score"], 8)

        # Verify each log has correct message
        for i, log_item in enumerate(result["logs"], start=1):
            self.assertIn(f"Sent DoS request {i}", log_item["message"])
            self.assertEqual(log_item["details"]["status_code"], 200)

    @patch("backend.attack_scripts.dos_attack.make_request")
    def test_dos_attack_exception_every_time(self, mock_make_request):
        """
        All requests fail with an exception.
        """
        mock_make_request.side_effect = Exception("Mocked failure")

        result = dos_attack_test("http://example.com", {"request_count": 3})
        self.assertEqual(len(result["logs"]), 3)
        for i, log_item in enumerate(result["logs"], start=1):
            self.assertIn(f"Error during DoS request {i}", log_item["message"])
            self.assertIn("Mocked failure", log_item["details"]["error"])

if __name__ == "__main__":
    unittest.main()
