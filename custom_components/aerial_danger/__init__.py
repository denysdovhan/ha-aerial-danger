"""Init file for the Aerial Danger integration."""

from __future__ import annotations

import re

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import Event, HomeAssistant, State, callback
from homeassistant.exceptions import ConfigEntryError
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    CONF_NEIGHBORHOOD_PATTERNS,
    CONF_REGION_PATTERNS,
    CONF_SOURCES,
    EVENT_DATA_NEW_STATE,
    EVENT_DATA_OLD_STATE,
    PLATFORMS,
)
from .danger import DangerDetector
from .runtime import RuntimeData, SourceDetection, derive_danger_state

INVALID_PATTERN_MESSAGE = "Invalid regex"
MISSING_PATTERNS_MESSAGE = "At least one area pattern is required"
MISSING_SOURCES_MESSAGE = "At least one source entity is required"


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

    if not regions and not neighborhoods:
        raise ConfigEntryError(MISSING_PATTERNS_MESSAGE)
    if not sources:
        raise ConfigEntryError(MISSING_SOURCES_MESSAGE)

    try:
        DangerDetector.validate_patterns(regions, neighborhoods)
    except re.error as ex:
        message = INVALID_PATTERN_MESSAGE
        raise ConfigEntryError(message) from ex

    detector = DangerDetector(regions, neighborhoods)

    active_detections: dict[str, SourceDetection] = {}
    for source in sources:
        state = hass.states.get(source)
        if state is None or state.state in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            continue

        detection = detector.danger(str(state.state))
        if detection.danger:
            active_detections[source] = SourceDetection(
                source_entity_id=source,
                detection=detection,
                updated_at=state.last_updated,
            )

    states, last_detection = derive_danger_state(active_detections)

    runtime = RuntimeData(
        detector=detector,
        active_detections=active_detections,
        states=states,
        last_detection=last_detection,
        entities=set(),
        event_entity=None,
        unsub=None,
    )

    entry.runtime_data = runtime

    @callback
    def _handle_state(event: Event) -> None:
        new_state: State | None = event.data.get(EVENT_DATA_NEW_STATE)
        old_state: State | None = event.data.get(EVENT_DATA_OLD_STATE)

        if new_state is None:
            return
        if old_state and old_state.state == new_state.state:
            return
        if new_state.state in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            return

        message = str(new_state.state)
        detection = detector.danger(message)

        if detection.danger:
            runtime.active_detections[new_state.entity_id] = SourceDetection(
                source_entity_id=new_state.entity_id,
                detection=detection,
                updated_at=event.time_fired,
            )
            if runtime.event_entity:
                runtime.event_entity.async_trigger_detection(
                    runtime.active_detections[new_state.entity_id]
                )
        else:
            runtime.active_detections.pop(new_state.entity_id, None)

        new_states, new_last_detection = derive_danger_state(runtime.active_detections)
        if new_states != runtime.states or new_last_detection != runtime.last_detection:
            runtime.states = new_states
            runtime.last_detection = new_last_detection
            for entity in runtime.entities:
                entity.async_write_ha_state()

    runtime.unsub = async_track_state_change_event(hass, sources, _handle_state)

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
