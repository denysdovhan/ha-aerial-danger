"""Binary sensors for the Aerial Danger integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.helpers.entity import DeviceInfo

from .const import DEFAULT_NAME, DOMAIN
from .danger import DangerType, Detection

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from . import RuntimeData

SENSOR_TYPES: dict[str, dict[str, Any]] = {
    "ballistic": {"name": "Ballistic danger", "type": DangerType.BALLISTIC},
    "cruise": {"name": "Cruise missile danger", "type": DangerType.CRUISE},
    "drone": {"name": "Drone danger", "type": DangerType.DRONE},
    "unknown": {"name": "Unknown danger", "type": DangerType.GENERIC},
    "danger": {"name": "Danger", "type": None},
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Aerial Danger binary sensors."""
    runtime: RuntimeData = hass.data[DOMAIN][entry.entry_id]

    entities = [
        DangerBinarySensor(
            runtime,
            entry,
            key,
            data["name"],
            data["type"],
        )
        for key, data in SENSOR_TYPES.items()
    ]

    runtime.entities.extend(entities)
    async_add_entities(entities)


class DangerBinarySensor(BinarySensorEntity):
    """Represents an Aerial Danger binary sensor."""

    _attr_should_poll = False
    _attr_device_class = BinarySensorDeviceClass.SAFETY

    def __init__(
        self,
        runtime: RuntimeData,
        entry: ConfigEntry,
        key: str,
        name: str,
        danger_type: DangerType | None,
    ) -> None:
        """Initialize the binary sensor."""
        self._runtime = runtime
        self._key = key
        self._danger_type = danger_type

        device_name = (
            entry.options.get("name")
            or entry.data.get("name")
            or entry.title
            or DEFAULT_NAME
        )

        self._attr_has_entity_name = True
        self._attr_translation_key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=device_name,
        )

    @property
    def is_on(self) -> bool:
        """Return true if this danger type is currently active."""
        return self._runtime.states[self._key]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return supplemental attributes for the sensor."""
        attrs: dict[str, Any] = {}
        if self._danger_type is None:
            # aggregate sensor: show which types are active
            attrs.update(
                {
                    "ballistic": self._runtime.states["ballistic"],
                    "cruise": self._runtime.states["cruise"],
                    "drone": self._runtime.states["drone"],
                    "unknown": self._runtime.states["unknown"],
                }
            )
        else:
            detection: Detection | None = self._runtime.last_detection.get(
                self._danger_type
            )
            if detection:
                attrs.update(
                    {
                        "area": detection.area,
                        "match": detection.match,
                        "message": detection.message,
                    }
                )

        return attrs
