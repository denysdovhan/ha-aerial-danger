"""Config flow for the Aerial Danger integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback

from .const import DEFAULT_NAME, DOMAIN

if TYPE_CHECKING:
    from homeassistant.data_entry_flow import FlowResult


class AerialDangerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Aerial Danger."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            name = user_input.get(CONF_NAME, DEFAULT_NAME)
            return self.async_create_entry(
                title=name,
                data={CONF_NAME: name},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
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

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )
