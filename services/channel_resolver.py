"""Channel resolution service."""

from config import CHANNEL_REGISTRY, PLAN_TIERS
from templates import get_channels, get_priority


def _is_channel_active(channel_name):
    """Check whether *channel_name* is enabled in the channel registry."""
    entry = CHANNEL_REGISTRY.get(channel_name)
    if entry is None:
        return False
    return entry.get("enabled", False)


def _apply_plan_limits(channels, plan_tier):
    """Enforce plan-tier channel limits.

    Parameters
    ----------
    channels : list[str]
    plan_tier : str

    Returns
    -------
    list[str]
    """
    tier = PLAN_TIERS.get(plan_tier)
    if tier is None:
        return channels
    max_ch = tier.get("max_channels")
    if max_ch is None:
        return channels
    if len(channels) <= max_ch:
        return channels
    return channels[:max_ch]


def _filter_disabled(channels):
    """Remove any channels that are disabled in the registry.

    Parameters
    ----------
    channels : list[str]

    Returns
    -------
    list[str]
    """
    disabled = [ch for ch in channels if not _is_channel_active(ch)]
    if not disabled:
        return channels
    return [ch for ch in channels if _is_channel_active(ch)]


def resolve_channels(event_type, plan_tier="enterprise"):
    """Resolve the effective channel list for a given event type.

    Parameters
    ----------
    event_type : str
    plan_tier : str

    Returns
    -------
    list[str]
    """
    base_channels = get_channels(event_type)
    filtered = _filter_disabled(base_channels)
    limited = _apply_plan_limits(filtered, plan_tier)
    return limited


def resolve_priority(event_type):
    """Return the resolved priority string for *event_type*.

    Parameters
    ----------
    event_type : str

    Returns
    -------
    str
    """
    return get_priority(event_type)
