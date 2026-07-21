"""Constants for the Aerial Danger integration."""

import logging
from typing import Final

from homeassistant.const import Platform

# Integration
DOMAIN: Final = "aerial_danger"
NAME: Final = "Aerial Danger"
DEFAULT_NAME: Final = "Aerial Danger"
PLATFORMS: Final = [Platform.BINARY_SENSOR, Platform.EVENT]
LOGGER: Final = logging.getLogger(__package__)

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
STATE_IRBM: Final = "irbm"
STATE_UNKNOWN_DANGER: Final = "unknown"

# Entity attributes
ATTR_MATCHED_AREA: Final = "matched_area"
ATTR_MATCHED_DANGER: Final = "matched_danger"
ATTR_MATCHED_MESSAGE: Final = "matched_message"
ATTR_SOURCE_ENTITY_ID: Final = "source_entity_id"
ATTR_TIMESTAMP: Final = "timestamp"

# Events
EVENT_DATA_NEW_STATE: Final = "new_state"
EVENT_DATA_OLD_STATE: Final = "old_state"
EVENT_TYPE_BALLISTIC: Final = "ballistic"
EVENT_TYPE_CRUISE: Final = "cruise"
EVENT_TYPE_DRONE: Final = "drone"
EVENT_TYPE_IRBM: Final = "irbm"
EVENT_TYPE_UNKNOWN: Final = "unknown"
EVENT_TYPES: Final = [
    EVENT_TYPE_IRBM,
    EVENT_TYPE_BALLISTIC,
    EVENT_TYPE_CRUISE,
    EVENT_TYPE_DRONE,
    EVENT_TYPE_UNKNOWN,
]
