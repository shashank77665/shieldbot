import unittest
from unittest.mock import patch,MagicMock
from backend.attack_scripts.sql_injection import sql_injection_test

class TestSQLInjection(unittest.TestCase):
    @patch("backend.utils.http_client.make_request")
    def test_sql_injection_default_payloads(self, mock_request):
        """
        Test default payloads if none provided. 
        """
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_request.return_value = mock_resp

        result = sql_injection_test("http://example.com", {})
        self.assertIn("logs", result)
        self.assertEqual(result["score"], 5)

    @patch("backend.utils.http_client.make_request")
    def test_sql_injection_custom_payloads(self, mock_request):
        """
        Provide custom payloads to test coverage.
        """
        mock_request.return_value.status_code = 200
        result = sql_injection_test("http://example.com", {
            "payloads": ["' OR '1'='1", "' UNION SELECT --"]
        })
        self.assertEqual(len(result["logs"]), 2)

    @patch("backend.utils.http_client.make_request")
    def test_sql_injection_exception(self, mock_request):
        """
        Simulate request exception or error.
        """
        mock_request.side_effect = Exception("HTTP error")
        result = sql_injection_test("http://example.com", {"payloads": ["attack"]})
        self.assertIn("Error testing payload", result["logs"][0]["message"])

if __name__ == "__main__":
    unittest.main()
