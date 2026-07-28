"""Config flow for the Aerial Danger integration."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_LOCALITY_PATTERNS,
    CONF_LOCALITY_PRESETS,
    CONF_REGION_PATTERNS,
    CONF_REGION_PRESETS,
    CONF_SOURCES,
    DEFAULT_NAME,
    DEFAULT_REGION_PATTERNS,
    DOMAIN,
)
from .danger import DangerDetector
from .danger.pattern_utils import (
    locality_ids,
    resolve_locality_patterns,
    resolve_region_patterns,
)
from .danger.presets import PRESETS

if TYPE_CHECKING:
    from homeassistant.data_entry_flow import FlowResult


def _validate_pattern_input(value: Any) -> list[str] | None:
    """Validate YAML pattern input."""
    if value is None or value == {}:
        return []
    if isinstance(value, list) and all(isinstance(pattern, str) for pattern in value):
        return value
    return None


def _patterns_are_valid(patterns: list[str]) -> bool:
    """Return whether regex patterns compile."""
    try:
        DangerDetector.validate_patterns(patterns)
    except re.error:
        return False
    return True


def build_preset_selector(
    options: list[str], translation_key: str
) -> selector.SelectSelector:
    """Create a searchable translated preset selector."""
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=options,
            multiple=True,
            mode=selector.SelectSelectorMode.DROPDOWN,
            translation_key=translation_key,
        )
    )


def build_regions_schema(
    selected_presets: list[str], patterns: list[str]
) -> vol.Schema:
    """Return the region step schema."""
    return vol.Schema(
        {
            vol.Optional(
                CONF_REGION_PRESETS, default=selected_presets
            ): build_preset_selector(list(PRESETS), "region_presets"),
            vol.Optional(
                CONF_REGION_PATTERNS, default=patterns
            ): selector.ObjectSelector(),
        }
    )


def build_localities_schema(
    region_presets: list[str],
    selected_presets: list[str],
    patterns: list[str],
) -> vol.Schema:
    """Return the locality step schema for selected regions."""
    fields: dict[vol.Marker, object] = {}
    available_localities = locality_ids(region_presets)
    if available_localities:
        fields[vol.Optional(CONF_LOCALITY_PRESETS, default=selected_presets)] = (
            build_preset_selector(available_localities, "locality_presets")
        )
    fields[vol.Optional(CONF_LOCALITY_PATTERNS, default=patterns)] = (
        selector.ObjectSelector()
    )
    return vol.Schema(fields)


def _entry_value(entry: config_entries.ConfigEntry, key: str) -> list[str]:
    """Return an option list falling back to entry data."""
    value = entry.options.get(key, entry.data.get(key, []))
    if isinstance(value, list):
        return value
    if isinstance(value, str) and value:
        return [value]
    return []


class AerialDangerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Aerial Danger."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize config flow state."""
        self._name = DEFAULT_NAME
        self._sources: list[str] = []
        self._region_presets: list[str] = []
        self._region_patterns = list(DEFAULT_REGION_PATTERNS)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Collect the entry name and source entities."""
        errors: dict[str, str] = {}
        if user_input is not None:
            self._name = user_input[CONF_NAME]
            self._sources = user_input[CONF_SOURCES]
            if self._sources:
                return await self.async_step_regions()
            errors[CONF_SOURCES] = "sources_required"
        else:
            self._name = self.hass.config.location_name

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_NAME, default=self._name): str,
                    vol.Required(
                        CONF_SOURCES, default=self._sources
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(multiple=True)
                    ),
                }
            ),
            errors=errors,
        )

    async def async_step_regions(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Collect region presets and custom patterns."""
        errors: dict[str, str] = {}
        if user_input is not None:
            patterns = _validate_pattern_input(user_input.get(CONF_REGION_PATTERNS))
            if patterns is None:
                errors["base"] = "invalid_pattern_format"
            elif not _patterns_are_valid(patterns):
                errors["base"] = "invalid_pattern"
            else:
                self._region_presets = user_input.get(CONF_REGION_PRESETS, [])
                self._region_patterns = patterns
                return await self.async_step_localities()

        return self.async_show_form(
            step_id="regions",
            data_schema=build_regions_schema(
                self._region_presets, self._region_patterns
            ),
            errors=errors,
        )

    async def async_step_localities(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Collect locality presets and custom patterns."""
        errors: dict[str, str] = {}
        selected_localities: list[str] = []
        locality_patterns: list[str] = []
        if user_input is not None:
            locality_patterns_input = _validate_pattern_input(
                user_input.get(CONF_LOCALITY_PATTERNS)
            )
            if locality_patterns_input is None:
                errors["base"] = "invalid_pattern_format"
            elif not _patterns_are_valid(locality_patterns_input):
                errors["base"] = "invalid_pattern"
            else:
                locality_patterns = locality_patterns_input
                allowed = set(locality_ids(self._region_presets))
                selected_localities = [
                    preset
                    for preset in user_input.get(CONF_LOCALITY_PRESETS, [])
                    if preset in allowed
                ]
                regions = resolve_region_patterns(
                    self._region_patterns,
                    self._region_presets,
                )
                localities = resolve_locality_patterns(
                    locality_patterns,
                    self._region_presets,
                    selected_localities,
                )
                if not regions and not localities:
                    errors["base"] = "patterns_required"
                else:
                    return self.async_create_entry(
                        title=self._name,
                        data={
                            CONF_SOURCES: self._sources,
                            CONF_REGION_PRESETS: self._region_presets,
                            CONF_REGION_PATTERNS: self._region_patterns,
                            CONF_LOCALITY_PRESETS: selected_localities,
                            CONF_LOCALITY_PATTERNS: locality_patterns,
                        },
                    )

        return self.async_show_form(
            step_id="localities",
            data_schema=build_localities_schema(
                self._region_presets, selected_localities, locality_patterns
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        _config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Return the options flow handler."""
        return AerialDangerOptionsFlow()


class AerialDangerOptionsFlow(config_entries.OptionsFlow):
    """Handle an options flow for Aerial Danger."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Collect source entities."""
        current_sources = _entry_value(self.config_entry, CONF_SOURCES)
        errors: dict[str, str] = {}
        if user_input is not None:
            self._sources = user_input[CONF_SOURCES]
            if self._sources:
                return await self.async_step_regions()
            errors[CONF_SOURCES] = "sources_required"
            current_sources = self._sources

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SOURCES, default=current_sources
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(multiple=True)
                    )
                }
            ),
            errors=errors,
        )

    async def async_step_regions(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Collect region options."""
        current_presets = _entry_value(self.config_entry, CONF_REGION_PRESETS)
        current_patterns = _entry_value(self.config_entry, CONF_REGION_PATTERNS)
        errors: dict[str, str] = {}
        if user_input is not None:
            current_presets = user_input.get(CONF_REGION_PRESETS, [])
            patterns = _validate_pattern_input(user_input.get(CONF_REGION_PATTERNS))
            if patterns is None:
                errors["base"] = "invalid_pattern_format"
            elif not _patterns_are_valid(patterns):
                errors["base"] = "invalid_pattern"
                current_patterns = patterns
            else:
                self._region_presets = current_presets
                self._region_patterns = patterns
                return await self.async_step_localities()

        return self.async_show_form(
            step_id="regions",
            data_schema=build_regions_schema(current_presets, current_patterns),
            errors=errors,
        )

    async def async_step_localities(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Collect locality options and save them."""
        allowed = set(locality_ids(self._region_presets))
        current_presets = [
            preset
            for preset in _entry_value(self.config_entry, CONF_LOCALITY_PRESETS)
            if preset in allowed
        ]
        current_patterns = _entry_value(self.config_entry, CONF_LOCALITY_PATTERNS)
        errors: dict[str, str] = {}
        if user_input is not None:
            current_presets = [
                preset
                for preset in user_input.get(CONF_LOCALITY_PRESETS, [])
                if preset in allowed
            ]
            patterns = _validate_pattern_input(user_input.get(CONF_LOCALITY_PATTERNS))
            if patterns is None:
                errors["base"] = "invalid_pattern_format"
            elif not _patterns_are_valid(patterns):
                errors["base"] = "invalid_pattern"
                current_patterns = patterns
            else:
                current_patterns = patterns
                regions = resolve_region_patterns(
                    self._region_patterns,
                    self._region_presets,
                )
                localities = resolve_locality_patterns(
                    current_patterns,
                    self._region_presets,
                    current_presets,
                )
                if not regions and not localities:
                    errors["base"] = "patterns_required"
                else:
                    return self.async_create_entry(
                        title="",
                        data={
                            CONF_SOURCES: self._sources,
                            CONF_REGION_PRESETS: self._region_presets,
                            CONF_REGION_PATTERNS: self._region_patterns,
                            CONF_LOCALITY_PRESETS: current_presets,
                            CONF_LOCALITY_PATTERNS: current_patterns,
                        },
                    )

        return self.async_show_form(
            step_id="localities",
            data_schema=build_localities_schema(
                self._region_presets, current_presets, current_patterns
            ),
            errors=errors,
        )
