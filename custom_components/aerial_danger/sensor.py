"""Diagnostic sensors for the Aerial Danger integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import EntityCategory

from .const import (
    MATCHED_AREA,
    MATCHED_DANGER,
    MATCHED_MESSAGE,
    MATCHED_SOURCE,
    STATE_CLEAR,
    STATE_NATIONWIDE,
)
from .danger import DangerType
from .entity import AerialDangerEntity

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from . import AerialDangerConfigEntry
    from .runtime import SourceDetection


def state_matched_message(
    _hass: HomeAssistant,
    source_detection: SourceDetection,
) -> str:
    """Return the matched source message."""
    return source_detection.detection.message


def state_matched_area(
    _hass: HomeAssistant,
    source_detection: SourceDetection,
) -> str | None:
    """Return the matched area."""
    if source_detection.detection.type is DangerType.IRBM:
        return STATE_NATIONWIDE
    return source_detection.detection.matched_area


def state_matched_danger(
    _hass: HomeAssistant,
    source_detection: SourceDetection,
) -> str | None:
    """Return the matched danger."""
    return source_detection.detection.matched_danger


def state_matched_source(
    hass: HomeAssistant,
    source_detection: SourceDetection,
) -> str | None:
    """Return the friendly name of the matched source entity."""
    state = hass.states.get(source_detection.source_entity_id)
    return state.name if state else None


@dataclass(frozen=True, kw_only=True)
class AerialDangerSensorEntityDescription(SensorEntityDescription):
    """Describe an Aerial Danger diagnostic sensor."""

    value_fn: Callable[[HomeAssistant, SourceDetection], str | None]


SENSOR_TYPES: tuple[AerialDangerSensorEntityDescription, ...] = (
    AerialDangerSensorEntityDescription(
        key=MATCHED_MESSAGE,
        translation_key=MATCHED_MESSAGE,
        value_fn=state_matched_message,
    ),
    AerialDangerSensorEntityDescription(
        key=MATCHED_AREA,
        translation_key=MATCHED_AREA,
        value_fn=state_matched_area,
    ),
    AerialDangerSensorEntityDescription(
        key=MATCHED_DANGER,
        translation_key=MATCHED_DANGER,
        value_fn=state_matched_danger,
    ),
    AerialDangerSensorEntityDescription(
        key=MATCHED_SOURCE,
        translation_key=MATCHED_SOURCE,
        value_fn=state_matched_source,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: AerialDangerConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Aerial Danger diagnostic sensors."""
    async_add_entities(
        DangerDiagnosticSensor(entry, description) for description in SENSOR_TYPES
    )


class DangerDiagnosticSensor(AerialDangerEntity, SensorEntity):
    """Represent an Aerial Danger diagnostic sensor."""

    _attr_should_poll = False
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    entity_description: AerialDangerSensorEntityDescription

    def __init__(
        self,
        entry: AerialDangerConfigEntry,
        description: AerialDangerSensorEntityDescription,
    ) -> None:
        """Initialize the diagnostic sensor."""
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
    def native_value(self) -> str | None:
        """Return the current aggregate match value."""
        if (source_detection := self._runtime.latest_detection) is None:
            return STATE_CLEAR
        return self.entity_description.value_fn(self.hass, source_detection)
