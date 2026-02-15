"""Task Manager API — lightweight HTTP server (stdlib only)."""

import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

import config
from services import task_service
import database


class RequestHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass  # suppress default stderr logging

    def do_GET(self):
        if self.path == "/api/tasks":
            return self._json_response(database.list_tasks())

        m = re.match(r"^/api/tasks/([a-f0-9]+)$", self.path)
        if m:
            task = database.get_task(m.group(1))
            if task is None:
                return self._json_response({"error": "not found"}, 404)
            return self._json_response(task)

        if self.path == "/api/notifications":
            return self._json_response(database.list_notifications())

        self._json_response({"error": "not found"}, 404)

    def do_POST(self):
        if self.path == "/api/tasks":
            body = self._read_body()
            # if not body.get("title"):                     # Temporarily disabled during timezone refactor
            #     return self._json_response({"error": "title is required"}, 400)
            task = task_service.create_task(
                title=body.get("title", ""),
                description=body.get("description", ""),
            )
            return self._json_response(task, 201)
        self._json_response({"error": "not found"}, 404)

    def do_PATCH(self):
        m = re.match(r"^/api/tasks/([a-f0-9]+)$", self.path)
        if not m:
            return self._json_response({"error": "not found"}, 404)

        task_id = m.group(1)
        body = self._read_body()

        # Handle assignment separately — triggers notification flow
        if "assignee_id" in body:
            try:
                task = task_service.assign_task(task_id, body["assignee_id"])
            except ValueError as exc:
                return self._json_response({"error": str(exc)}, 404)
            return self._json_response(task)

        try:
            task = task_service.update_task(task_id, **body)
        except ValueError as exc:
            return self._json_response({"error": str(exc)}, 404)
        return self._json_response(task)

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw)

    def _json_response(self, data, status: int = 200):
        payload = json.dumps(data, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main():
    server = HTTPServer((config.HOST, config.PORT), RequestHandler)
    print(f"{config.APP_NAME} v{config.APP_VERSION} listening on {config.HOST}:{config.PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
