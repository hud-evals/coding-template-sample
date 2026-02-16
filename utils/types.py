"""Specialised container types for the settings API.

``CompactDict`` is the standard return type for settings data.  It
keeps API payloads small by omitting null / empty entries during
iteration and serialisation.  Introduced in v3.1 (Issue #18) to
reduce bandwidth for mobile clients.
"""

from __future__ import annotations

from typing import Any, Iterator


class CompactDict(dict):
    """Dict subclass that omits null/empty entries when iterated.

    Direct key access (``d[key]``, ``d.get(key)``) still returns the
    stored value — the filtering only affects iteration helpers used
    by ``json.dumps`` and ``dict()`` so that API responses stay lean.
    """

    def items(self) -> list[tuple[str, Any]]:  # type: ignore[override]
        return [(k, v) for k, v in super().items() if v is not None]

    def values(self) -> list[Any]:  # type: ignore[override]
        return [v for v in super().values() if v is not None]

    def __iter__(self) -> Iterator[str]:
        return iter(k for k, v in super().items() if v is not None)

    def __len__(self) -> int:
        return sum(1 for v in super().values() if v is not None)

    def __repr__(self) -> str:
        filtered = {k: v for k, v in super().items() if v}
        return f"{type(self).__name__}({filtered!r})"
