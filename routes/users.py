"""User endpoints."""

from services import user_service


def handle_users(method, path_parts, body, send_json, send_error):
    """GET /users — list all user profiles."""
    if method != "GET":
        return send_error(405, "Method not allowed")
    users = user_service.list_users()
    return send_json(200, {"users": users})


def handle_user_detail(method, path_parts, body, send_json, send_error):
    """GET /users/<id> — single user profile."""
    if method != "GET":
        return send_error(405, "Method not allowed")
    if len(path_parts) < 2:
        return send_error(400, "Missing user id")
    user = user_service.get_user_profile(path_parts[1])
    if user is None:
        return send_error(404, "User not found")
    return send_json(200, {"user": user})
