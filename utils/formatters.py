"""Display formatting utilities.

Converts raw setting values into human-readable representations
for UI display and notification templates.
"""

_FREQUENCY_LABELS = {
    0: "Never",
    1: "Daily",
    7: "Weekly",
    30: "Monthly",
}


def format_frequency(value: int) -> str:
    """Map a numeric notification_frequency to a label."""
    return _FREQUENCY_LABELS.get(value, f"Every {value} days")


def format_bool_setting(value: bool) -> str:
    """Return 'Enabled' / 'Disabled' for boolean settings."""
    return "Enabled" if value else "Disabled"


def format_settings_for_display(settings: dict) -> dict:
    """Produce a human-friendly version of a settings dict.

    This is used in email templates and the web dashboard.
    The raw values must already be resolved before calling this
    function; it only handles presentation.
    """
    display = {}
    for key, value in settings.items():
        if key == "notification_frequency":
            display[key] = format_frequency(value)
        elif key in ("dark_mode", "email_digest"):
            display[key] = format_bool_setting(value)
        else:
            display[key] = str(value)
    return display
