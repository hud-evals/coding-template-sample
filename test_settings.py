"""Tests for the user settings pipeline.

Validates that user settings — including valid falsy values like 0, False,
and empty string — are correctly preserved through the full read path.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import database
from services import settings_service, notification_service


class TestSettingsReadPath:
    """Verify get_effective_settings returns correct stored values."""

    def test_alice_notification_frequency_zero(self):
        """Alice set notification_frequency to 0 (never). Must stay 0."""
        settings = settings_service.get_effective_settings("user-alice")
        assert settings is not None
        assert settings.get("notification_frequency") == 0, (
            f"Alice set notification_frequency to 0 (never), "
            f"but got {settings.get('notification_frequency')}"
        )

    def test_alice_dark_mode_false(self):
        """Alice explicitly disabled dark mode. Must stay False."""
        settings = settings_service.get_effective_settings("user-alice")
        assert "dark_mode" in settings, "dark_mode key missing from response"
        assert settings["dark_mode"] is False, (
            f"Alice disabled dark_mode, but got {settings.get('dark_mode')}"
        )

    def test_charlie_empty_bio(self):
        """Charlie intentionally cleared his bio. Must stay empty."""
        settings = settings_service.get_effective_settings("user-charlie")
        assert settings is not None
        assert "bio" in settings, "bio key missing from response"
        assert settings["bio"] == "", (
            f"Charlie set bio to empty string, but got {settings.get('bio')!r}"
        )

    def test_truthy_values_preserved(self):
        """Truthy custom values must work correctly."""
        settings = settings_service.get_effective_settings("user-charlie")
        assert settings["theme"] == "midnight"

    def test_bob_gets_defaults(self):
        """Bob has no custom settings — should get all defaults."""
        settings = settings_service.get_effective_settings("user-bob")
        assert settings is not None
        assert settings.get("notification_frequency") == 1
        assert settings.get("dark_mode") is True


class TestNotificationCascade:
    """Verify notification decisions respect stored settings."""

    def test_alice_should_not_be_notified(self):
        """Alice set notification_frequency to 0 — should NOT be notified."""
        result = notification_service.should_notify("user-alice")
        assert result is False, (
            "Alice opted out (frequency=0) but should_notify returned True"
        )

    def test_bob_should_be_notified(self):
        """Bob uses defaults (frequency=1) — should be notified."""
        result = notification_service.should_notify("user-bob")
        assert result is True


class TestWriteReadCycle:
    """Verify writing a falsy value and reading it back works."""

    def setup_method(self):
        self._original_bob = dict(database.get_user_settings("user-bob") or {})

    def teardown_method(self):
        database.update_user_settings("user-bob", self._original_bob)

    def test_write_zero_then_read(self):
        """Write notification_frequency=0, read back, must get 0."""
        database.update_user_settings("user-bob", {"notification_frequency": 0})
        settings = settings_service.get_effective_settings("user-bob")
        assert settings.get("notification_frequency") == 0, (
            f"Wrote 0, got back {settings.get('notification_frequency')}"
        )

    def test_write_false_then_read(self):
        """Write dark_mode=False, read back, must get False."""
        database.update_user_settings("user-bob", {"dark_mode": False})
        settings = settings_service.get_effective_settings("user-bob")
        assert "dark_mode" in settings, "dark_mode key missing after write"
        assert settings["dark_mode"] is False, (
            f"Wrote False, got back {settings.get('dark_mode')}"
        )
