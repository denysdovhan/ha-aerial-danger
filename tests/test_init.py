"""Tests for the Aerial Danger integration setup."""

# ruff: noqa: S101

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import CONF_NAME, STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.aerial_danger import RuntimeData
from custom_components.aerial_danger.const import (
    CONF_NEIGHBORHOOD_PATTERNS,
    CONF_REGION_PATTERNS,
    CONF_SOURCES,
    DEFAULT_NAME,
    DOMAIN,
)

pytestmark = pytest.mark.usefixtures("enable_custom_integrations")
EXPECTED_ENTITY_COUNT = 5


def _entry(data: dict[str, object]) -> MockConfigEntry:
    """Create an Aerial Danger mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title=DEFAULT_NAME,
        data=data,
    )


async def test_setup_stores_runtime_data_on_entry(
    hass: HomeAssistant,
) -> None:
    """Test setup stores runtime data on the config entry."""
    entry = _entry(
        {
            CONF_NAME: DEFAULT_NAME,
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_NEIGHBORHOOD_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    config_entry = hass.config_entries.async_get_entry(entry.entry_id)
    assert config_entry is not None
    assert config_entry.state is ConfigEntryState.LOADED
    assert isinstance(config_entry.runtime_data, RuntimeData)
    assert len(config_entry.runtime_data.entities) == EXPECTED_ENTITY_COUNT


async def test_source_state_updates_binary_sensors(
    hass: HomeAssistant,
) -> None:
    """Test source state changes update binary sensors."""
    entry = _entry(
        {
            CONF_NAME: DEFAULT_NAME,
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_NEIGHBORHOOD_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.aerial_danger_ballistic_danger").state == (
        STATE_OFF
    )

    hass.states.async_set("sensor.alerts", "Київ швидкісна!")
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.aerial_danger_ballistic_danger").state == (
        STATE_ON
    )
    assert hass.states.get("binary_sensor.aerial_danger_danger").state == STATE_ON


async def test_same_type_detection_refreshes_attributes(
    hass: HomeAssistant,
) -> None:
    """Test same-type detections refresh entity attributes."""
    entry = _entry(
        {
            CONF_NAME: DEFAULT_NAME,
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_NEIGHBORHOOD_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    hass.states.async_set("sensor.alerts", "Київ швидкісна!")
    await hass.async_block_till_done()
    assert hass.states.get("binary_sensor.aerial_danger_ballistic_danger").state == (
        STATE_ON
    )
    assert hass.states.get("binary_sensor.aerial_danger_danger").state == STATE_ON
    assert (
        hass.states.get("binary_sensor.aerial_danger_ballistic_danger").attributes[
            "message"
        ]
        == "Київ швидкісна!"
    )

    hass.states.async_set("sensor.alerts", "Київ є ЦІЛЬ!")
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.aerial_danger_ballistic_danger").state == (
        STATE_ON
    )
    assert hass.states.get("binary_sensor.aerial_danger_danger").state == STATE_ON
    assert (
        hass.states.get("binary_sensor.aerial_danger_ballistic_danger").attributes[
            "message"
        ]
        == "Київ є ЦІЛЬ!"
    )


async def test_cleared_detection_removes_stale_attributes(
    hass: HomeAssistant,
) -> None:
    """Test non-matching messages clear stale detection attributes."""
    entry = _entry(
        {
            CONF_NAME: DEFAULT_NAME,
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_NEIGHBORHOOD_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    hass.states.async_set("sensor.alerts", "Київ швидкісна!")
    await hass.async_block_till_done()
    hass.states.async_set("sensor.alerts", "Все тихо")
    await hass.async_block_till_done()

    state = hass.states.get("binary_sensor.aerial_danger_ballistic_danger")
    assert state.state == STATE_OFF
    assert "message" not in state.attributes


async def test_setup_rejects_invalid_stored_pattern(
    hass: HomeAssistant,
) -> None:
    """Test setup fails cleanly for invalid stored regex."""
    entry = _entry(
        {
            CONF_NAME: DEFAULT_NAME,
            CONF_REGION_PATTERNS: ["("],
            CONF_NEIGHBORHOOD_PATTERNS: [],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert not await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    config_entry = hass.config_entries.async_get_entry(entry.entry_id)
    assert config_entry is not None
    assert config_entry.state is ConfigEntryState.SETUP_ERROR
