import sys, os, copy
sys.path.insert(0, os.path.dirname(__file__))

from services.notification_builder import build_notification
from templates import _ROUTING


class TestNotificationBuilder:

    def setup_method(self):
        self._saved = copy.deepcopy(_ROUTING)

    def teardown_method(self):
        for k in list(_ROUTING.keys()):
            _ROUTING[k] = self._saved[k]

    def test_basic(self):
        n = build_notification("task.assigned", "alice@example.com", {"task_id": "T-1"})
        assert n is not None
        assert n["recipient"] == "alice@example.com"
        assert "email" in n["channels"]

    def test_extra_channels(self):
        n = build_notification("task.assigned", "a@ex.com", {}, extra_channels=["slack"])
        assert "slack" in n["channels"]
        assert "email" in n["channels"]

    def test_independent_notifications(self):
        build_notification("task.assigned", "a@ex.com", {}, extra_channels=["slack"])
        n2 = build_notification("task.assigned", "b@ex.com", {})
        assert n2["channels"] == ["email"], f"Expected ['email'], got {n2['channels']}"

    def test_routing_unchanged(self):
        orig = list(_ROUTING["task.assigned"]["channels"])
        build_notification("task.assigned", "a@ex.com", {}, extra_channels=["slack", "push"])
        assert _ROUTING["task.assigned"]["channels"] == orig, f"Routing mutated: {_ROUTING['task.assigned']['channels']}"

    def test_cross_type_independent(self):
        build_notification("task.assigned", "a@ex.com", {}, extra_channels=["slack"])
        n2 = build_notification("task.completed", "b@ex.com", {})
        assert n2["channels"] == ["email"], f"Expected ['email'], got {n2['channels']}"
