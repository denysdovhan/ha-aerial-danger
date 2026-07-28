"""Danger detection library for the Aerial Danger integration."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .keywords import (
    BALLISTIC_DANGER,
    CRUISE_DANGER,
    DRONE_DANGER,
    GENERIC_DANGER,
    IRBM_DANGER,
    SAFETY,
)
from .models import DangerType, Detection, PatternMatch

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

RE_FLAGS = re.IGNORECASE | re.UNICODE
AREA_PLACEHOLDER = "{area}"


class DangerDetector:
    """Detects aerial danger types in messages using area-based regex patterns."""

    @staticmethod
    def validate_patterns(*pattern_groups: Iterable[str]) -> None:
        """Compile configured regex patterns."""
        for patterns in pattern_groups:
            for pattern in patterns:
                re.compile(pattern, RE_FLAGS)

    def __init__(self, regions: Iterable[str], localities: Iterable[str]) -> None:
        """Initialize detector with region and locality regexes."""
        self._regions = list(regions)
        self._localities = list(localities)
        self._safety_patterns = self.compile_patterns(SAFETY)

        self._ballistic_patterns = self.compile_patterns(
            self.map_areas(BALLISTIC_DANGER, self._regions + self._localities)
        )
        self._irbm_patterns = self.compile_patterns(IRBM_DANGER)
        self._cruise_patterns = self.compile_patterns(
            self.map_areas(CRUISE_DANGER, self._regions + self._localities)
        )
        self._drone_patterns = self.compile_patterns(
            self.map_areas(DRONE_DANGER, self._localities)
        )
        self._generic_patterns = self.compile_patterns(
            self.map_areas(GENERIC_DANGER, self._regions + self._localities)
        )

    def map_areas(self, phrases: Sequence[str], areas: Sequence[str]) -> list[str]:
        """Expand phrases with area placeholders into area-specific phrases."""
        expanded: list[str] = []
        for phrase in phrases:
            if AREA_PLACEHOLDER in phrase:
                expanded.extend(
                    phrase.replace(AREA_PLACEHOLDER, area) for area in areas
                )
            else:
                expanded.append(phrase)
        return expanded

    def compile_patterns(self, phrases: Sequence[str]) -> list[re.Pattern[str]]:
        """Compile a list of regex patterns from phrases."""
        return [re.compile(phrase, RE_FLAGS) for phrase in phrases]

    def find_area(self, message: str, areas: Sequence[str]) -> PatternMatch | None:
        """Find the first area mentioned in the message."""
        for pattern in areas:
            if match := re.search(pattern, message, RE_FLAGS):
                return PatternMatch(text=match.group(0), pattern=pattern)
        return None

    def match_first(
        self, patterns: Sequence[re.Pattern[str]], message: str
    ) -> PatternMatch | None:
        """Find the first pattern that matches the message."""
        for pattern in patterns:
            match = pattern.search(message)
            if match:
                return PatternMatch(text=match.group(0), pattern=pattern.pattern)
        return None

    def detect(
        self,
        *,
        message: str,
        patterns: Sequence[re.Pattern[str]],
        areas: Sequence[str],
        danger_type: DangerType,
        match_areas: bool = True,
    ) -> Detection:
        """Shared detection helper used by danger-specific methods."""
        if self.match_first(self._safety_patterns, message):
            return Detection(danger=False, message=message)

        danger_match = self.match_first(patterns, message)
        if danger_match is None:
            return Detection(danger=False, message=message)

        area_match = self.find_area(message, areas) if match_areas else None
        if match_areas and area_match is None:
            return Detection(danger=False, message=message)

        return Detection(
            danger=True,
            type=danger_type,
            message=message,
            matched_area=area_match.text if area_match else None,
            matched_danger=danger_match.text,
            area_pattern=area_match.pattern if area_match else None,
            danger_pattern=danger_match.pattern,
        )

    def ballistic_danger(self, message: str) -> Detection:
        """Detect ballistic danger; returns first match or a negative detection."""
        return self.detect(
            danger_type=DangerType.BALLISTIC,
            patterns=self._ballistic_patterns,
            areas=self._regions + self._localities,
            message=message,
        )

    def irbm_danger(self, message: str) -> Detection:
        """Detect nationwide IRBM danger without requiring a configured area."""
        return self.detect(
            danger_type=DangerType.IRBM,
            patterns=self._irbm_patterns,
            areas=(),
            message=message,
            match_areas=False,
        )

    def cruise_missile_danger(self, message: str) -> Detection:
        """Detect cruise-missile danger; returns first match or a negative detection."""
        return self.detect(
            danger_type=DangerType.CRUISE,
            patterns=self._cruise_patterns,
            areas=self._regions + self._localities,
            message=message,
        )

    def drone_danger(self, message: str) -> Detection:
        """Detect drone danger; returns first match or a negative detection."""
        return self.detect(
            danger_type=DangerType.DRONE,
            patterns=self._drone_patterns,
            areas=self._localities,
            message=message,
        )

    def generic_danger(self, message: str) -> Detection:
        """Detect generic danger linked to any provided area."""
        return self.detect(
            danger_type=DangerType.GENERIC,
            patterns=self._generic_patterns,
            areas=self._regions + self._localities,
            message=message,
        )

    def danger(self, message: str) -> Detection:
        """Composite detector: IRBM → ballistic → cruise → drone → generic."""
        for checker in (
            self.irbm_danger,
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
    "PatternMatch",
]
