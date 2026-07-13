"""Constants for the Aerial Danger integration."""

from typing import Final

from homeassistant.const import Platform

# Integration
DOMAIN: Final = "aerial_danger"
NAME: Final = "Aerial Danger"
DEFAULT_NAME: Final = "Aerial Danger"
PLATFORMS: Final = [Platform.BINARY_SENSOR, Platform.EVENT]

# Configuration
CONF_REGION_PATTERNS: Final = "region_patterns"
CONF_NEIGHBORHOOD_PATTERNS: Final = "neighborhood_patterns"
CONF_SOURCES: Final = "sources"

# Errors
ERROR_INVALID_PATTERN: Final = "Invalid regex"
ERROR_MISSING_PATTERNS: Final = "At least one area pattern is required"
ERROR_MISSING_SOURCES: Final = "At least one source entity is required"

# Entity states
STATE_BALLISTIC: Final = "ballistic"
STATE_CRUISE: Final = "cruise"
STATE_DANGER: Final = "danger"
STATE_DRONE: Final = "drone"
STATE_UNKNOWN_DANGER: Final = "unknown"

# Entity attributes
ATTR_AREA: Final = "area"
ATTR_BALLISTIC: Final = "ballistic"
ATTR_CRUISE: Final = "cruise"
ATTR_DRONE: Final = "drone"
ATTR_MATCH: Final = "match"
ATTR_MESSAGE: Final = "message"
ATTR_SOURCE_ENTITY_ID: Final = "source_entity_id"
ATTR_TIMESTAMP: Final = "timestamp"
ATTR_UNKNOWN: Final = "unknown"

# Events
EVENT_DATA_NEW_STATE: Final = "new_state"
EVENT_DATA_OLD_STATE: Final = "old_state"
EVENT_TYPE_BALLISTIC: Final = "ballistic"
EVENT_TYPE_CRUISE: Final = "cruise"
EVENT_TYPE_DRONE: Final = "drone"
EVENT_TYPE_UNKNOWN: Final = "unknown"
EVENT_TYPES: Final = [
    EVENT_TYPE_BALLISTIC,
    EVENT_TYPE_CRUISE,
    EVENT_TYPE_DRONE,
    EVENT_TYPE_UNKNOWN,
]
