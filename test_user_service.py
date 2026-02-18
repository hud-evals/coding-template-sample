"""Tests for user_service module."""

import pytest
from user_service import get_user_profile, list_users


TEST_DB = {
    "1": {"name": "Alice", "email": "alice@example.com", "profile": {"display_name": "Alice A.", "bio": "Engineer"}},
    "2": {"name": "Bob", "email": "bob@example.com", "profile": None},
    "3": {"name": "Charlie", "email": "charlie@example.com"},
}


class TestGetUserProfile:
    def test_user_with_profile(self):
        result = get_user_profile("1", TEST_DB)
        assert result["name"] == "Alice A."
        assert result["email"] == "alice@example.com"
        assert result["bio"] == "Engineer"

    def test_user_with_none_profile(self):
        result = get_user_profile("2", TEST_DB)
        assert result["name"] == "Bob"
        assert result["email"] == "bob@example.com"
        assert result["bio"] == ""

    def test_user_without_profile_key(self):
        result = get_user_profile("3", TEST_DB)
        assert result["name"] == "Charlie"
        assert result["email"] == "charlie@example.com"
        assert result["bio"] == ""

    def test_user_not_found(self):
        with pytest.raises(ValueError, match="not found"):
            get_user_profile("999", TEST_DB)


class TestListUsers:
    def test_lists_all_users(self):
        result = list_users(TEST_DB)
        assert len(result) == 3
        names = {u["name"] for u in result}
        assert names == {"Alice", "Bob", "Charlie"}
