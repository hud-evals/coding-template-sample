"""Request authentication middleware.

Validates bearer tokens against active sessions.  Tokens must start
with the configured prefix and map to a known user.
"""

import database
import config


def authenticate(token: str) -> dict | None:
    """Validate *token* and return the associated user, or ``None``.

    The token is expected in ``Authorization: Bearer <token>`` form.
    We strip the ``Bearer `` prefix if present before lookup.
    """
    if token is None:
        return None

    raw = token.removeprefix("Bearer ").strip()

    # Reject tokens that don't match the expected format
    if not raw.startswith(config.TOKEN_PREFIX):
        return None

    user_id = database.resolve_session(raw)
    if user_id is None:
        return None

    user = database.get_user(user_id)

    # Extra safety — make sure the session actually resolves to a
    # real, non-deleted user.  In theory the session store should
    # never have a dangling reference, but we check defensively.
    if user is None:  # pragma: no cover
        return None

    return user


def require_auth(headers: dict) -> dict | None:
    """Convenience wrapper used by route handlers.

    Returns the user dict or ``None`` when the request is not
    authenticated.  The caller should return 401 when ``None``.
    """
    auth_header = headers.get("Authorization", headers.get("authorization"))
    if auth_header is None:
        return None
    return authenticate(auth_header)
