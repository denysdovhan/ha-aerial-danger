"""Init file for the Aerial Danger integration."""

from __future__ import annotations

import re

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import Event, HomeAssistant, State, callback
from homeassistant.exceptions import ConfigEntryError
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    CONF_LOCALITY_PATTERNS,
    CONF_LOCALITY_PRESETS,
    CONF_REGION_PATTERNS,
    CONF_REGION_PRESETS,
    CONF_SOURCES,
    ERROR_INVALID_PATTERN,
    ERROR_MISSING_PATTERNS,
    ERROR_MISSING_SOURCES,
    EVENT_DATA_NEW_STATE,
    EVENT_DATA_OLD_STATE,
    LOGGER,
    PLATFORMS,
)
from .danger import DangerDetector
from .danger.pattern_utils import resolve_locality_patterns, resolve_region_patterns
from .runtime import RuntimeData, SourceDetection, derive_danger_state

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
    region_presets = _entry_list(entry, CONF_REGION_PRESETS)
    regions = resolve_region_patterns(
        _entry_list(entry, CONF_REGION_PATTERNS),
        region_presets,
    )
    localities = resolve_locality_patterns(
        _entry_list(entry, CONF_LOCALITY_PATTERNS),
        region_presets,
        _entry_list(entry, CONF_LOCALITY_PRESETS),
    )
    sources = _entry_list(entry, CONF_SOURCES)

    if not regions and not localities:
        raise ConfigEntryError(ERROR_MISSING_PATTERNS)
    if not sources:
        raise ConfigEntryError(ERROR_MISSING_SOURCES)

    try:
        DangerDetector.validate_patterns(regions, localities)
    except re.error as ex:
        raise ConfigEntryError(ERROR_INVALID_PATTERN) from ex

    detector = DangerDetector(regions, localities)

    active_detections: dict[str, SourceDetection] = {}
    for source in sources:
        state = hass.states.get(source)
        if state is None or state.state in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            continue

        detection = detector.danger(str(state.state))
        if detection.danger:
            LOGGER.debug(
                "Seeded danger for entry %s from %s: type=%s, message=%r, "
                "matched_area=%r, matched_danger=%r, area_pattern=%r, "
                "danger_pattern=%r",
                entry.entry_id,
                source,
                detection.type.value if detection.type else None,
                detection.message,
                detection.matched_area,
                detection.matched_danger,
                detection.area_pattern,
                detection.danger_pattern,
            )
            active_detections[source] = SourceDetection(
                source_entity_id=source,
                detection=detection,
                updated_at=state.last_updated,
            )

    states, last_detection, latest_detection = derive_danger_state(active_detections)

    runtime = RuntimeData(
        detector=detector,
        active_detections=active_detections,
        states=states,
        last_detection=last_detection,
        latest_detection=latest_detection,
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
            LOGGER.debug(
                "Detected danger for entry %s from %s: type=%s, message=%r, "
                "matched_area=%r, matched_danger=%r, area_pattern=%r, "
                "danger_pattern=%r",
                entry.entry_id,
                new_state.entity_id,
                detection.type.value if detection.type else None,
                detection.message,
                detection.matched_area,
                detection.matched_danger,
                detection.area_pattern,
                detection.danger_pattern,
            )
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

        new_states, new_last_detection, new_latest_detection = derive_danger_state(
            runtime.active_detections
        )
        if (
            new_states != runtime.states
            or new_last_detection != runtime.last_detection
            or new_latest_detection != runtime.latest_detection
        ):
            runtime.states = new_states
            runtime.last_detection = new_last_detection
            runtime.latest_detection = new_latest_detection
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
