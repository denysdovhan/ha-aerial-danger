"""Config flow for the Aerial Danger integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_CITY_PATTERNS,
    CONF_NEIGHBORHOOD_PATTERNS,
    CONF_SOURCES,
    DEFAULT_NAME,
    DOMAIN,
)

if TYPE_CHECKING:
    from homeassistant.data_entry_flow import FlowResult


class AerialDangerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Aerial Danger."""

    VERSION = 1

    @staticmethod
    def _split_lines(value: str | None) -> list[str]:
        """Split multiline text into a list of non-empty lines."""
        if not value:
            return []
        return [line.strip() for line in value.splitlines() if line.strip()]

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            name = user_input.get(CONF_NAME, DEFAULT_NAME)
            city_patterns = self._split_lines(user_input.get(CONF_CITY_PATTERNS))
            neighborhood_patterns = self._split_lines(
                user_input.get(CONF_NEIGHBORHOOD_PATTERNS)
            )
            sources: list[str] = user_input.get(CONF_SOURCES, [])
            return self.async_create_entry(
                title=name,
                data={
                    CONF_NAME: name,
                    CONF_CITY_PATTERNS: city_patterns,
                    CONF_NEIGHBORHOOD_PATTERNS: neighborhood_patterns,
                    CONF_SOURCES: sources,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                    vol.Optional(CONF_CITY_PATTERNS): selector.TextSelector(
                        selector.TextSelectorConfig(multiline=True)
                    ),
                    vol.Optional(CONF_NEIGHBORHOOD_PATTERNS): selector.TextSelector(
                        selector.TextSelectorConfig(multiline=True)
                    ),
                    vol.Optional(CONF_SOURCES, default=[]): selector.EntitySelector(
                        selector.EntitySelectorConfig(multiple=True)
                    ),
                },
            ),
        )

    @callback
    def async_get_options_flow(
        self,
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Return the options flow handler."""
        return AerialDangerOptionsFlow(config_entry)


class AerialDangerOptionsFlow(config_entries.OptionsFlow):
    """Handle an options flow for Aerial Danger."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    @staticmethod
    def _split_lines(value: str | None) -> list[str]:
        if not value:
            return []
        return [line.strip() for line in value.splitlines() if line.strip()]

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            user_input = dict(user_input)
            user_input[CONF_CITY_PATTERNS] = self._split_lines(
                user_input.get(CONF_CITY_PATTERNS)
            )
            user_input[CONF_NEIGHBORHOOD_PATTERNS] = self._split_lines(
                user_input.get(CONF_NEIGHBORHOOD_PATTERNS)
            )
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
                        CONF_NAME,
                        default=options.get(
                            CONF_NAME, data.get(CONF_NAME, DEFAULT_NAME)
                        ),
                    ): str,
                    vol.Optional(
                        CONF_CITY_PATTERNS,
                        default=_join(
                            options.get(
                                CONF_CITY_PATTERNS, data.get(CONF_CITY_PATTERNS, [])
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
                    vol.Optional(
                        CONF_SOURCES,
                        default=options.get(CONF_SOURCES, data.get(CONF_SOURCES, [])),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(multiple=True)
                    ),
                }
            ),
        )
