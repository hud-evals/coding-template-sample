"""Response sanitisation middleware.

Cleans up API responses by removing null/empty values for a cleaner
JSON contract.  Applied automatically to all outbound responses.
Introduced in v3.1 to reduce payload sizes (Issue #18).
"""


def sanitize_payload(data):
    """Recursively remove null/empty entries from response payloads.

    This keeps our JSON responses lean by stripping out fields that
    have no meaningful value.  Clients can treat missing keys as
    'use default' per our API contract (Issue #18).
    """
    if isinstance(data, dict):
        return {k: sanitize_payload(v) for k, v in data.items() if v is not None}
    if isinstance(data, list):
        return [sanitize_payload(item) for item in data]
    return data
