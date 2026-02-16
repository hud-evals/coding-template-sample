"""User notification preference lookups."""

from config import CHANNEL_DEFAULTS, PLAN_TIERS

_preference_store = {}


def register_preferences(user_id, preferences):
    """Store notification preferences for *user_id*.

    Parameters
    ----------
    user_id : str
    preferences : dict
    """
    _preference_store[user_id] = dict(preferences)


def get_user_plan(user_id):
    """Return the plan tier string for *user_id*.

    Parameters
    ----------
    user_id : str

    Returns
    -------
    str
    """
    prefs = _preference_store.get(user_id, {})
    return prefs.get("plan", "free")


def get_user_timezone(user_id):
    """Return the IANA timezone string for *user_id*.

    Parameters
    ----------
    user_id : str

    Returns
    -------
    str
    """
    prefs = _preference_store.get(user_id, {})
    return prefs.get("timezone", "UTC")


def get_quiet_hours(user_id):
    """Return (start_hour, end_hour) tuple or ``None``.

    Parameters
    ----------
    user_id : str

    Returns
    -------
    tuple[int, int] or None
    """
    prefs = _preference_store.get(user_id, {})
    quiet = prefs.get("quiet_hours")
    if quiet is None:
        return None
    return (quiet.get("start", 22), quiet.get("end", 7))


def get_fallback_channels(priority):
    """Return fallback channel list when routing yields nothing.

    Parameters
    ----------
    priority : str

    Returns
    -------
    list[str]
    """
    channels = CHANNEL_DEFAULTS.get(priority)
    if not channels:
        return ["email"]
    return channels


def is_channel_opted_out(user_id, channel):
    """Check whether *user_id* has opted out of *channel*.

    Parameters
    ----------
    user_id : str
    channel : str

    Returns
    -------
    bool
    """
    prefs = _preference_store.get(user_id, {})
    opt_outs = prefs.get("opted_out_channels", [])
    return channel in opt_outs


def get_max_channels_for_plan(plan_tier):
    """Return the channel limit for *plan_tier*.

    Parameters
    ----------
    plan_tier : str

    Returns
    -------
    int or None
    """
    tier = PLAN_TIERS.get(plan_tier)
    if tier is None:
        return 1
    return tier.get("max_channels")
