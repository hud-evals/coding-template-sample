"""Application configuration and default settings.

Central configuration for TaskApp user settings API.
Default values are applied when a user has no custom override.
"""

APP_NAME = "TaskApp Settings API"
APP_VERSION = "3.2.1"
HOST = "0.0.0.0"
PORT = 8080

# Default settings applied to all users unless overridden.
# notification_frequency: 0=never, 1=daily, 7=weekly, 30=monthly
DEFAULT_SETTINGS = {
    "notification_frequency": 1,
    "dark_mode": True,
    "theme": "default",
    "bio": "Hey there! I'm using TaskApp.",
    "email_digest": True,
    "timezone": "UTC",
}

VALID_THEMES = [
    "default", "ocean", "midnight", "sunset", "forest", "arctic",
]

VALID_FREQUENCIES = [0, 1, 7, 30]

VALID_TIMEZONES = [
    "UTC", "America/New_York", "America/Chicago",
    "America/Denver", "America/Los_Angeles",
    "Europe/London", "Europe/Berlin", "Asia/Tokyo",
]

# Cache configuration — disabled after Issue #15 (stale cache on write-through)
CACHE_ENABLED = False
CACHE_TTL = 300  # seconds

# Rate limiting
RATE_LIMIT = 100       # requests per minute
RATE_WINDOW = 60       # window in seconds

# Auth
SESSION_DURATION = 3600  # 1 hour
TOKEN_PREFIX = "tsk_"
