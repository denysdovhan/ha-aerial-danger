"""Constants for the Aerial Danger integration."""

from typing import Final

from homeassistant.const import Platform

CONF_CITY_PATTERNS: Final = "city_patterns"
CONF_NEIGHBORHOOD_PATTERNS: Final = "neighborhood_patterns"
CONF_SOURCES: Final = "sources"

EVENT_BALLISTIC: Final = "ballistic_danger"
EVENT_CRUISE: Final = "cruise_danger"
EVENT_DRONE: Final = "drone_danger"
EVENT_UNKNOWN: Final = "unknown_danger"
EVENTS: Final = (
    EVENT_BALLISTIC,
    EVENT_CRUISE,
    EVENT_DRONE,
    EVENT_UNKNOWN,
)

DOMAIN: Final = "aerial_danger"
NAME: Final = "Aerial Danger"
DEFAULT_NAME: Final = "Aerial Danger"
PLATFORMS: Final = [Platform.BINARY_SENSOR]
