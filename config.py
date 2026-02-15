"""Application configuration.

Refactored as part of Issue #5 — timezone-aware datetime migration.
All naive datetime usage has been replaced with timezone-aware equivalents.
See also: database.py, task_service.py
"""

from datetime import datetime, timezone

# App metadata
APP_NAME = "TaskManager"
APP_VERSION = "1.4.2"

# Server
HOST = "0.0.0.0"
PORT = 8000

# Timezone configuration — updated in timezone refactor (Issue #5)
# Previously used local time; now all timestamps are UTC.
TIMEZONE = "UTC"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# Feature flags
NOTIFICATION_ENABLED = True
MAX_TASKS = 10_000


def get_timestamp() -> str:
    """Return the current UTC timestamp as an ISO-formatted string.

    Updated in timezone refactor (Issue #5) — previously used
    datetime.utcnow() which returns a naive datetime.
    """
    now = datetime.now(timezone.utc)  # Updated in timezone refactor (Issue #5)
    return now.strftime(DATE_FORMAT)
