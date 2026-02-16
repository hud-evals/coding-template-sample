"""Settings endpoints."""

import json
from services import settings_service
from services import audit_service
from utils.validators import validate_settings
from utils.permissions import can_modify


def handle_settings(method, path_parts, body, send_json, send_error):
    """GET/PUT /settings/<user_id>"""
    if len(path_parts) < 2:
        return send_error(400, "Missing user id")

    user_id = path_parts[1]

    if method == "GET":
        settings = settings_service.get_effective_settings(user_id)
        if settings is None:
            return send_error(404, "User not found")
        return send_json(200, {"user_id": user_id, "settings": settings})

    if method == "PUT":
        if not body:
            return send_error(400, "Request body required")

        try:
            updates = json.loads(body) if isinstance(body, str) else body
        except (json.JSONDecodeError, TypeError):
            return send_error(400, "Invalid JSON")

        valid, errors = validate_settings(updates)
        if errors:
            return send_error(422, "; ".join(errors))

        before = settings_service.get_effective_settings(user_id)
        result = settings_service.update_settings(user_id, valid)
        if result is None:
            return send_error(404, "User not found")

        audit_service.record_change(user_id, before, result)
        return send_json(200, {"user_id": user_id, "settings": result})

    return send_error(405, "Method not allowed")


def handle_setting_key(method, path_parts, body, send_json, send_error):
    """GET /settings/key/<user_id>/<key>"""
    if method != "GET":
        return send_error(405, "Method not allowed")
    if len(path_parts) < 4:
        return send_error(400, "Missing user id or key")

    user_id = path_parts[2]
    key = path_parts[3]
    value = settings_service.get_single_setting(user_id, key)
    if value is None:
        return send_error(404, "Setting not found")
    return send_json(200, {"user_id": user_id, "key": key, "value": value})
