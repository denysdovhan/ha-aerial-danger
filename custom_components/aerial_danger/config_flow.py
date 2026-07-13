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
    CONF_NEIGHBORHOOD_PATTERNS,
    CONF_REGION_PATTERNS,
    CONF_SOURCES,
    DEFAULT_NAME,
    DOMAIN,
)
from .danger import DangerDetector

if TYPE_CHECKING:
    from homeassistant.data_entry_flow import FlowResult


def _split_lines(value: str | None) -> list[str]:
    """Split multiline text into a list of non-empty lines."""
    if not value:
        return []
    return [line.strip() for line in value.splitlines() if line.strip()]


def _patterns_are_valid(
    region_patterns: list[str],
    neighborhood_patterns: list[str],
) -> bool:
    """Return whether configured regex patterns compile."""
    try:
        DangerDetector.validate_patterns(region_patterns, neighborhood_patterns)
    except re.error:
        return False
    return True


def _validate_input(
    region_patterns: list[str],
    neighborhood_patterns: list[str],
    sources: list[str],
) -> dict[str, str]:
    """Validate normalized config or options input."""
    errors: dict[str, str] = {}
    if not region_patterns and not neighborhood_patterns:
        errors["base"] = "patterns_required"
    elif not _patterns_are_valid(region_patterns, neighborhood_patterns):
        errors["base"] = "invalid_pattern"
    if not sources:
        errors[CONF_SOURCES] = "sources_required"
    return errors


class AerialDangerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Aerial Danger."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            name = user_input[CONF_NAME]
            region_patterns = _split_lines(user_input.get(CONF_REGION_PATTERNS))
            neighborhood_patterns = _split_lines(
                user_input.get(CONF_NEIGHBORHOOD_PATTERNS)
            )
            sources: list[str] = user_input[CONF_SOURCES]
            errors = _validate_input(
                region_patterns,
                neighborhood_patterns,
                sources,
            )
            if not errors:
                return self.async_create_entry(
                    title=name,
                    data={
                        CONF_REGION_PATTERNS: region_patterns,
                        CONF_NEIGHBORHOOD_PATTERNS: neighborhood_patterns,
                        CONF_SOURCES: sources,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                    vol.Optional(CONF_REGION_PATTERNS): selector.TextSelector(
                        selector.TextSelectorConfig(multiline=True)
                    ),
                    vol.Optional(CONF_NEIGHBORHOOD_PATTERNS): selector.TextSelector(
                        selector.TextSelectorConfig(multiline=True)
                    ),
                    vol.Required(CONF_SOURCES, default=[]): selector.EntitySelector(
                        selector.EntitySelectorConfig(multiple=True)
                    ),
                },
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
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}
        if user_input is not None:
            user_input = dict(user_input)
            user_input[CONF_REGION_PATTERNS] = _split_lines(
                user_input.get(CONF_REGION_PATTERNS)
            )
            user_input[CONF_NEIGHBORHOOD_PATTERNS] = _split_lines(
                user_input.get(CONF_NEIGHBORHOOD_PATTERNS)
            )
            errors = _validate_input(
                user_input[CONF_REGION_PATTERNS],
                user_input[CONF_NEIGHBORHOOD_PATTERNS],
                user_input[CONF_SOURCES],
            )
            if not errors:
                user_input.pop(CONF_NAME, None)
                return self.async_create_entry(title="", data=user_input)

        data = self.config_entry.data
        options = self.config_entry.options

        def _join(value: list[str] | str | None) -> str:
            if isinstance(value, list):
                return "\n".join(value)
            return value or ""

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_REGION_PATTERNS,
                        default=_join(
                            options.get(
                                CONF_REGION_PATTERNS,
                                data.get(CONF_REGION_PATTERNS, []),
                            )
                        ),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(multiline=True)
                    ),
                    vol.Optional(
                        CONF_NEIGHBORHOOD_PATTERNS,
                        default=_join(
                            options.get(
                                CONF_NEIGHBORHOOD_PATTERNS,
                                data.get(CONF_NEIGHBORHOOD_PATTERNS, []),
                            )
                        ),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(multiline=True)
                    ),
                    vol.Required(
                        CONF_SOURCES,
                        default=options.get(CONF_SOURCES, data.get(CONF_SOURCES, [])),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(multiple=True)
                    ),
                }
            ),
            errors=errors,
        )
