"""Simple HTTP server with JSON API endpoints."""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class APIHandler(BaseHTTPRequestHandler):
    """Handle HTTP requests for the API."""

    def _send_response(self, status_code, content_type, body):
        """Send an HTTP response."""
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def _send_json(self, data, status_code=200):
        """Send a JSON response."""
        body = str(data)
        self._send_response(status_code, "application/json", body)

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path == "/":
            self._send_json({"message": "Welcome to the API", "version": "1.0"})

        elif path == "/api/users":
            users = [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
                {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
            ]
            self._send_json({"users": users, "count": len(users)})

        elif path == "/api/user":
            user_id = query.get("id", [None])[0]
            if user_id is None:
                self._send_json({"error": "Missing user id"}, status_code=400)
                return

            users = {
                "1": {"id": 1, "name": "Alice", "email": "alice@example.com"},
                "2": {"id": 2, "name": "Bob", "email": "bob@example.com"},
                "3": {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
            }
            user = users.get(user_id)
            if user:
                self._send_json({"user": user})
            else:
                self._send_json({"error": "User not found"}, status_code=404)

        elif path == "/health":
            self._send_json({"status": "healthy"})

        else:
            self._send_json({"error": "Not found"}, status_code=404)

    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""

        if path == "/api/echo":
            try:
                data = json.loads(body) if body else {}
                self._send_json({"echo": data})
            except json.JSONDecodeError:
                self._send_json({"error": "Invalid JSON"}, status_code=400)

        elif path == "/api/user":
            try:
                data = json.loads(body) if body else {}
                name = data.get("name")
                email = data.get("email")

                if not name or not email:
                    self._send_json({"error": "Missing name or email"}, status_code=400)
                    return

                # Simulate creating a user
                new_user = {"id": 4, "name": name, "email": email}
                self._send_json({"user": new_user, "created": True}, status_code=201)

            except json.JSONDecodeError:
                self._send_json({"error": "Invalid JSON"}, status_code=400)

        else:
            self._send_json({"error": "Not found"}, status_code=404)

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def run_server(host="localhost", port=8000):
    """Run the HTTP server."""
    server = HTTPServer((host, port), APIHandler)
    print(f"Server running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
