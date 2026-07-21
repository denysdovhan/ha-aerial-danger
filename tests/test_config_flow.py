"""Tests for Aerial Danger config and options flows."""

# ruff: noqa: S101

import pytest
from homeassistant.config_entries import SOURCE_USER
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult, FlowResultType
from homeassistant.helpers import selector
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.aerial_danger.const import (
    CONF_NEIGHBORHOOD_PATTERNS,
    CONF_NEIGHBORHOOD_PRESETS,
    CONF_REGION_PATTERNS,
    CONF_REGION_PRESETS,
    CONF_SOURCES,
    DEFAULT_NAME,
    DOMAIN,
)
from custom_components.aerial_danger.runtime import RuntimeData

pytestmark = pytest.mark.usefixtures("enable_custom_integrations")


async def _config_regions(
    hass: HomeAssistant,
    *,
    name: str = DEFAULT_NAME,
    sources: list[str] | None = None,
) -> FlowResult:
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    return await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_NAME: name,
            CONF_SOURCES: ["sensor.alerts"] if sources is None else sources,
        },
    )


async def _config_neighborhoods(
    hass: HomeAssistant,
    *,
    region_presets: list[str] | None = None,
    region_patterns: str = "",
) -> FlowResult:
    result = await _config_regions(hass)
    return await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_REGION_PRESETS: region_presets or [],
            CONF_REGION_PATTERNS: region_patterns,
        },
    )


def _entry(data: dict[str, object]) -> MockConfigEntry:
    return MockConfigEntry(domain=DOMAIN, title=DEFAULT_NAME, data=data)


async def _options_regions(hass: HomeAssistant, entry: MockConfigEntry) -> FlowResult:
    result = await hass.config_entries.options.async_init(entry.entry_id)
    return await hass.config_entries.options.async_configure(
        result["flow_id"], {CONF_SOURCES: ["sensor.updated"]}
    )


async def test_config_preset_only_and_selector_shape(hass: HomeAssistant) -> None:
    """Test preset-only configuration and dependent selectors."""
    result = await _config_regions(hass, name="Kyiv alerts")
    assert result["step_id"] == "regions"
    assert isinstance(
        result["data_schema"].schema[CONF_REGION_PRESETS], selector.SelectSelector
    )
    assert isinstance(
        result["data_schema"].schema[CONF_REGION_PATTERNS], selector.TextSelector
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {CONF_REGION_PRESETS: ["kyiv"], CONF_REGION_PATTERNS: ""},
    )
    assert result["step_id"] == "neighborhoods"
    neighborhood_selector = result["data_schema"].schema[CONF_NEIGHBORHOOD_PRESETS]
    assert isinstance(neighborhood_selector, selector.SelectSelector)
    assert neighborhood_selector.config["multiple"] is True
    assert isinstance(
        result["data_schema"].schema[CONF_NEIGHBORHOOD_PATTERNS],
        selector.TextSelector,
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_NEIGHBORHOOD_PRESETS: ["kyiv_nyvky"],
            CONF_NEIGHBORHOOD_PATTERNS: "",
        },
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Kyiv alerts"
    assert result["data"] == {
        CONF_SOURCES: ["sensor.alerts"],
        CONF_REGION_PRESETS: ["kyiv"],
        CONF_REGION_PATTERNS: [],
        CONF_NEIGHBORHOOD_PRESETS: ["kyiv_nyvky"],
        CONF_NEIGHBORHOOD_PATTERNS: [],
    }


@pytest.mark.parametrize(
    (
        "region_presets",
        "region_patterns",
        "neighborhood_presets",
        "neighborhood_patterns",
    ),
    [
        ([], "custom region\nsecond region", [], "custom neighborhood"),
        (["kyiv"], "custom region", ["kyiv_nyvky"], "custom neighborhood"),
        (["kyiv"], "", ["kyiv_nyvky", "kyiv_sviatoshyn"], ""),
    ],
)
async def test_config_custom_combined_and_multiple_neighborhoods(
    hass: HomeAssistant,
    region_presets: list[str],
    region_patterns: str,
    neighborhood_presets: list[str],
    neighborhood_patterns: str,
) -> None:
    """Test custom, combined, and multi-neighborhood configuration."""
    result = await _config_neighborhoods(
        hass, region_presets=region_presets, region_patterns=region_patterns
    )
    user_input = {CONF_NEIGHBORHOOD_PATTERNS: neighborhood_patterns}
    if region_presets:
        user_input[CONF_NEIGHBORHOOD_PRESETS] = neighborhood_presets
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"][CONF_REGION_PATTERNS] == region_patterns.splitlines()
    assert result["data"][CONF_NEIGHBORHOOD_PRESETS] == neighborhood_presets


async def test_config_no_region_omits_neighborhood_selector(
    hass: HomeAssistant,
) -> None:
    """Test custom neighborhoods work without a selected region."""
    result = await _config_neighborhoods(hass)
    schema = result["data_schema"].schema
    assert CONF_NEIGHBORHOOD_PRESETS not in schema
    assert isinstance(schema[CONF_NEIGHBORHOOD_PATTERNS], selector.TextSelector)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_NEIGHBORHOOD_PATTERNS: "custom neighborhood"}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_config_validation(hass: HomeAssistant) -> None:
    """Test source, effective-pattern, and region regex validation steps."""
    result = await _config_regions(hass, sources=[])
    assert result["step_id"] == "user"
    assert result["errors"] == {CONF_SOURCES: "sources_required"}

    result = await _config_regions(hass)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_REGION_PATTERNS: "("}
    )
    assert result["step_id"] == "regions"
    assert result["errors"] == {"base": "invalid_pattern"}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_REGION_PATTERNS: ""}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_NEIGHBORHOOD_PATTERNS: "("}
    )
    assert result["step_id"] == "neighborhoods"
    assert result["errors"] == {"base": "invalid_pattern"}
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_NEIGHBORHOOD_PATTERNS: ""}
    )
    assert result["errors"] == {"base": "patterns_required"}


async def test_config_allows_multiple_entries(hass: HomeAssistant) -> None:
    """Test another entry does not block setup."""
    _entry(
        {
            CONF_REGION_PATTERNS: ["existing"],
            CONF_NEIGHBORHOOD_PATTERNS: [],
            CONF_SOURCES: ["sensor.existing"],
        }
    ).add_to_hass(hass)
    result = await _config_neighborhoods(hass, region_presets=["kyiv"])
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_NEIGHBORHOOD_PATTERNS: ""}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_options_prepopulation_and_old_entry_zero_presets(
    hass: HomeAssistant,
) -> None:
    """Test old entries prepopulate custom values and default presets empty."""
    entry = _entry(
        {
            CONF_REGION_PRESETS: {},
            CONF_REGION_PATTERNS: ["old region", "second region"],
            CONF_NEIGHBORHOOD_PATTERNS: ["old neighborhood"],
            CONF_SOURCES: ["sensor.old"],
        }
    )
    entry.add_to_hass(hass)
    result = await _options_regions(hass, entry)
    schema = result["data_schema"].schema
    region_marker = next(key for key in schema if key == CONF_REGION_PATTERNS)
    preset_marker = next(key for key in schema if key == CONF_REGION_PRESETS)
    assert region_marker.default() == "old region\nsecond region"
    assert preset_marker.default() == []


async def test_options_prepopulates_legacy_string_patterns(
    hass: HomeAssistant,
) -> None:
    """Test legacy string patterns remain editable in options."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: "legacy region",
            CONF_NEIGHBORHOOD_PATTERNS: "legacy neighborhood",
            CONF_SOURCES: ["sensor.old"],
        }
    )
    entry.add_to_hass(hass)

    result = await _options_regions(hass, entry)
    region_schema = result["data_schema"].schema
    region_marker = next(key for key in region_schema if key == CONF_REGION_PATTERNS)
    assert region_marker.default() == "legacy region"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {CONF_REGION_PATTERNS: "legacy region"}
    )
    neighborhood_schema = result["data_schema"].schema
    neighborhood_marker = next(
        key for key in neighborhood_schema if key == CONF_NEIGHBORHOOD_PATTERNS
    )
    assert neighborhood_marker.default() == "legacy neighborhood"


async def test_options_parent_deselection_prunes_children(
    hass: HomeAssistant,
) -> None:
    """Test deselecting a region removes its neighborhood selections."""
    entry = _entry(
        {
            CONF_REGION_PRESETS: ["kyiv"],
            CONF_REGION_PATTERNS: [],
            CONF_NEIGHBORHOOD_PRESETS: ["kyiv_nyvky"],
            CONF_NEIGHBORHOOD_PATTERNS: ["custom neighborhood"],
            CONF_SOURCES: ["sensor.old"],
        }
    )
    entry.add_to_hass(hass)
    result = await _options_regions(hass, entry)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {CONF_REGION_PRESETS: [], CONF_REGION_PATTERNS: "custom region"},
    )
    assert CONF_NEIGHBORHOOD_PRESETS not in result["data_schema"].schema
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {CONF_NEIGHBORHOOD_PATTERNS: "custom neighborhood"}
    )
    assert result["data"][CONF_NEIGHBORHOOD_PRESETS] == []


async def test_options_reloads_entry(hass: HomeAssistant) -> None:
    """Test saved three-step options reload a loaded entry."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: ["old"],
            CONF_NEIGHBORHOOD_PATTERNS: [],
            CONF_SOURCES: ["sensor.old"],
        }
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    old_runtime = entry.runtime_data
    result = await _options_regions(hass, entry)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {CONF_REGION_PRESETS: ["kyiv"], CONF_REGION_PATTERNS: ""},
    )
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {
            CONF_NEIGHBORHOOD_PRESETS: ["kyiv_nyvky"],
            CONF_NEIGHBORHOOD_PATTERNS: "",
        },
    )
    await hass.async_block_till_done()
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert isinstance(entry.runtime_data, RuntimeData)
    assert entry.runtime_data is not old_runtime


async def test_options_validation(hass: HomeAssistant) -> None:
    """Test source, regex, and effective-pattern options validation."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: ["old"],
            CONF_NEIGHBORHOOD_PATTERNS: [],
            CONF_SOURCES: ["sensor.old"],
        }
    )
    entry.add_to_hass(hass)
    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {CONF_SOURCES: []}
    )
    assert result["errors"] == {CONF_SOURCES: "sources_required"}
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {CONF_SOURCES: ["sensor.updated"]}
    )
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {CONF_REGION_PATTERNS: "("}
    )
    assert result["errors"] == {"base": "invalid_pattern"}
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {CONF_REGION_PATTERNS: ""}
    )
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {CONF_NEIGHBORHOOD_PATTERNS: "("}
    )
    assert result["errors"] == {"base": "invalid_pattern"}
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {CONF_NEIGHBORHOOD_PATTERNS: ""}
    )
    assert result["errors"] == {"base": "patterns_required"}
