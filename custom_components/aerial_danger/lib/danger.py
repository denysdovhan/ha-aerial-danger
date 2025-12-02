"""
Danger detection library for the Aerial Danger integration.

The detector expands phrase templates against user-provided area regexes,
compiles them once, and provides per-danger detection helpers plus a composite
`danger` check. Matching is case-insensitive and returns only the first hit to
keep processing predictable for downstream sensors.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from .keywords import (
    BALLISTIC_DANGER,
    CRUISE_DANGER,
    DRONE_DANGER,
    GENERIC_DANGER,
)

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

RE_FLAGS = re.IGNORECASE | re.UNICODE
AREA_PLACEHOLDER = "{area}"


class DangerType(str, Enum):
    """Enum of supported aerial danger types."""

    BALLISTIC = "ballistic"
    CRUISE = "cruise"
    DRONE = "drone"
    GENERIC = "generic"


@dataclass
class Detection:
    """Represents a detected aerial danger."""

    danger: bool
    message: str
    type: DangerType | None = None
    area: str | None = None
    match: str | None = None


def map_areas(phrases: Sequence[str], areas: Sequence[str]) -> list[str]:
    expanded: list[str] = []
    for phrase in phrases:
        if AREA_PLACEHOLDER in phrase:
            expanded.extend(phrase.replace(AREA_PLACEHOLDER, area) for area in areas)
        else:
            expanded.append(phrase)
    return expanded


def compile_patterns(phrases: Sequence[str]) -> list[re.Pattern[str]]:
    return [re.compile(phrase, RE_FLAGS) for phrase in phrases]


def find_area(message: str, areas: Sequence[str]) -> str | None:
    for area in areas:
        if re.search(area, message, RE_FLAGS):
            return area
    return None


def match_first(patterns: Sequence[re.Pattern[str]], message: str) -> str | None:
    for pattern in patterns:
        match = pattern.search(message)
        if match:
            return match.group(0)
    return None


class DangerDetector:
    """Detects aerial danger types in messages using area-based regex patterns."""

    def __init__(self, cities: Iterable[str], neighborhoods: Iterable[str]) -> None:
        """Initialize detector with city and neighborhood regexes."""
        self._cities = list(cities)
        self._neighborhoods = list(neighborhoods)

        self._ballistic_patterns = compile_patterns(
            map_areas(BALLISTIC_DANGER, self._cities + self._neighborhoods)
        )
        self._cruise_patterns = compile_patterns(
            map_areas(CRUISE_DANGER, self._cities + self._neighborhoods)
        )
        self._drone_patterns = compile_patterns(
            map_areas(DRONE_DANGER, self._neighborhoods)
        )
        self._generic_patterns = compile_patterns(
            map_areas(GENERIC_DANGER, self._cities + self._neighborhoods)
        )

    def ballistic_danger(self, message: str) -> Detection:
        """Detect ballistic danger; returns first match or a negative detection."""
        normalized = message.lower()
        match = match_first(self._ballistic_patterns, normalized)
        if not match:
            return Detection(danger=False, message=message)

        area = find_area(normalized, self._cities + self._neighborhoods)
        if not area:
            return Detection(danger=False, message=message)
        return Detection(
            danger=True,
            type=DangerType.BALLISTIC,
            area=area,
            match=match,
            message=message,
        )

    def cruise_missile_danger(self, message: str) -> Detection:
        """Detect cruise-missile danger; returns first match or a negative detection."""
        normalized = message.lower()
        match = match_first(self._cruise_patterns, normalized)
        if not match:
            return Detection(danger=False, message=message)

        area = find_area(normalized, self._cities + self._neighborhoods)
        if not area:
             return Detection(danger=False, message=message)
        return Detection(
            danger=True,
            type=DangerType.CRUISE,
            area=area,
            match=match,
            message=message,
        )

    def drone_danger(self, message: str) -> Detection:
        """Detect drone danger; returns first match or a negative detection."""
        normalized = message.lower()
        match = match_first(self._drone_patterns, normalized)
        if not match:
            return Detection(danger=False, message=message)

        area = find_area(normalized, self._neighborhoods)
        if not area:
            return Detection(danger=False, message=message)
        return Detection(
            danger=True,
            type=DangerType.DRONE,
            area=area,
            match=match,
            message=message,
        )

    def generic_danger(self, message: str) -> Detection:
        """Detect generic danger linked to any provided area."""
        normalized = message.lower()
        match = match_first(self._generic_patterns, normalized)
        if not match:
            return Detection(danger=False, message=message)

        area = find_area(normalized, self._cities + self._neighborhoods)
        if not area:
            return Detection(danger=False, message=message)
        return Detection(
            danger=True,
            type=DangerType.GENERIC,
            area=area,
            match=match,
            message=message,
        )

    def danger(self, message: str) -> Detection:
        """Composite detector: ballistic → cruise → drone → generic; first hit wins."""
        for checker in (
            self.ballistic_danger,
            self.cruise_missile_danger,
            self.drone_danger,
            self.generic_danger,
        ):
            detection = checker(message)
            if detection.danger:
                return detection
        return Detection(danger=False, message=message)


__all__ = [
    "DangerDetector",
    "DangerType",
    "Detection",
]
