"""User profile service.

Provides helpers for retrieving and formatting user profile data
from the in-memory user store.
"""

USERS_DB = {
    "1": {"name": "Alice", "email": "alice@example.com", "profile": {"display_name": "Alice A.", "bio": "Engineer"}},
    "2": {"name": "Bob", "email": "bob@example.com", "profile": {"display_name": "Bob B.", "bio": "Designer"}},
    "3": {"name": "Charlie", "email": "charlie@example.com", "profile": None},
    "4": {"name": "Diana", "email": "diana@example.com"},
}


def get_user_profile(user_id, users_db=None):
    """Return formatted profile dict for a user.

    Args:
        user_id: The user ID to look up.
        users_db: Optional user database dict. Defaults to USERS_DB.

    Returns:
        dict with 'name', 'email', and 'bio' keys.

    Raises:
        ValueError: If the user ID is not found.
    """
    if users_db is None:
        users_db = USERS_DB

    user = users_db.get(str(user_id))
    if not user:
        raise ValueError(f"User {user_id} not found")

    profile = user.get("profile")
    if profile:
        name = profile["display_name"]
        bio = profile.get("bio", "")
    else:
        name = user.get("name", "Unknown")
        bio = ""

    return {
        "name": name,
        "email": user["email"],
        "bio": bio,
    }


def list_users(users_db=None):
    """Return a list of all user summaries.

    Args:
        users_db: Optional user database dict. Defaults to USERS_DB.

    Returns:
        List of dicts with 'id', 'name', and 'email' keys.
    """
    if users_db is None:
        users_db = USERS_DB

    return [
        {"id": uid, "name": u["name"], "email": u["email"]}
        for uid, u in users_db.items()
    ]
