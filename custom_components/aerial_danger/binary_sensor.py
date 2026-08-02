"""Binary sensors for the Aerial Danger integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .const import (
    ATTR_MATCHED_AREA,
    ATTR_MATCHED_DANGER,
    ATTR_MATCHED_MESSAGE,
    ATTR_SOURCE_ENTITY_ID,
    STATE_BALLISTIC,
    STATE_CRUISE,
    STATE_DANGER,
    STATE_DRONE,
    STATE_IRBM,
    STATE_MLRS,
    STATE_UNKNOWN_DANGER,
)
from .danger import DangerType, Detection
from .entity import AerialDangerEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from . import AerialDangerConfigEntry


@dataclass(frozen=True, kw_only=True)
class AerialDangerBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes an Aerial Danger binary sensor."""

    danger_type: DangerType | None = None


SENSOR_TYPES: tuple[AerialDangerBinarySensorEntityDescription, ...] = (
    AerialDangerBinarySensorEntityDescription(
        key=STATE_IRBM,
        translation_key=STATE_IRBM,
        danger_type=DangerType.IRBM,
    ),
    AerialDangerBinarySensorEntityDescription(
        key=STATE_MLRS,
        translation_key=STATE_MLRS,
        danger_type=DangerType.MLRS,
    ),
    AerialDangerBinarySensorEntityDescription(
        key=STATE_BALLISTIC,
        translation_key=STATE_BALLISTIC,
        danger_type=DangerType.BALLISTIC,
    ),
    AerialDangerBinarySensorEntityDescription(
        key=STATE_CRUISE,
        translation_key=STATE_CRUISE,
        danger_type=DangerType.CRUISE,
    ),
    AerialDangerBinarySensorEntityDescription(
        key=STATE_DRONE,
        translation_key=STATE_DRONE,
        danger_type=DangerType.DRONE,
    ),
    AerialDangerBinarySensorEntityDescription(
        key=STATE_UNKNOWN_DANGER,
        translation_key=STATE_UNKNOWN_DANGER,
        danger_type=DangerType.GENERIC,
    ),
    AerialDangerBinarySensorEntityDescription(
        key=STATE_DANGER,
        translation_key=STATE_DANGER,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: AerialDangerConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Aerial Danger binary sensors."""
    entities = [
        DangerBinarySensor(
            entry,
            description,
        )
        for description in SENSOR_TYPES
    ]

    async_add_entities(entities)


class DangerBinarySensor(AerialDangerEntity, BinarySensorEntity):
    """Represents an Aerial Danger binary sensor."""

    _attr_should_poll = False
    _attr_device_class = BinarySensorDeviceClass.SAFETY

    def __init__(
        self,
        entry: AerialDangerConfigEntry,
        description: AerialDangerBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(entry)
        self.entity_description = description

        self._attr_translation_key = description.translation_key
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    async def async_added_to_hass(self) -> None:
        """Register entity for push updates."""
        await super().async_added_to_hass()
        self._runtime.entities.add(self)

    async def async_will_remove_from_hass(self) -> None:
        """Unregister entity from push updates."""
        self._runtime.entities.discard(self)
        await super().async_will_remove_from_hass()

    @property
    def is_on(self) -> bool:
        """Return true if this danger type is currently active."""
        return self._runtime.states[self.entity_description.key]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return supplemental attributes for the sensor."""
        if self.entity_description.danger_type is None:
            source_detection = self._runtime.latest_detection
        else:
            source_detection = self._runtime.last_detection.get(
                self.entity_description.danger_type
            )

        detection: Detection | None = (
            source_detection.detection if source_detection else None
        )
        return {
            ATTR_MATCHED_MESSAGE: detection.message if detection else None,
            ATTR_MATCHED_AREA: detection.matched_area if detection else None,
            ATTR_MATCHED_DANGER: detection.matched_danger if detection else None,
            ATTR_SOURCE_ENTITY_ID: (
                source_detection.source_entity_id if source_detection else None
            ),
        }
