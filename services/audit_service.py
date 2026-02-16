"""Audit logging for settings changes.

Records before/after snapshots so we can answer "who changed what and when".
"""

import copy
import time
from models import AuditEntry

_log: list[AuditEntry] = []


def record_change(user_id: str, before: dict | None, after: dict | None) -> None:
    """Append an audit entry.  Uses deep copies to avoid aliasing."""
    entry = AuditEntry(
        user_id=user_id,
        action="settings_update",
        before=copy.deepcopy(before),
        after=copy.deepcopy(after),
        timestamp=time.time(),
    )
    _log.append(entry)


def get_history(user_id: str) -> list[dict]:
    """Return the audit trail for *user_id* (newest first)."""
    entries = [e for e in _log if e.user_id == user_id]
    entries.sort(key=lambda e: e.timestamp, reverse=True)
    return [
        {
            "action": e.action,
            "before": e.before,
            "after": e.after,
            "timestamp": e.timestamp,
        }
        for e in entries
    ]


def clear():
    """Reset the audit log (used in tests)."""
    _log.clear()
