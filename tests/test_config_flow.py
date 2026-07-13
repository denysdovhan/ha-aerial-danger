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
from custom_components.aerial_danger.runtime import RuntimeData

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

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_NAME: DEFAULT_NAME,
            CONF_REGION_PATTERNS: "kyiv",
            CONF_NEIGHBORHOOD_PATTERNS: "",
            CONF_SOURCES: ["sensor.alerts"],
        },
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY


@pytest.mark.parametrize(
    ("region_patterns", "neighborhood_patterns"),
    [("", ""), ("\n", "  ")],
)
async def test_user_flow_requires_pattern(
    hass: HomeAssistant,
    region_patterns: str,
    neighborhood_patterns: str,
) -> None:
    """Test user flow requires at least one area pattern."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_NAME: DEFAULT_NAME,
            CONF_REGION_PATTERNS: region_patterns,
            CONF_NEIGHBORHOOD_PATTERNS: neighborhood_patterns,
            CONF_SOURCES: ["sensor.alerts"],
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "patterns_required"}


async def test_user_flow_requires_source(hass: HomeAssistant) -> None:
    """Test user flow requires at least one source entity."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_NAME: DEFAULT_NAME,
            CONF_REGION_PATTERNS: "kyiv",
            CONF_NEIGHBORHOOD_PATTERNS: "",
            CONF_SOURCES: [],
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {CONF_SOURCES: "sources_required"}


async def test_user_flow_allows_multiple_entries(
    hass: HomeAssistant,
) -> None:
    """Test user flow creates an entry when another already exists."""
    MockConfigEntry(
        domain=DOMAIN,
        title="Existing alerts",
        data={
            CONF_REGION_PATTERNS: ["kyiv"],
            CONF_NEIGHBORHOOD_PATTERNS: [],
            CONF_SOURCES: ["sensor.existing_alerts"],
        },
    ).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_NAME: "Additional alerts",
            CONF_REGION_PATTERNS: "capital",
            CONF_NEIGHBORHOOD_PATTERNS: "nyvky",
            CONF_SOURCES: ["sensor.additional_alerts"],
        },
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Additional alerts"


async def test_options_flow_updates_lists(hass: HomeAssistant) -> None:
    """Test options flow updates normalized list options."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=DEFAULT_NAME,
        data={
            CONF_REGION_PATTERNS: "kyiv",
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
            CONF_REGION_PATTERNS: "kyiv\ncapital",
            CONF_NEIGHBORHOOD_PATTERNS: "nyvky\nsvyatoshyn",
            CONF_SOURCES: ["sensor.alerts"],
        },
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        CONF_REGION_PATTERNS: ["kyiv", "capital"],
        CONF_NEIGHBORHOOD_PATTERNS: ["nyvky", "svyatoshyn"],
        CONF_SOURCES: ["sensor.alerts"],
    }


async def test_options_flow_reloads_loaded_entry(hass: HomeAssistant) -> None:
    """Test options updates reload an active config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=DEFAULT_NAME,
        data={
            CONF_REGION_PATTERNS: ["kyiv"],
            CONF_NEIGHBORHOOD_PATTERNS: [],
            CONF_SOURCES: ["sensor.old_alerts"],
        },
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    old_runtime = entry.runtime_data
    assert isinstance(old_runtime, RuntimeData)

    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {
            CONF_REGION_PATTERNS: "capital",
            CONF_NEIGHBORHOOD_PATTERNS: "",
            CONF_SOURCES: ["sensor.new_alerts"],
        },
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert isinstance(entry.runtime_data, RuntimeData)
    assert entry.runtime_data is not old_runtime


async def test_options_flow_rejects_invalid_pattern(hass: HomeAssistant) -> None:
    """Test options flow rejects invalid regex patterns."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=DEFAULT_NAME,
        data={
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
            CONF_REGION_PATTERNS: "kyiv",
            CONF_NEIGHBORHOOD_PATTERNS: "(",
            CONF_SOURCES: ["sensor.alerts"],
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_pattern"}

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {
            CONF_REGION_PATTERNS: "kyiv",
            CONF_NEIGHBORHOOD_PATTERNS: "",
            CONF_SOURCES: ["sensor.alerts"],
        },
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_options_flow_requires_pattern(hass: HomeAssistant) -> None:
    """Test options flow requires at least one area pattern."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=DEFAULT_NAME,
        data={
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
            CONF_REGION_PATTERNS: "",
            CONF_NEIGHBORHOOD_PATTERNS: "",
            CONF_SOURCES: ["sensor.alerts"],
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "patterns_required"}


async def test_options_flow_requires_source(hass: HomeAssistant) -> None:
    """Test options flow requires at least one source entity."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=DEFAULT_NAME,
        data={
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
            CONF_REGION_PATTERNS: "kyiv",
            CONF_NEIGHBORHOOD_PATTERNS: "",
            CONF_SOURCES: [],
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {CONF_SOURCES: "sources_required"}
