import unittest
from unittest.mock import patch, MagicMock
from backend.utils.http_client import make_request

class TestHttpClient(unittest.TestCase):
    @patch("requests.post")
    def test_make_request_post_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = "OK"

        resp = make_request("http://example.com", data={"test": "data"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, "OK")

    @patch("requests.get")
    def test_make_request_get_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "GET OK"

        resp = make_request("http://example.com", method="GET")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, "GET OK")

    @patch("requests.post")
    def test_make_request_exception(self, mock_post):
        mock_post.side_effect = Exception("Request failed")
        with self.assertRaises(RuntimeError) as ctx:
            make_request("http://example.com", data={"test": "data"})
        self.assertIn("HTTP request failed: Request failed", str(ctx.exception))

    @patch("requests.post")
    def test_make_request_bad_status(self, mock_post):
        mock_post.return_value.raise_for_status.side_effect = Exception("Error 404")
        with self.assertRaises(RuntimeError) as ctx:
            make_request("http://example.com", data={"test": "data"})
        self.assertIn("HTTP request failed: Error 404", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
