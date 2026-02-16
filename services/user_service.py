"""User CRUD operations."""

import database


def get_user(user_id: str) -> dict | None:
    """Return the full user record or ``None``."""
    return database.get_user(user_id)


def get_user_profile(user_id: str) -> dict | None:
    """Return a public-facing profile (no raw settings blob)."""
    user = database.get_user(user_id)
    if user is None:
        return None
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "tier": user["tier"],
    }


def list_users() -> list[dict]:
    """Return all user profiles."""
    return [
        {"id": u["id"], "name": u["name"], "email": u["email"], "tier": u["tier"]}
        for u in database.get_all_users()
    ]
