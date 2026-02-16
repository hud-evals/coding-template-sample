"""Sliding-window rate limiter for notification delivery."""

import time
from config import PLAN_TIERS


_buckets = {}


def _get_bucket(recipient):
    """Return the event-timestamp list for *recipient*.

    Parameters
    ----------
    recipient : str

    Returns
    -------
    list[float]
    """
    if recipient not in _buckets:
        _buckets[recipient] = []
    return _buckets[recipient]


def _prune_bucket(bucket, window_seconds=60):
    """Remove entries older than *window_seconds* from *bucket*.

    Parameters
    ----------
    bucket : list[float]
    window_seconds : int

    Returns
    -------
    list[float]
    """
    cutoff = time.time() - window_seconds
    return [ts for ts in bucket if ts > cutoff]


def check_rate_limit(recipient, plan_tier="free"):
    """Determine whether *recipient* has exceeded their rate limit.

    Parameters
    ----------
    recipient : str
    plan_tier : str

    Returns
    -------
    tuple[bool, dict]
        ``(allowed, info)`` where *allowed* is ``True`` when the
        request may proceed.
    """
    tier = PLAN_TIERS.get(plan_tier, PLAN_TIERS["free"])
    limit = tier.get("rate_limit")
    if limit is None:
        return True, {"limit": None, "remaining": None}

    bucket = _get_bucket(recipient)
    bucket[:] = _prune_bucket(bucket)
    current = len(bucket)

    if current >= limit:
        return False, {
            "limit": limit,
            "remaining": 0,
            "retry_after_seconds": 60,
        }

    return True, {
        "limit": limit,
        "remaining": limit - current,
    }


def record_event(recipient):
    """Record a delivery event for *recipient*.

    Parameters
    ----------
    recipient : str
    """
    bucket = _get_bucket(recipient)
    bucket.append(time.time())


def reset(recipient=None):
    """Clear rate-limit state.

    Parameters
    ----------
    recipient : str or None
        If ``None``, clears all state.
    """
    if recipient is None:
        _buckets.clear()
    else:
        _buckets.pop(recipient, None)
