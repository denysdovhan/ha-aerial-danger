"""Tests for Aerial Danger diagnostics."""

# ruff: noqa: S101

import json

import pytest
from homeassistant.components.diagnostics import REDACTED
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.aerial_danger.const import (
    CONF_NEIGHBORHOOD_PATTERNS,
    CONF_REGION_PATTERNS,
    CONF_SOURCES,
    DOMAIN,
    STATE_BALLISTIC,
    STATE_DANGER,
)
from custom_components.aerial_danger.diagnostics import (
    async_get_config_entry_diagnostics,
)

pytestmark = pytest.mark.usefixtures("enable_custom_integrations")


async def test_config_entry_diagnostics_redacts_user_data(
    hass: HomeAssistant,
) -> None:
    """Test diagnostics redact location patterns and source entities."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_NEIGHBORHOOD_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.alerts"],
        },
        options={
            CONF_REGION_PATTERNS: [r"\bкиївщина\b"],
            CONF_NEIGHBORHOOD_PATTERNS: [],
            CONF_SOURCES: ["sensor.private_alerts"],
        },
    )
    hass.states.async_set("sensor.private_alerts", "Київщина швидкісна!")
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    diagnostics = await async_get_config_entry_diagnostics(hass, entry)

    assert diagnostics["entry"] == {
        "version": entry.version,
        "minor_version": entry.minor_version,
        "state": str(ConfigEntryState.LOADED),
        "data": {
            CONF_REGION_PATTERNS: REDACTED,
            CONF_NEIGHBORHOOD_PATTERNS: REDACTED,
            CONF_SOURCES: REDACTED,
        },
        "options": {
            CONF_REGION_PATTERNS: REDACTED,
            CONF_NEIGHBORHOOD_PATTERNS: REDACTED,
            CONF_SOURCES: REDACTED,
        },
    }
    assert diagnostics["runtime"] == {
        "states": {
            STATE_BALLISTIC: True,
            "cruise": False,
            "drone": False,
            "unknown": False,
            STATE_DANGER: True,
        },
        "active_detection_types": [STATE_BALLISTIC],
        "entity_count": 5,
        "event_entity_available": True,
        "state_listener_active": True,
    }
    json.dumps(diagnostics)
