"""Event entity for the Aerial Danger integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.event import EventEntity
from homeassistant.core import callback

from .const import (
    ATTR_MATCHED_AREA,
    ATTR_MATCHED_DANGER,
    ATTR_MATCHED_MESSAGE,
    ATTR_SOURCE_ENTITY_ID,
    ATTR_TIMESTAMP,
    EVENT_TYPE_BALLISTIC,
    EVENT_TYPE_CRUISE,
    EVENT_TYPE_DRONE,
    EVENT_TYPE_IRBM,
    EVENT_TYPE_MLRS,
    EVENT_TYPE_UNKNOWN,
    EVENT_TYPES,
)
from .danger import DangerType
from .entity import AerialDangerEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from . import AerialDangerConfigEntry
    from .runtime import SourceDetection


EVENT_TYPE_BY_DANGER_TYPE = {
    DangerType.IRBM: EVENT_TYPE_IRBM,
    DangerType.MLRS: EVENT_TYPE_MLRS,
    DangerType.BALLISTIC: EVENT_TYPE_BALLISTIC,
    DangerType.CRUISE: EVENT_TYPE_CRUISE,
    DangerType.DRONE: EVENT_TYPE_DRONE,
    DangerType.GENERIC: EVENT_TYPE_UNKNOWN,
}


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: AerialDangerConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Aerial Danger event entity."""
    async_add_entities([AerialDangerEvent(entry)])


class AerialDangerEvent(AerialDangerEntity, EventEntity):
    """Represent detected aerial danger events."""

    _attr_event_types = EVENT_TYPES
    _attr_should_poll = False
    _attr_translation_key = "danger"

    def __init__(self, entry: AerialDangerConfigEntry) -> None:
        """Initialize the event entity."""
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_danger_event"

    async def async_added_to_hass(self) -> None:
        """Register the event entity for direct push updates."""
        await super().async_added_to_hass()
        self._runtime.event_entity = self

    async def async_will_remove_from_hass(self) -> None:
        """Unregister the event entity from direct push updates."""
        if self._runtime.event_entity is self:
            self._runtime.event_entity = None
        await super().async_will_remove_from_hass()

    @callback
    def async_trigger_detection(self, source_detection: SourceDetection) -> None:
        """Publish a detected danger through the event entity."""
        detection = source_detection.detection
        if detection.type is None:
            return

        self._trigger_event(
            EVENT_TYPE_BY_DANGER_TYPE[detection.type],
            {
                ATTR_MATCHED_MESSAGE: detection.message,
                ATTR_MATCHED_AREA: detection.matched_area,
                ATTR_MATCHED_DANGER: detection.matched_danger,
                ATTR_SOURCE_ENTITY_ID: source_detection.source_entity_id,
                ATTR_TIMESTAMP: source_detection.updated_at.isoformat(),
            },
        )
        self.async_write_ha_state()
