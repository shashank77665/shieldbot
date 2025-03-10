import unittest
from backend.utils.response_parser import parse_response, format_log

class MockResponse:
    def __init__(self, status_code=200, text="", headers=None):
        self.status_code = status_code
        self.text = text
        self.headers = headers if headers else {}

class TestResponseParser(unittest.TestCase):
    def test_parse_response(self):
        mock_resp = MockResponse(200, "This is a test response", {"Content-Type": "text/html"})
        result = parse_response(mock_resp)

        self.assertEqual(result["status_code"], 200)
        self.assertIn("content_snippet", result)
        self.assertEqual(result["content_snippet"], "This is a test response"[:200])
        self.assertEqual(result["headers"], {"Content-Type": "text/html"})

    def test_parse_response_large_text(self):
        text_data = "A" * 300  # Over 200 characters
        mock_resp = MockResponse(200, text_data, {"Content-Length": "300"})
        result = parse_response(mock_resp)
        self.assertEqual(len(result["content_snippet"]), 200)

    def test_format_log(self):
        log = format_log("Test message", {"key": "value"})
        self.assertIn("timestamp", log)
        self.assertEqual(log["message"], "Test message")
        self.assertEqual(log["details"]["key"], "value")

if __name__ == "__main__":
    unittest.main()
