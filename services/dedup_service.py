"""Event deduplication service."""

import hashlib
import time
from config import DEDUP_CONFIG


_seen = {}


def _extract_field(data, dotted_key):
    """Traverse *data* using a dot-separated key path.

    Parameters
    ----------
    data : dict
    dotted_key : str

    Returns
    -------
    str
    """
    parts = dotted_key.split(".")
    current = data
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return ""
    return str(current) if current is not None else ""


def _compute_fingerprint(event):
    """Derive a dedup fingerprint from configured fields.

    Parameters
    ----------
    event : dict

    Returns
    -------
    str
    """
    fields = DEDUP_CONFIG.get("hash_fields", [])
    parts = []
    for field in fields:
        parts.append(_extract_field(event, field))
    raw = "|".join(parts)
    return hashlib.md5(raw.encode()).hexdigest()


def is_duplicate(event):
    """Check whether *event* has been seen within the dedup window.

    Parameters
    ----------
    event : dict

    Returns
    -------
    bool
    """
    window = DEDUP_CONFIG.get("window_seconds", 300)
    _prune_expired(window)

    fingerprint = _compute_fingerprint(event)
    if fingerprint in _seen:
        return True

    _seen[fingerprint] = time.time()
    return False


def _prune_expired(window_seconds):
    """Remove fingerprints older than *window_seconds*.

    Parameters
    ----------
    window_seconds : int
    """
    cutoff = time.time() - window_seconds
    expired = [fp for fp, ts in _seen.items() if ts < cutoff]
    for fp in expired:
        del _seen[fp]


def clear():
    """Reset all dedup state."""
    _seen.clear()
