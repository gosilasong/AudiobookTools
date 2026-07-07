from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Merger:
    """
    Merge audiobook chapters into audiobook volumes.

    The actual merge implementation will be added in a later milestone.
    """

    hours_per_volume: float = 2.0
