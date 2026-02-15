"""
Application configuration and default settings.

Default values are applied for any setting a user hasn't explicitly configured.
See the settings pipeline refactor (Issue #22) for migration notes.
"""

APP_NAME = "SettingsAPI"
APP_VERSION = "3.2.0"
HOST = "0.0.0.0"
PORT = 8000

# Default user settings — applied when a setting hasn't been explicitly set.
# Updated in the settings pipeline refactor (Issue #22).
DEFAULT_SETTINGS = {
    "notification_frequency": 1,   # 0=never, 1=daily, 7=weekly, 30=monthly
    "dark_mode": True,
    "theme": "default",
    "bio": "Hey there! I'm using TaskApp.",
    "email_digest": True,
    "timezone": "UTC",
}

# Valid values for constrained settings
VALID_FREQUENCIES = [0, 1, 7, 30]
VALID_THEMES = ["default", "midnight", "ocean", "forest"]
VALID_TIMEZONES = [
    "UTC", "America/New_York", "America/Chicago",
    "America/Denver", "America/Los_Angeles",
    "Europe/London", "Europe/Berlin", "Asia/Tokyo",
]

MAX_BIO_LENGTH = 200
