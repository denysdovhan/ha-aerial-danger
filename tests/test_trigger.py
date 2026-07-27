"""Tests for Aerial Danger triggers."""

# ruff: noqa: S101

import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock, Mock

import pytest
from homeassistant.components.websocket_api.automation import (
    async_get_triggers_for_target,
)
from homeassistant.const import CONF_DEVICE_ID, CONF_PLATFORM, CONF_TARGET
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.trigger import (
    async_initialize_triggers,
    async_validate_trigger_config,
)
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.aerial_danger.const import (
    ATTR_MATCHED_MESSAGE,
    CONF_LOCALITY_PATTERNS,
    CONF_REGION_PATTERNS,
    CONF_SOURCES,
    DOMAIN,
    EVENT_TYPE_DRONE,
    EVENT_TYPES,
    STATE_DANGER,
)

pytestmark = pytest.mark.usefixtures("enable_custom_integrations")
EXPECTED_MATCH_COUNT = 2


async def _setup_entry(hass: HomeAssistant) -> str:
    """Set up an entry and return its device ID."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Kyiv alerts",
        data={
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.alerts"],
        },
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    device = dr.async_get(hass).async_get_device(identifiers={(DOMAIN, entry.entry_id)})
    assert device is not None
    return device.id


async def test_trigger_discovery(hass: HomeAssistant) -> None:
    """Test target discovery returns every danger type."""
    device_id = await _setup_entry(hass)

    triggers = await async_get_triggers_for_target(
        hass,
        {CONF_DEVICE_ID: [device_id]},
        expand_group=True,
    )

    assert {
        f"{DOMAIN}.{trigger_type}" for trigger_type in [STATE_DANGER, *EVENT_TYPES]
    } <= triggers


async def test_trigger_fires_for_selected_danger(
    hass: HomeAssistant,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test only matching detections fire and same-type detections repeat."""
    monkeypatch.setattr(
        dt_util,
        "utcnow",
        lambda: datetime(2026, 7, 23, tzinfo=UTC),
    )
    device_id = await _setup_entry(hass)
    config = await async_validate_trigger_config(
        hass,
        [
            {
                CONF_PLATFORM: f"{DOMAIN}.{EVENT_TYPE_DRONE}",
                CONF_TARGET: {CONF_DEVICE_ID: [device_id]},
            }
        ],
    )
    action_called = asyncio.Event()
    action = AsyncMock(side_effect=lambda *_: action_called.set())
    remove = await async_initialize_triggers(
        hass,
        config,
        action,
        DOMAIN,
        "test",
        Mock(),
    )
    assert remove is not None

    hass.states.async_set("sensor.alerts", "Київ швидкісна!")
    await hass.async_block_till_done()
    action.assert_not_awaited()

    hass.states.async_set("sensor.alerts", "Нивки над вами БПЛА!")
    await asyncio.wait_for(action_called.wait(), timeout=1)
    action.assert_awaited_once()
    assert (
        action.await_args.args[0]["trigger"]["to_state"].attributes[
            ATTR_MATCHED_MESSAGE
        ]
        == "Нивки над вами БПЛА!"
    )

    action_called.clear()
    hass.states.async_set("sensor.alerts", "Нивки, летить БПЛА!")
    await asyncio.wait_for(action_called.wait(), timeout=1)
    assert action.await_count == EXPECTED_MATCH_COUNT

    remove()
    action_called.clear()
    hass.states.async_set("sensor.alerts", "БПЛА над Нивками!")
    await hass.async_block_till_done()
    assert action.await_count == EXPECTED_MATCH_COUNT


@pytest.mark.parametrize(
    "message",
    [
        pytest.param("Загроза БРСД.", id="irbm"),
        pytest.param("Київ швидкісна!", id="ballistic"),
        pytest.param("Київ увага КР!!", id="cruise"),
        pytest.param("Нивки над вами БПЛА!", id="drone"),
        pytest.param("Київ!", id="unknown"),
    ],
)
async def test_danger_trigger_fires_for_every_danger(
    hass: HomeAssistant,
    message: str,
) -> None:
    """Test the aggregate trigger fires for every native danger type."""
    device_id = await _setup_entry(hass)
    config = await async_validate_trigger_config(
        hass,
        [
            {
                CONF_PLATFORM: f"{DOMAIN}.{STATE_DANGER}",
                CONF_TARGET: {CONF_DEVICE_ID: [device_id]},
            }
        ],
    )
    action_called = asyncio.Event()
    action = AsyncMock(side_effect=lambda *_: action_called.set())
    remove = await async_initialize_triggers(
        hass,
        config,
        action,
        DOMAIN,
        "test",
        Mock(),
    )
    assert remove is not None

    hass.states.async_set("sensor.alerts", message)
    await asyncio.wait_for(action_called.wait(), timeout=1)

    action.assert_awaited_once()
    remove()
