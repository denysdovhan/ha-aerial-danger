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
    ATTR_AREA,
    ATTR_BALLISTIC,
    ATTR_CRUISE,
    ATTR_DRONE,
    ATTR_MATCH,
    ATTR_MESSAGE,
    ATTR_SOURCE_ENTITY_ID,
    ATTR_UNKNOWN,
    STATE_BALLISTIC,
    STATE_CRUISE,
    STATE_DANGER,
    STATE_DRONE,
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
        key=STATE_BALLISTIC,
        translation_key="ballistic",
        danger_type=DangerType.BALLISTIC,
    ),
    AerialDangerBinarySensorEntityDescription(
        key=STATE_CRUISE,
        translation_key="cruise",
        danger_type=DangerType.CRUISE,
    ),
    AerialDangerBinarySensorEntityDescription(
        key=STATE_DRONE,
        translation_key="drone",
        danger_type=DangerType.DRONE,
    ),
    AerialDangerBinarySensorEntityDescription(
        key=STATE_UNKNOWN_DANGER,
        translation_key="unknown",
        danger_type=DangerType.GENERIC,
    ),
    AerialDangerBinarySensorEntityDescription(
        key=STATE_DANGER,
        translation_key="danger",
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
        attrs: dict[str, Any] = {}
        if self.entity_description.danger_type is None:
            # aggregate sensor: show which types are active
            attrs.update(
                {
                    ATTR_BALLISTIC: self._runtime.states[STATE_BALLISTIC],
                    ATTR_CRUISE: self._runtime.states[STATE_CRUISE],
                    ATTR_DRONE: self._runtime.states[STATE_DRONE],
                    ATTR_UNKNOWN: self._runtime.states[STATE_UNKNOWN_DANGER],
                }
            )
        else:
            source_detection = self._runtime.last_detection.get(
                self.entity_description.danger_type
            )
            if source_detection:
                detection: Detection = source_detection.detection
                attrs.update(
                    {
                        ATTR_AREA: detection.area,
                        ATTR_MATCH: detection.match,
                        ATTR_MESSAGE: detection.message,
                        ATTR_SOURCE_ENTITY_ID: source_detection.source_entity_id,
                    }
                )

        return attrs
