"""Binary sensors for the Aerial Danger integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.helpers.entity import DeviceInfo

from .const import DEFAULT_NAME, DOMAIN
from .danger import DangerType, Detection

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from . import AerialDangerConfigEntry, RuntimeData


@dataclass(frozen=True, kw_only=True)
class AerialDangerBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes an Aerial Danger binary sensor."""

    danger_type: DangerType | None = None


SENSOR_TYPES: tuple[AerialDangerBinarySensorEntityDescription, ...] = (
    AerialDangerBinarySensorEntityDescription(
        key="ballistic",
        translation_key="ballistic",
        danger_type=DangerType.BALLISTIC,
    ),
    AerialDangerBinarySensorEntityDescription(
        key="cruise",
        translation_key="cruise",
        danger_type=DangerType.CRUISE,
    ),
    AerialDangerBinarySensorEntityDescription(
        key="drone",
        translation_key="drone",
        danger_type=DangerType.DRONE,
    ),
    AerialDangerBinarySensorEntityDescription(
        key="unknown",
        translation_key="unknown",
        danger_type=DangerType.GENERIC,
    ),
    AerialDangerBinarySensorEntityDescription(
        key="danger",
        translation_key="danger",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: AerialDangerConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Aerial Danger binary sensors."""
    runtime = entry.runtime_data

    entities = [
        DangerBinarySensor(
            runtime,
            entry,
            description,
        )
        for description in SENSOR_TYPES
    ]

    async_add_entities(entities)


class DangerBinarySensor(BinarySensorEntity):
    """Represents an Aerial Danger binary sensor."""

    _attr_should_poll = False
    _attr_device_class = BinarySensorDeviceClass.SAFETY

    def __init__(
        self,
        runtime: RuntimeData,
        entry: AerialDangerConfigEntry,
        description: AerialDangerBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        self._runtime = runtime
        self.entity_description = description

        device_name = (
            entry.options.get("name")
            or entry.data.get("name")
            or entry.title
            or DEFAULT_NAME
        )

        self._attr_has_entity_name = True
        self._attr_translation_key = description.translation_key
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=device_name,
        )

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
                    "ballistic": self._runtime.states["ballistic"],
                    "cruise": self._runtime.states["cruise"],
                    "drone": self._runtime.states["drone"],
                    "unknown": self._runtime.states["unknown"],
                }
            )
        else:
            detection: Detection | None = self._runtime.last_detection.get(
                self.entity_description.danger_type
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
