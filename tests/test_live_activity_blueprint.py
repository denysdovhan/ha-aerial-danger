"""Tests for the Live Activity automation blueprint."""

# ruff: noqa: S101

import asyncio
import shutil
from collections.abc import AsyncGenerator
from datetime import timedelta
from pathlib import Path

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_fire_time_changed,
    async_mock_service,
)

from custom_components.aerial_danger.const import (
    CONF_LOCALITY_PATTERNS,
    CONF_LOCALITY_PRESETS,
    CONF_REGION_PATTERNS,
    CONF_REGION_PRESETS,
    CONF_SOURCES,
    DOMAIN,
)

pytestmark = pytest.mark.usefixtures("enable_custom_integrations")

BLUEPRINT = (
    Path(__file__).parents[1] / "blueprints" / "aerial_danger_live_activity.yaml"
)
ALARM = "binary_sensor.kyiv_air"
SOURCE = "sensor.channel"
OTHER_SOURCE = "sensor.other_channel"
TAG = "aerial_danger_live_activity_kyiv_air"
DANGER = "🚀 Київ — балістика"
YELLOW = {
    "notification_icon": "mdi:alert",
    "notification_icon_color": "#eeee00",
    "color": "#eeee00",
    "background_color": "#333300",
}
RED = {
    "notification_icon": "mdi:alert-octagram",
    "notification_icon_color": "#ee0000",
    "color": "#ee0000",
    "background_color": "#330000",
}
GREEN = {
    "notification_icon": "mdi:emoticon-happy",
    "notification_icon_color": "#00ee00",
    "color": "#00ee00",
    "background_color": "#003300",
}


async def _add_phone(
    hass: HomeAssistant, name: str, *, notify_state: str | None = "unknown"
) -> str:
    """Register a mobile_app device, optionally with its notify entity."""
    entry = MockConfigEntry(domain="mobile_app", title=name)
    entry.add_to_hass(hass)
    device = dr.async_get(hass).async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={("mobile_app", entry.entry_id)},
        name=name,
    )
    if notify_state is not None:
        notify = er.async_get(hass).async_get_or_create(
            "notify",
            "mobile_app",
            entry.entry_id,
            config_entry=entry,
            device_id=device.id,
        )
        hass.states.async_set(notify.entity_id, notify_state)
    return device.id


async def _setup(
    hass: HomeAssistant,
    tmp_path: Path,
    phones: list[str],
    **inputs: object,
) -> None:
    """Set up Aerial Danger and an automation from the blueprint."""
    hass.config.config_dir = str(tmp_path)
    target = tmp_path / "blueprints" / "automation" / "test"
    target.mkdir(parents=True)
    shutil.copy(BLUEPRINT, target)

    hass.states.async_set(ALARM, "off")
    hass.states.async_set(SOURCE, "")
    hass.states.async_set(OTHER_SOURCE, "")
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_REGION_PRESETS: ["kyiv"],
            CONF_REGION_PATTERNS: [],
            CONF_LOCALITY_PRESETS: [],
            CONF_LOCALITY_PATTERNS: [],
            CONF_SOURCES: [SOURCE, OTHER_SOURCE],
        },
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    danger_device = next(
        device.id
        for device in dr.async_entries_for_config_entry(
            dr.async_get(hass), entry.entry_id
        )
    )

    assert await async_setup_component(
        hass,
        "automation",
        {
            "automation": {
                "id": "live_activity",
                "alias": "Live Activity",
                "use_blueprint": {
                    "path": "test/aerial_danger_live_activity.yaml",
                    "input": {
                        "air_alert_entity": ALARM,
                        "aerial_danger_device": danger_device,
                        "source_entities": [SOURCE, OTHER_SOURCE],
                        "mobile_devices": phones,
                        **inputs,
                    },
                },
            }
        },
    )
    await hass.async_block_till_done()
    assert hass.states.get("automation.live_activity") is not None


async def _settle() -> None:
    """
    Let automation runs progress.

    `async_block_till_done` would wait for runs paused in a hold.
    """
    for _ in range(50):
        await asyncio.sleep(0)


async def _set(hass: HomeAssistant, entity_id: str, state: str) -> None:
    hass.states.async_set(entity_id, state)
    await _settle()


async def _advance(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, seconds: float
) -> None:
    freezer.tick(timedelta(seconds=seconds))
    async_fire_time_changed(hass)
    await _settle()


@pytest.fixture
async def calls(hass: HomeAssistant) -> AsyncGenerator[list[ServiceCall]]:
    """
    Record notifications sent to the phone named "Phone".

    Stops the automation afterwards so no hold outlives the test.
    """
    yield async_mock_service(hass, "notify", "mobile_app_phone")
    if hass.states.get("automation.live_activity"):
        await hass.services.async_call(
            "automation",
            "turn_off",
            {"entity_id": "automation.live_activity"},
            blocking=True,
        )
        await hass.async_block_till_done()


async def test_alert_lifecycle(
    hass: HomeAssistant,
    tmp_path: Path,
    freezer: FrozenDateTimeFactory,
    calls: list[ServiceCall],
) -> None:
    """One activity follows an alert from start to all-clear."""
    await _setup(
        hass,
        tmp_path,
        [await _add_phone(hass, "Phone")],
        dashboard_path="/lovelace/0",
    )
    tap = {"url": "/lovelace/0", "clickAction": "/lovelace/0"}

    await _set(hass, ALARM, "on")
    assert calls[-1].data == {
        "title": "Тривога",
        "message": "Оголошено повітряну тривогу",
        "data": {"tag": TAG, "live_update": True, **YELLOW, **tap},
    }

    await _advance(hass, freezer, 10)
    await _set(hass, SOURCE, "Нових\nзагроз   немає")
    await _advance(hass, freezer, 1)
    assert calls[-1].data == {
        "title": "Тривога",
        "message": "Нових загроз немає",
        "data": {
            "tag": TAG,
            "live_update": True,
            **YELLOW,
            "silent": True,
            "alert_once": True,
            **tap,
        },
    }

    await _advance(hass, freezer, 10)
    sent = len(calls)
    await _set(hass, SOURCE, DANGER)
    await _advance(hass, freezer, 1)
    assert len(calls) == sent + 1
    assert calls[-1].data == {
        "title": "Небезпека",
        "message": DANGER,
        "data": {"tag": TAG, "live_update": True, **RED, **tap},
    }

    await _set(hass, ALARM, "off")
    assert calls[-1].data == {
        "title": "Відбій",
        "message": "Відбій повітряної тривоги",
        "data": {"tag": TAG, "live_update": True, **GREEN, **tap},
    }
    await _advance(hass, freezer, 30)
    assert calls[-1].data == {"message": "clear_notification", "data": {"tag": TAG}}


async def test_danger_before_alarm_starts_red(
    hass: HomeAssistant,
    tmp_path: Path,
    freezer: FrozenDateTimeFactory,
    calls: list[ServiceCall],
) -> None:
    """A danger reported shortly before Ukraine Alarm turns on is shown."""
    await _setup(hass, tmp_path, [await _add_phone(hass, "Phone")])

    await _set(hass, SOURCE, DANGER)
    assert calls == []
    await _advance(hass, freezer, 5)
    await _set(hass, ALARM, "on")
    assert calls[-1].data["title"] == "Небезпека"
    assert calls[-1].data["message"] == DANGER

    await _set(hass, ALARM, "off")
    await _advance(hass, freezer, 30)
    await _set(hass, SOURCE, "Загроза минула")
    await _set(hass, ALARM, "on")
    assert calls[-1].data["title"] == "Тривога"


async def test_danger_stays_red_while_active(
    hass: HomeAssistant,
    tmp_path: Path,
    freezer: FrozenDateTimeFactory,
    calls: list[ServiceCall],
) -> None:
    """Other channels' posts and outages keep an active danger red."""
    await _setup(hass, tmp_path, [await _add_phone(hass, "Phone")])
    await _set(hass, ALARM, "on")
    await _advance(hass, freezer, 10)
    await _set(hass, SOURCE, DANGER)
    sent = len(calls)

    await _advance(hass, freezer, 3)
    await _set(hass, OTHER_SOURCE, "Одещина — чисто")
    await _advance(hass, freezer, 15)
    await _set(hass, OTHER_SOURCE, "Харківщина — чисто")
    await _advance(hass, freezer, 15)
    assert len(calls) == sent

    await _advance(hass, freezer, 180)
    await _set(hass, ALARM, "unavailable")
    await _set(hass, ALARM, "on")
    assert calls[-1].data["title"] == "Небезпека"
    assert calls[-1].data["message"] == DANGER
    assert calls[-1].data["data"]["silent"] is True

    await _advance(hass, freezer, 15)
    await _set(hass, SOURCE, "Загроза минула")
    await _advance(hass, freezer, 1)
    assert calls[-1].data["title"] == "Тривога"
    assert calls[-1].data["message"] == "Загроза минула"


async def test_held_messages_shown_after_hold(
    hass: HomeAssistant,
    tmp_path: Path,
    freezer: FrozenDateTimeFactory,
    calls: list[ServiceCall],
) -> None:
    """Messages during a hold are not lost; the newest follows the hold."""
    await _setup(hass, tmp_path, [await _add_phone(hass, "Phone")])
    await _set(hass, ALARM, "on")
    await _advance(hass, freezer, 10)

    await _set(hass, SOURCE, DANGER)
    await _advance(hass, freezer, 5)
    await _set(hass, SOURCE, "Перша")
    await _set(hass, SOURCE, "Загроза минула")
    sent = len(calls)
    await _advance(hass, freezer, 5)
    assert len(calls) == sent

    await _advance(hass, freezer, 5)
    assert len(calls) == sent + 1
    assert calls[-1].data["title"] == "Тривога"
    assert calls[-1].data["message"] == "Загроза минула"
    assert calls[-1].data["data"]["silent"] is True


async def test_danger_burst_alerts_once(
    hass: HomeAssistant,
    tmp_path: Path,
    freezer: FrozenDateTimeFactory,
    calls: list[ServiceCall],
) -> None:
    """Detections in quick succession update quietly."""
    await _setup(hass, tmp_path, [await _add_phone(hass, "Phone")])
    await _set(hass, ALARM, "on")
    await _advance(hass, freezer, 10)

    await _set(hass, SOURCE, DANGER)
    assert "silent" not in calls[-1].data["data"]
    await _advance(hass, freezer, 2)
    await _set(hass, SOURCE, "Балістика на Київ!")
    assert calls[-1].data["title"] == "Небезпека"
    assert calls[-1].data["data"]["silent"] is True


async def test_alarm_sensor_outage(
    hass: HomeAssistant,
    tmp_path: Path,
    freezer: FrozenDateTimeFactory,
    calls: list[ServiceCall],
) -> None:
    """Ukraine Alarm outages neither re-alert nor leave the activity stuck."""
    await _setup(hass, tmp_path, [await _add_phone(hass, "Phone")])
    await _set(hass, ALARM, "on")
    await _advance(hass, freezer, 10)

    await _set(hass, ALARM, "unavailable")
    await _set(hass, ALARM, "on")
    assert calls[-1].data["data"]["silent"] is True
    await _advance(hass, freezer, 10)

    sent = len(calls)
    await _set(hass, ALARM, "unavailable")
    await _set(hass, ALARM, "off")
    assert [call.data for call in calls[sent:]] == [
        {"message": "clear_notification", "data": {"tag": TAG}}
    ]


async def test_idle_outage_sends_nothing(
    hass: HomeAssistant,
    tmp_path: Path,
    calls: list[ServiceCall],
) -> None:
    """Without a recent alert, Ukraine Alarm recovering to off is silent."""
    await _setup(hass, tmp_path, [await _add_phone(hass, "Phone")])
    await _set(hass, ALARM, "unavailable")
    await _set(hass, ALARM, "off")
    assert calls == []


async def test_without_sources(
    hass: HomeAssistant,
    tmp_path: Path,
    freezer: FrozenDateTimeFactory,
    calls: list[ServiceCall],
) -> None:
    """Sources are optional: start, danger, and all-clear still work."""
    await _setup(hass, tmp_path, [await _add_phone(hass, "Phone")], source_entities=[])
    await _set(hass, ALARM, "on")
    await _advance(hass, freezer, 10)
    await _set(hass, SOURCE, DANGER)
    await _set(hass, ALARM, "off")
    await _advance(hass, freezer, 30)
    assert [call.data.get("title") for call in calls] == [
        "Тривога",
        "Небезпека",
        "Відбій",
        None,
    ]


async def test_phones(
    hass: HomeAssistant,
    tmp_path: Path,
    calls: list[ServiceCall],
) -> None:
    """Only push-capable phones are notified, each action once."""
    other = async_mock_service(hass, "notify", "mobile_app_iphone_darina")
    phones = [
        await _add_phone(hass, "Without push", notify_state=None),
        await _add_phone(hass, "Stale", notify_state="unavailable"),
        await _add_phone(hass, "Phone"),
        await _add_phone(hass, "Phone"),
        await _add_phone(hass, "iPhone Дарина"),
    ]
    await _setup(hass, tmp_path, phones)

    await _set(hass, ALARM, "on")
    assert len(calls) == 1
    assert len(other) == 1
    assert "url" not in calls[0].data["data"]
