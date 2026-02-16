"""Webhook notification processing API."""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler

from config import APP_CONFIG
from routes.webhooks import handle_webhook_routes


class WebhookRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for webhook endpoints."""

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON body"})
            return

        status, response = handle_webhook_routes(self.path, "POST", data)
        self._send_json(status, response)

    def do_GET(self):
        status, response = handle_webhook_routes(self.path, "GET", None)
        self._send_json(status, response)

    def _send_json(self, status_code, payload):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload, default=str).encode())

    def log_message(self, format, *args):
        pass


def run_server():
    """Start the HTTP server."""
    host = APP_CONFIG["host"]
    port = APP_CONFIG["port"]
    server = HTTPServer((host, port), WebhookRequestHandler)
    print(f"Webhook API listening on {host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == "__main__":
    run_server()
