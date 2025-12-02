"""Init file for the Aerial Danger integration."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import Event, HomeAssistant, State, callback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    CONF_CITY_PATTERNS,
    CONF_NEIGHBORHOOD_PATTERNS,
    CONF_SOURCES,
    DOMAIN,
    EVENT_BALLISTIC,
    EVENT_CRUISE,
    EVENT_DRONE,
    EVENT_UNKNOWN,
    PLATFORMS,
)
from .danger import DangerDetector, DangerType, Detection

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)


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
    entities: list
    unsub: Callable[[], None] | None


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Aerial Danger from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    data = entry.options or entry.data
    cities = data.get(CONF_CITY_PATTERNS, [])
    neighborhoods = data.get(CONF_NEIGHBORHOOD_PATTERNS, [])
    sources: list[str] = data.get(CONF_SOURCES, [])

    detector = DangerDetector(cities, neighborhoods)
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
        entities=[],
        unsub=None,
    )

    hass.data[DOMAIN][entry.entry_id] = runtime

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

        if new_states != states:
            states.update(new_states)
            for entity in runtime.entities:
                entity.async_write_ha_state()

        if detection.danger:
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
            # Clear last detections for non-matching types
            for danger_type in last_detection:
                last_detection[danger_type] = None

    if sources:
        runtime.unsub = async_track_state_change_event(hass, sources, _handle_state)
    else:
        _LOGGER.warning(
            "No sources configured for Aerial Danger entry '%s'", entry.title
        )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    runtime: RuntimeData | None = hass.data.get(DOMAIN, {}).get(entry.entry_id)
    if runtime and runtime.unsub:
        runtime.unsub()

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle config entry updates."""
    await hass.config_entries.async_reload(entry.entry_id)
