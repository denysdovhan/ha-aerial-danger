"""Danger detection models for the Aerial Danger integration."""

from dataclasses import dataclass
from enum import Enum


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
