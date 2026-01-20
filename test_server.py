"""Tests for the HTTP server JSON responses."""

import json
import threading
import time
import unittest
from http.client import HTTPConnection

from server import APIHandler
from http.server import HTTPServer


class ServerTestCase(unittest.TestCase):
    """Base test case that starts/stops the server."""

    @classmethod
    def setUpClass(cls):
        """Start the server in a background thread."""
        cls.server = HTTPServer(("localhost", 8765), APIHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(0.1)  # Give server time to start

    @classmethod
    def tearDownClass(cls):
        """Shut down the server."""
        cls.server.shutdown()
        cls.server_thread.join(timeout=1)

    def make_request(self, path, method="GET", body=None):
        """Make an HTTP request and return (status_code, parsed_json)."""
        conn = HTTPConnection("localhost", 8765)
        headers = {"Content-Type": "application/json"} if body else {}
        conn.request(method, path, body=body, headers=headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        conn.close()
        return response.status, json.loads(data)


class TestJSONResponse(ServerTestCase):
    """Test that the server returns valid JSON responses."""

    def test_root_returns_valid_json(self):
        """GET / should return valid JSON with message and version."""
        status, data = self.make_request("/")
        self.assertEqual(status, 200)
        self.assertEqual(data["message"], "Welcome to the API")
        self.assertEqual(data["version"], "1.0")

    def test_users_returns_valid_json(self):
        """GET /api/users should return valid JSON with users list."""
        status, data = self.make_request("/api/users")
        self.assertEqual(status, 200)
        self.assertIn("users", data)
        self.assertEqual(data["count"], 3)
        self.assertEqual(data["users"][0]["name"], "Alice")

    def test_health_returns_valid_json(self):
        """GET /health should return valid JSON with status."""
        status, data = self.make_request("/health")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "healthy")

    def test_echo_returns_valid_json(self):
        """POST /api/echo should return valid JSON echoing the input."""
        payload = json.dumps({"test": "data", "number": 42})
        status, data = self.make_request("/api/echo", method="POST", body=payload)
        self.assertEqual(status, 200)
        self.assertEqual(data["echo"]["test"], "data")
        self.assertEqual(data["echo"]["number"], 42)


if __name__ == "__main__":
    unittest.main()
