"""
Lightweight HTTP server for the User Settings API.

Uses only the standard library (http.server + json) so the container
has zero external dependencies.
"""

from __future__ import annotations

import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any

import config
from services import settings_service, user_service, notification_service
from utils.validators import validate_settings
from utils.permissions import filter_allowed_updates


# ── Routing helpers ─────────────────────────────────────────────────

_ROUTE_USER       = re.compile(r"^/api/users/([^/]+)$")
_ROUTE_SETTINGS   = re.compile(r"^/api/users/([^/]+)/settings$")
_ROUTE_RESET      = re.compile(r"^/api/users/([^/]+)/settings/reset$")
_ROUTE_NOTIFY     = re.compile(r"^/api/notifications/pending$")
_ROUTE_USERS_LIST = re.compile(r"^/api/users$")


def _json_response(handler: BaseHTTPRequestHandler, status: int, body: Any) -> None:
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(json.dumps(body).encode())


def _read_body(handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    length = int(handler.headers.get("Content-Length", 0))
    raw = handler.rfile.read(length)
    return json.loads(raw) if raw else {}


# ── Request handler ─────────────────────────────────────────────────

class SettingsHandler(BaseHTTPRequestHandler):

    # ── GET ──────────────────────────────────────────────────────────

    def do_GET(self) -> None:
        # GET /api/users
        if _ROUTE_USERS_LIST.match(self.path):
            users = user_service.list_all_users()
            return _json_response(self, 200, users)

        # GET /api/users/{id}
        m = _ROUTE_USER.match(self.path)
        if m:
            profile = user_service.get_user_profile(m.group(1))
            if profile is None:
                return _json_response(self, 404, {"error": "user not found"})
            return _json_response(self, 200, profile)

        # GET /api/users/{id}/settings
        m = _ROUTE_SETTINGS.match(self.path)
        if m:
            effective = settings_service.get_effective_settings(m.group(1))
            if effective is None:
                return _json_response(self, 404, {"error": "user not found"})
            return _json_response(self, 200, effective)

        # GET /api/notifications/pending
        if _ROUTE_NOTIFY.match(self.path):
            pending = notification_service.get_pending_notifications()
            return _json_response(self, 200, pending)

        _json_response(self, 404, {"error": "not found"})

    # ── PATCH ────────────────────────────────────────────────────────

    def do_PATCH(self) -> None:
        # PATCH /api/users/{id}/settings
        m = _ROUTE_SETTINGS.match(self.path)
        if not m:
            return _json_response(self, 404, {"error": "not found"})

        user_id = m.group(1)
        body = _read_body(self)

        # Validate values
        ok, errors = validate_settings(body)
        if not ok:
            return _json_response(self, 400, {"errors": errors})

        # Enforce tier permissions
        allowed = filter_allowed_updates(user_id, body)

        success = settings_service.update_user_settings(user_id, allowed)
        if not success:
            return _json_response(self, 404, {"error": "user not found"})

        effective = settings_service.get_effective_settings(user_id)
        return _json_response(self, 200, effective)

    # ── POST ─────────────────────────────────────────────────────────

    def do_POST(self) -> None:
        # POST /api/users/{id}/settings/reset
        m = _ROUTE_RESET.match(self.path)
        if not m:
            return _json_response(self, 404, {"error": "not found"})

        user_id = m.group(1)
        body = _read_body(self)
        key = body.get("key")

        if not key or key not in config.DEFAULT_SETTINGS:
            return _json_response(self, 400, {"error": "invalid setting key"})

        success = settings_service.reset_setting(user_id, key)
        if not success:
            return _json_response(self, 404, {"error": "user not found"})

        effective = settings_service.get_effective_settings(user_id)
        return _json_response(self, 200, effective)

    # Silence default request logging
    def log_message(self, fmt: str, *args: Any) -> None:
        pass


# ── Entry point ─────────────────────────────────────────────────────

def main() -> None:
    server = HTTPServer((config.HOST, config.PORT), SettingsHandler)
    print(f"{config.APP_NAME} v{config.APP_VERSION} listening on {config.HOST}:{config.PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
