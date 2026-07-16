"""Diagnostics support for the Aerial Danger integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from . import AerialDangerConfigEntry


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,  # noqa: ARG001
    entry: AerialDangerConfigEntry,
) -> dict[str, object]:
    """Return diagnostics for a config entry."""
    runtime = entry.runtime_data

    return {
        "entry": {
            "version": entry.version,
            "minor_version": entry.minor_version,
            "state": str(entry.state),
            "data": entry.data,
            "options": entry.options,
        },
        "runtime": {
            "states": dict(runtime.states),
            "active_detection_types": sorted(
                source_detection.detection.type.value
                for source_detection in runtime.active_detections.values()
                if source_detection.detection.type is not None
            ),
            "entity_count": len(runtime.entities),
            "event_entity_available": runtime.event_entity is not None,
            "state_listener_active": runtime.unsub is not None,
        },
    }
