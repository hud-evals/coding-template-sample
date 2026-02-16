"""Settings cache layer.

Provides a TTL-based cache in front of the database to avoid
redundant reads.  Currently **disabled** via ``config.CACHE_ENABLED``
after we hit staleness issues in Issue #15.  The code is kept around
so we can re-enable it once we add proper invalidation.
"""

import time
import config

# TODO: invalidate on settings update — root cause of Issue #15
_cache: dict[str, tuple[float, dict]] = {}


def get(user_id: str) -> dict | None:
    """Return cached settings if fresh, else ``None``."""
    if not config.CACHE_ENABLED:
        return None

    entry = _cache.get(user_id)
    if entry is None:
        return None

    stored_at, data = entry
    if time.time() - stored_at > config.CACHE_TTL:
        # Stale — evict and return miss
        del _cache[user_id]
        return None

    return data


def put(user_id: str, data: dict) -> None:
    """Store *data* in the cache for *user_id*."""
    if not config.CACHE_ENABLED:
        return
    _cache[user_id] = (time.time(), data)


def invalidate(user_id: str) -> None:
    """Remove a single user's cached entry."""
    _cache.pop(user_id, None)


def clear():
    """Flush the entire cache (used in tests)."""
    _cache.clear()
