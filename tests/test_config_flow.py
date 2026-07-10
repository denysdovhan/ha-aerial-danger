"""Tests for the Aerial Danger config flow."""

# ruff: noqa: S101

import pytest
from homeassistant.config_entries import SOURCE_USER
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.aerial_danger.const import (
    CONF_NEIGHBORHOOD_PATTERNS,
    CONF_REGION_PATTERNS,
    CONF_SOURCES,
    DEFAULT_NAME,
    DOMAIN,
)

pytestmark = pytest.mark.usefixtures("enable_custom_integrations")


async def test_user_flow_creates_entry(hass: HomeAssistant) -> None:
    """Test user flow creates an entry with normalized lists."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_NAME: "Kyiv alerts",
            CONF_REGION_PATTERNS: "kyiv\n\ncapital ",
            CONF_NEIGHBORHOOD_PATTERNS: "nyvky",
            CONF_SOURCES: ["sensor.alerts"],
        },
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Kyiv alerts"
    assert result["data"] == {
        CONF_NAME: "Kyiv alerts",
        CONF_REGION_PATTERNS: ["kyiv", "capital"],
        CONF_NEIGHBORHOOD_PATTERNS: ["nyvky"],
        CONF_SOURCES: ["sensor.alerts"],
    }


async def test_user_flow_rejects_invalid_pattern(hass: HomeAssistant) -> None:
    """Test user flow rejects invalid regex patterns."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_NAME: DEFAULT_NAME,
            CONF_REGION_PATTERNS: "(",
            CONF_NEIGHBORHOOD_PATTERNS: "",
            CONF_SOURCES: ["sensor.alerts"],
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_pattern"}


async def test_user_flow_aborts_if_already_configured(
    hass: HomeAssistant,
) -> None:
    """Test user flow prevents duplicate entries."""
    MockConfigEntry(domain=DOMAIN, data={CONF_NAME: DEFAULT_NAME}).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_options_flow_updates_lists(hass: HomeAssistant) -> None:
    """Test options flow updates normalized list options."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=DEFAULT_NAME,
        data={
            CONF_NAME: DEFAULT_NAME,
            CONF_REGION_PATTERNS: ["kyiv"],
            CONF_NEIGHBORHOOD_PATTERNS: ["nyvky"],
            CONF_SOURCES: ["sensor.old_alerts"],
        },
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {
            CONF_NAME: "Updated alerts",
            CONF_REGION_PATTERNS: "kyiv\ncapital",
            CONF_NEIGHBORHOOD_PATTERNS: "nyvky\nsvyatoshyn",
            CONF_SOURCES: ["sensor.alerts"],
        },
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        CONF_NAME: "Updated alerts",
        CONF_REGION_PATTERNS: ["kyiv", "capital"],
        CONF_NEIGHBORHOOD_PATTERNS: ["nyvky", "svyatoshyn"],
        CONF_SOURCES: ["sensor.alerts"],
    }


async def test_options_flow_rejects_invalid_pattern(hass: HomeAssistant) -> None:
    """Test options flow rejects invalid regex patterns."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=DEFAULT_NAME,
        data={
            CONF_NAME: DEFAULT_NAME,
            CONF_REGION_PATTERNS: ["kyiv"],
            CONF_NEIGHBORHOOD_PATTERNS: [],
            CONF_SOURCES: ["sensor.alerts"],
        },
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {
            CONF_NAME: DEFAULT_NAME,
            CONF_REGION_PATTERNS: "kyiv",
            CONF_NEIGHBORHOOD_PATTERNS: "(",
            CONF_SOURCES: ["sensor.alerts"],
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_pattern"}
