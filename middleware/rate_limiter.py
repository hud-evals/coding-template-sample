"""Simple in-memory rate limiter.

Tracks request counts per IP within a sliding window.
"""

import time
import config

_buckets: dict[str, list[float]] = {}


def is_rate_limited(client_ip: str) -> bool:
    """Return ``True`` if *client_ip* has exceeded the rate limit."""
    now = time.time()
    window_start = now - config.RATE_WINDOW

    hits = _buckets.setdefault(client_ip, [])

    # Prune expired entries
    _buckets[client_ip] = [t for t in hits if t > window_start]
    hits = _buckets[client_ip]

    if len(hits) >= config.RATE_LIMIT:
        return True

    hits.append(now)
    return False


def reset():
    """Clear all rate-limit state (used in tests)."""
    _buckets.clear()
