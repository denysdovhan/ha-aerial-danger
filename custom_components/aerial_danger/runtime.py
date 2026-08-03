"""Runtime data for the Aerial Danger integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .const import (
    STATE_BALLISTIC,
    STATE_CRUISE,
    STATE_DANGER,
    STATE_DRONE,
    STATE_GUIDED_BOMB,
    STATE_IRBM,
    STATE_MLRS,
    STATE_UNKNOWN_DANGER,
)
from .danger import DangerDetector, DangerType, Detection

if TYPE_CHECKING:
    from collections.abc import Callable
    from datetime import datetime

    from homeassistant.helpers.entity import Entity

    from .event import AerialDangerEvent


DANGER_TYPE_STATE_KEYS = {
    DangerType.IRBM: STATE_IRBM,
    DangerType.MLRS: STATE_MLRS,
    DangerType.GUIDED_BOMB: STATE_GUIDED_BOMB,
    DangerType.BALLISTIC: STATE_BALLISTIC,
    DangerType.CRUISE: STATE_CRUISE,
    DangerType.DRONE: STATE_DRONE,
    DangerType.GENERIC: STATE_UNKNOWN_DANGER,
}


@dataclass(frozen=True)
class SourceDetection:
    """Represent the latest active detection from one source."""

    source_entity_id: str
    detection: Detection
    updated_at: datetime


@dataclass
class RuntimeData:
    """Keep runtime objects for an entry."""

    detector: DangerDetector
    active_detections: dict[str, SourceDetection]
    states: dict[str, bool]
    last_detection: dict[DangerType, SourceDetection | None]
    latest_detection: SourceDetection | None
    entities: set[Entity]
    event_entity: AerialDangerEvent | None
    unsub: Callable[[], None] | None


def derive_danger_state(
    active_detections: dict[str, SourceDetection],
) -> tuple[
    dict[str, bool],
    dict[DangerType, SourceDetection | None],
    SourceDetection | None,
]:
    """Derive entry state from active source detections."""
    states = {
        STATE_IRBM: False,
        STATE_MLRS: False,
        STATE_GUIDED_BOMB: False,
        STATE_BALLISTIC: False,
        STATE_CRUISE: False,
        STATE_DRONE: False,
        STATE_UNKNOWN_DANGER: False,
        STATE_DANGER: False,
    }
    last_detection: dict[DangerType, SourceDetection | None] = {
        DangerType.IRBM: None,
        DangerType.MLRS: None,
        DangerType.GUIDED_BOMB: None,
        DangerType.BALLISTIC: None,
        DangerType.CRUISE: None,
        DangerType.DRONE: None,
        DangerType.GENERIC: None,
    }
    latest_detection: SourceDetection | None = None

    for source_detection in active_detections.values():
        danger_type = source_detection.detection.type
        if danger_type is None:
            continue

        states[DANGER_TYPE_STATE_KEYS[danger_type]] = True
        current = last_detection[danger_type]
        if current is None or (
            source_detection.updated_at,
            source_detection.source_entity_id,
        ) > (current.updated_at, current.source_entity_id):
            last_detection[danger_type] = source_detection

        if latest_detection is None or (
            source_detection.updated_at,
            source_detection.source_entity_id,
        ) > (latest_detection.updated_at, latest_detection.source_entity_id):
            latest_detection = source_detection

    states[STATE_DANGER] = any(
        states[state_key] for state_key in DANGER_TYPE_STATE_KEYS.values()
    )
    return states, last_detection, latest_detection
