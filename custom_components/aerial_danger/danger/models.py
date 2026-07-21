"""Danger detection models for the Aerial Danger integration."""

from dataclasses import dataclass
from enum import Enum


class DangerType(str, Enum):
    """Enum of supported aerial danger types."""

    BALLISTIC = "ballistic"
    CRUISE = "cruise"
    DRONE = "drone"
    GENERIC = "generic"
    IRBM = "irbm"


@dataclass
class PatternMatch:
    """Represents text matched by a regex pattern."""

    text: str
    pattern: str


@dataclass
class Detection:
    """Represents a detected aerial danger."""

    danger: bool
    message: str
    type: DangerType | None = None
    matched_area: str | None = None
    matched_danger: str | None = None
    area_pattern: str | None = None
    danger_pattern: str | None = None
