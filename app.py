"""TaskApp Settings API — HTTP server.

A lightweight settings management service built on ``http.server``.
Routes are registered in ``routes/__init__.py`` and dispatched here.
All JSON responses pass through the response middleware pipeline
for consistent payload formatting (Issue #18).
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler

import config
from middleware.response import sanitize_payload
from middleware.rate_limiter import is_rate_limited
from routes import ROUTES


def json_response(handler, status: int, data):
    """Send a JSON response, applying payload sanitisation (Issue #18)."""
    clean = sanitize_payload(data)
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(json.dumps(clean).encode())


def error_response(handler, status: int, message: str):
    """Send a JSON error envelope."""
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(json.dumps({"error": message}).encode())


class RequestHandler(BaseHTTPRequestHandler):
    """Dispatch incoming requests to the matching route handler."""

    def _dispatch(self, method: str):
        client_ip = self.client_address[0]
        if is_rate_limited(client_ip):
            return error_response(self, 429, "Rate limit exceeded")

        path = self.path.rstrip("/")
        parts = [p for p in path.split("/") if p]

        body = None
        length = int(self.headers.get("Content-Length", 0))
        if length:
            body = self.rfile.read(length).decode()

        # Match route by prefix
        for route_prefix, handler_fn in ROUTES.items():
            route_key = route_prefix.rstrip("/")
            route_parts = [p for p in route_key.split("/") if p]
            if parts[:len(route_parts)] == route_parts:
                return handler_fn(
                    method,
                    parts,
                    body,
                    lambda s, d: json_response(self, s, d),
                    lambda s, m: error_response(self, s, m),
                )

        error_response(self, 404, "Not found")

    def do_GET(self):
        self._dispatch("GET")

    def do_PUT(self):
        self._dispatch("PUT")

    def do_POST(self):
        self._dispatch("POST")

    def log_message(self, format, *args):
        pass  # Silence request logs during tests


def create_app() -> HTTPServer:
    """Build and return the HTTP server (does not start it)."""
    return HTTPServer((config.HOST, config.PORT), RequestHandler)


if __name__ == "__main__":
    server = create_app()
    print(f"{config.APP_NAME} listening on {config.HOST}:{config.PORT}")
    server.serve_forever()
