"""Triggers for the Aerial Danger integration."""

from typing import ClassVar, override

from homeassistant.components.event import ATTR_EVENT_TYPE
from homeassistant.components.event import DOMAIN as EVENT_DOMAIN
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.automation import DomainSpec
from homeassistant.helpers.trigger import (
    NotTriggeredReasonReporter,
    StatelessEntityTriggerBase,
    Trigger,
    TriggerConfig,
)

from .const import EVENT_TYPES, STATE_DANGER


class DangerDetectedTrigger(StatelessEntityTriggerBase):
    """Trigger when a matching danger event is detected."""

    _domain_specs: ClassVar = {EVENT_DOMAIN: DomainSpec()}

    def __init__(self, hass: HomeAssistant, config: TriggerConfig) -> None:
        """Initialize the danger trigger."""
        super().__init__(hass, config)
        trigger_type = config.key.rsplit(".", 1)[-1]
        self._event_types = (
            EVENT_TYPES if trigger_type == STATE_DANGER else [trigger_type]
        )

    @override
    def is_valid_state(
        self,
        state: State,
        report_not_triggered: NotTriggeredReasonReporter,
    ) -> bool:
        """Check if the event type matches the selected danger."""
        return state.attributes.get(ATTR_EVENT_TYPE) in self._event_types

    @override
    def is_valid_transition(self, from_state: State, to_state: State) -> bool:
        """Accept every event entity update."""
        return True


TRIGGERS: dict[str, type[Trigger]] = dict.fromkeys(
    [STATE_DANGER, *EVENT_TYPES],
    DangerDetectedTrigger,
)


async def async_get_triggers(
    hass: HomeAssistant,  # noqa: ARG001
) -> dict[str, type[Trigger]]:
    """Return Aerial Danger triggers."""
    return TRIGGERS
