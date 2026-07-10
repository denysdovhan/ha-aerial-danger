"""Init file for the Aerial Danger integration."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import Event, HomeAssistant, State, callback
from homeassistant.exceptions import ConfigEntryError
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    CONF_NEIGHBORHOOD_PATTERNS,
    CONF_REGION_PATTERNS,
    CONF_SOURCES,
    EVENT_BALLISTIC,
    EVENT_CRUISE,
    EVENT_DRONE,
    EVENT_UNKNOWN,
    PLATFORMS,
)
from .danger import DangerDetector, DangerType, Detection

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)
INVALID_PATTERN_MESSAGE = "Invalid regex"


STATE_KEYS = {
    DangerType.BALLISTIC: "ballistic",
    DangerType.CRUISE: "cruise",
    DangerType.DRONE: "drone",
    DangerType.GENERIC: "unknown",
}


@dataclass
class RuntimeData:
    """Keeps runtime objects for an entry."""

    detector: DangerDetector
    states: dict[str, bool]
    last_detection: dict[DangerType, Detection | None]
    entities: set[Entity]
    unsub: Callable[[], None] | None


type AerialDangerConfigEntry = ConfigEntry[RuntimeData]


def _entry_list(
    entry: AerialDangerConfigEntry,
    key: str,
) -> list[str]:
    """Return an option list falling back to entry data."""
    value = entry.options.get(key, entry.data.get(key, []))
    if isinstance(value, list):
        return value
    if isinstance(value, str) and value:
        return [value]
    return []


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AerialDangerConfigEntry,
) -> bool:
    """Set up Aerial Danger from a config entry."""
    regions = _entry_list(entry, CONF_REGION_PATTERNS)
    neighborhoods = _entry_list(entry, CONF_NEIGHBORHOOD_PATTERNS)
    sources = _entry_list(entry, CONF_SOURCES)

    try:
        DangerDetector.validate_patterns(regions, neighborhoods)
    except re.error as ex:
        message = INVALID_PATTERN_MESSAGE
        raise ConfigEntryError(message) from ex

    detector = DangerDetector(regions, neighborhoods)

    states = {
        "ballistic": False,
        "cruise": False,
        "drone": False,
        "unknown": False,
        "danger": False,
    }
    last_detection: dict[DangerType, Detection | None] = {
        DangerType.BALLISTIC: None,
        DangerType.CRUISE: None,
        DangerType.DRONE: None,
        DangerType.GENERIC: None,
    }

    runtime = RuntimeData(
        detector=detector,
        states=states,
        last_detection=last_detection,
        entities=set(),
        unsub=None,
    )

    entry.runtime_data = runtime

    @callback
    def _handle_state(event: Event) -> None:
        new_state: State | None = event.data.get("new_state")
        old_state: State | None = event.data.get("old_state")

        if new_state is None:
            return
        if old_state and old_state.state == new_state.state:
            return
        if new_state.state in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            return

        message = str(new_state.state)
        detection = detector.danger(message)

        new_states = {
            "ballistic": detection.type == DangerType.BALLISTIC,
            "cruise": detection.type == DangerType.CRUISE,
            "drone": detection.type == DangerType.DRONE,
            "unknown": detection.type == DangerType.GENERIC,
        }
        new_states["danger"] = any(new_states.values())

        if detection.danger:
            detection_changed = last_detection.get(detection.type) != detection
            for danger_type in last_detection:
                if danger_type != detection.type:
                    last_detection[danger_type] = None
            last_detection[detection.type] = detection
            event_type = {
                DangerType.BALLISTIC: EVENT_BALLISTIC,
                DangerType.CRUISE: EVENT_CRUISE,
                DangerType.DRONE: EVENT_DRONE,
                DangerType.GENERIC: EVENT_UNKNOWN,
            }[detection.type]
            hass.bus.async_fire(
                event_type,
                {
                    "type": detection.type.value,
                    "area": detection.area,
                    "match": detection.match,
                    "message": detection.message,
                    "entity_id": new_state.entity_id,
                    "timestamp": event.time_fired.isoformat(),
                },
            )
        else:
            detection_changed = any(last_detection.values())
            for danger_type in last_detection:
                last_detection[danger_type] = None

        if new_states != states or detection_changed:
            states.update(new_states)
            for entity in runtime.entities:
                entity.async_write_ha_state()

    if sources:
        runtime.unsub = async_track_state_change_event(hass, sources, _handle_state)
    else:
        _LOGGER.warning(
            "No sources configured for Aerial Danger entry '%s'", entry.title
        )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: AerialDangerConfigEntry,
) -> bool:
    """Unload a config entry."""
    runtime = getattr(entry, "runtime_data", None)
    if runtime and runtime.unsub:
        runtime.unsub()
        runtime.unsub = None

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok and runtime:
        runtime.entities.clear()

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: AerialDangerConfigEntry,
) -> None:
    """Handle config entry updates."""
    await hass.config_entries.async_reload(entry.entry_id)
