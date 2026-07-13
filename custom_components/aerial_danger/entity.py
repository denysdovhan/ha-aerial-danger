"""Base entity for the Aerial Danger integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers.entity import DeviceInfo, Entity

from .const import DOMAIN

if TYPE_CHECKING:
    from . import AerialDangerConfigEntry
    from .runtime import RuntimeData


class AerialDangerEntity(Entity):
    """Base class for Aerial Danger entities."""

    _attr_has_entity_name = True

    def __init__(self, entry: AerialDangerConfigEntry) -> None:
        """Initialize the entity."""
        self._runtime: RuntimeData = entry.runtime_data
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
        )
