"""Sensor platform for the Aerial Danger integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: ConfigEntry,  # noqa: ARG001
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up sensors for Aerial Danger."""
    # Sensors will be added once data predicates and channels are defined.
    async_add_entities([], update_before_add=False)
