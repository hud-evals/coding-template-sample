"""Priority escalation and on-call routing."""

import time
from templates import get_actions, get_cooldown


_escalation_log = []

_ONCALL_SCHEDULE = {
    "default": "ops-team@example.com",
    "weekends": "weekend-oncall@example.com",
}


def should_escalate(event_type, event_data):
    """Determine whether *event_type* requires escalation.

    Parameters
    ----------
    event_type : str
    event_data : dict

    Returns
    -------
    bool
    """
    actions = get_actions(event_type)
    if "page_oncall" in actions:
        return True
    severity = event_data.get("severity")
    if severity and severity in ("critical", "p0"):
        return True
    return False


def get_escalation_targets(event_type, event_data):
    """Return a list of escalation targets for the event.

    Parameters
    ----------
    event_type : str
    event_data : dict

    Returns
    -------
    list[str]
    """
    if not should_escalate(event_type, event_data):
        return []

    targets = [_ONCALL_SCHEDULE["default"]]

    team = event_data.get("team")
    if team and team in _ONCALL_SCHEDULE:
        targets.append(_ONCALL_SCHEDULE[team])

    return targets


def record_escalation(event_id, targets):
    """Log an escalation event.

    Parameters
    ----------
    event_id : str
    targets : list[str]
    """
    _escalation_log.append({
        "event_id": event_id,
        "targets": list(targets),
        "escalated_at": time.time(),
    })


def check_cooldown(event_type, recipient):
    """Check whether *event_type* is in cooldown for *recipient*.

    Parameters
    ----------
    event_type : str
    recipient : str

    Returns
    -------
    bool
    """
    cooldown_minutes = get_cooldown(event_type)
    if cooldown_minutes <= 0:
        return False

    cutoff = time.time() - (cooldown_minutes * 60)
    for entry in reversed(_escalation_log):
        if entry.get("escalated_at", 0) < cutoff:
            break
        for target in entry.get("targets", []):
            if target == recipient:
                return True
    return False
