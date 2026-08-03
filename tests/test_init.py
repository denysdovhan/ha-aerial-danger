"""Tests for the Aerial Danger integration setup."""

# ruff: noqa: S101

import pytest
from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN
from homeassistant.components.event import (
    ATTR_EVENT_TYPE,
)
from homeassistant.components.event import (
    DOMAIN as EVENT_DOMAIN,
)
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import (
    ATTR_FRIENDLY_NAME,
    CONF_NAME,
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    EntityCategory,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.translation import async_get_translations
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.aerial_danger import RuntimeData
from custom_components.aerial_danger.const import (
    ATTR_MATCHED_AREA,
    ATTR_MATCHED_DANGER,
    ATTR_MATCHED_MESSAGE,
    ATTR_SOURCE_ENTITY_ID,
    ATTR_TIMESTAMP,
    CONF_LOCALITY_PATTERNS,
    CONF_LOCALITY_PRESETS,
    CONF_REGION_PATTERNS,
    CONF_REGION_PRESETS,
    CONF_SOURCES,
    DEFAULT_NAME,
    DOMAIN,
    EVENT_TYPE_BALLISTIC,
    EVENT_TYPE_CRUISE,
    EVENT_TYPE_DRONE,
    EVENT_TYPE_GUIDED_BOMB,
    EVENT_TYPE_IRBM,
    EVENT_TYPE_MLRS,
    EVENT_TYPE_UNKNOWN,
    MATCHED_AREA,
    MATCHED_DANGER,
    MATCHED_MESSAGE,
    MATCHED_SOURCE,
    STATE_CLEAR,
    STATE_NATIONWIDE,
)

pytestmark = pytest.mark.usefixtures("enable_custom_integrations")
EXPECTED_ENTITY_COUNT = 12
DETECTION_ATTRIBUTE_KEYS = (
    ATTR_MATCHED_MESSAGE,
    ATTR_MATCHED_AREA,
    ATTR_MATCHED_DANGER,
    ATTR_SOURCE_ENTITY_ID,
)
DIAGNOSTIC_SENSOR_KEYS = (
    MATCHED_MESSAGE,
    MATCHED_AREA,
    MATCHED_DANGER,
    MATCHED_SOURCE,
)


def _entry(
    data: dict[str, object],
    *,
    title: str = DEFAULT_NAME,
) -> MockConfigEntry:
    """Create an Aerial Danger mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title=title,
        data=data,
    )


def _entity_id(
    hass: HomeAssistant,
    entry: MockConfigEntry,
    key: str,
) -> str:
    """Return an entity ID for an entry sensor key."""
    entity_id = er.async_get(hass).async_get_entity_id(
        BINARY_SENSOR_DOMAIN,
        DOMAIN,
        f"{entry.entry_id}_{key}",
    )
    assert entity_id is not None
    return entity_id


def _event_entity_id(
    hass: HomeAssistant,
    entry: MockConfigEntry,
) -> str:
    """Return the event entity ID for an entry."""
    entity_id = er.async_get(hass).async_get_entity_id(
        EVENT_DOMAIN,
        DOMAIN,
        f"{entry.entry_id}_danger_event",
    )
    assert entity_id is not None
    return entity_id


def _diagnostic_sensor_id(
    hass: HomeAssistant,
    entry: MockConfigEntry,
    key: str,
) -> str:
    """Return a diagnostic sensor entity ID for an entry."""
    entity_id = er.async_get(hass).async_get_entity_id(
        SENSOR_DOMAIN,
        DOMAIN,
        f"{entry.entry_id}_{key}",
    )
    assert entity_id is not None
    return entity_id


async def test_setup_stores_runtime_data_on_entry(
    hass: HomeAssistant,
) -> None:
    """Test setup stores runtime data on the config entry."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    config_entry = hass.config_entries.async_get_entry(entry.entry_id)
    assert config_entry is not None
    assert config_entry.state is ConfigEntryState.LOADED
    assert isinstance(config_entry.runtime_data, RuntimeData)
    assert len(config_entry.runtime_data.entities) == EXPECTED_ENTITY_COUNT


async def test_setup_resolves_preset_patterns(hass: HomeAssistant) -> None:
    """Test runtime detector uses current preset definitions."""
    entry = _entry(
        {
            CONF_REGION_PRESETS: ["kyiv"],
            CONF_REGION_PATTERNS: [],
            CONF_LOCALITY_PRESETS: ["kyiv_nyvky"],
            CONF_LOCALITY_PATTERNS: [],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    hass.states.async_set("sensor.alerts", "На Нивках БПЛА!")
    await hass.async_block_till_done()
    assert hass.states.get(_entity_id(hass, entry, "drone")).state == STATE_ON


async def test_setup_seeds_source_state_without_firing_event(
    hass: HomeAssistant,
) -> None:
    """Test setup seeds current source state without firing danger events."""
    hass.states.async_set("sensor.alerts", "Київ швидкісна!")
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get(_entity_id(hass, entry, "ballistic"))
    assert state.state == STATE_ON
    assert state.attributes[ATTR_MATCHED_MESSAGE] == "Київ швидкісна!"
    assert state.attributes[ATTR_MATCHED_AREA] == "Київ"
    assert state.attributes[ATTR_MATCHED_DANGER] == "Київ швидкісна"
    assert state.attributes[ATTR_SOURCE_ENTITY_ID] == "sensor.alerts"
    assert hass.states.get(_event_entity_id(hass, entry)).state == STATE_UNKNOWN


async def test_setup_seeds_first_match_from_each_source(
    hass: HomeAssistant,
) -> None:
    """Test setup keeps the first match from every active source."""
    hass.states.async_set("sensor.channel_a", "Циркон на Київ!")
    hass.states.async_set("sensor.channel_b", "Шахед на Нивки!")
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.channel_a", "sensor.channel_b"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    for key in ("ballistic", "drone", "danger"):
        assert hass.states.get(_entity_id(hass, entry, key)).state == STATE_ON
    for key in ("irbm", "mlrs", "guided_bomb", "cruise", "unknown"):
        assert hass.states.get(_entity_id(hass, entry, key)).state == STATE_OFF
    assert hass.states.get(_event_entity_id(hass, entry)).state == STATE_UNKNOWN


async def test_entry_title_rename_updates_device_name(hass: HomeAssistant) -> None:
    """Test native entry rename updates the integration device name."""
    entry = _entry(
        {
            CONF_NAME: "Legacy name",
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.alerts"],
        },
        title="Kyiv alerts",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    device_registry = dr.async_get(hass)
    device = device_registry.async_get_device(identifiers={(DOMAIN, entry.entry_id)})
    assert device is not None
    assert device.name == "Kyiv alerts"

    hass.config_entries.async_update_entry(entry, title="Renamed alerts")
    await hass.async_block_till_done()

    device = device_registry.async_get_device(identifiers={(DOMAIN, entry.entry_id)})
    assert device is not None
    assert entry.title == "Renamed alerts"
    assert device.name == "Renamed alerts"


async def test_source_state_updates_binary_sensors(
    hass: HomeAssistant,
) -> None:
    """Test source state changes update binary sensors."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.aerial_danger_ballistic_danger").state == (
        STATE_OFF
    )
    for key in (
        "irbm",
        "mlrs",
        "guided_bomb",
        "ballistic",
        "cruise",
        "drone",
        "unknown",
        "danger",
    ):
        state = hass.states.get(_entity_id(hass, entry, key))
        assert all(state.attributes[attr] is None for attr in DETECTION_ATTRIBUTE_KEYS)

    hass.states.async_set("sensor.alerts", "Київ швидкісна!")
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.aerial_danger_ballistic_danger").state == (
        STATE_ON
    )
    assert hass.states.get("binary_sensor.aerial_danger_danger").state == STATE_ON

    hass.states.async_set("sensor.alerts", "Загроза БРСД.")
    await hass.async_block_till_done()

    assert hass.states.get(_entity_id(hass, entry, "irbm")).state == STATE_ON
    assert hass.states.get(_entity_id(hass, entry, "ballistic")).state == STATE_OFF


@pytest.mark.parametrize(
    ("message", "sensor_key"),
    [
        ("🔴❗️ РСЗВ на Харків!", "mlrs"),
        ("💣 КАБ у напрямку Харків.", "guided_bomb"),
    ],
)
async def test_new_danger_types_update_binary_sensors(
    hass: HomeAssistant,
    message: str,
    sensor_key: str,
) -> None:
    """Test MLRS and guided bomb messages update their binary sensors."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [],
            CONF_LOCALITY_PATTERNS: [r"\bхарків\b"],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    hass.states.async_set("sensor.alerts", message)
    await hass.async_block_till_done()

    state = hass.states.get(_entity_id(hass, entry, sensor_key))
    assert state.state == STATE_ON
    assert state.attributes[ATTR_MATCHED_MESSAGE] == message
    assert state.attributes[ATTR_MATCHED_AREA] == "Харків"
    assert state.attributes[ATTR_SOURCE_ENTITY_ID] == "sensor.alerts"


@pytest.mark.parametrize(
    ("message", "sensor_key"),
    [
        ("🔴❗️ РСЗВ на Харків!", "mlrs"),
        ("💣 КАБ у напрямку Харків.", "guided_bomb"),
    ],
)
async def test_new_danger_types_ignore_region_patterns(
    hass: HomeAssistant,
    message: str,
    sensor_key: str,
) -> None:
    """Test MLRS and guided bomb sensors require locality patterns."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [r"\bхарків\b"],
            CONF_LOCALITY_PATTERNS: [],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    hass.states.async_set("sensor.alerts", message)
    await hass.async_block_till_done()

    assert hass.states.get(_entity_id(hass, entry, sensor_key)).state == STATE_OFF


async def test_non_matching_source_message_preserves_detection(
    hass: HomeAssistant,
) -> None:
    """Test non-matching messages neither replace nor clear active danger."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [],
            CONF_LOCALITY_PATTERNS: [r"\bхарків\b"],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    guided_bomb_id = _entity_id(hass, entry, "guided_bomb")
    alert = "💣 КАБ у напрямку Харків."
    hass.states.async_set("sensor.alerts", alert)
    await hass.async_block_till_done()

    hass.states.async_set(
        "sensor.alerts",
        "Аналітика: дальність КАБ до Харкова.",
    )
    await hass.async_block_till_done()

    state = hass.states.get(guided_bomb_id)
    assert state.state == STATE_ON
    assert state.attributes[ATTR_MATCHED_MESSAGE] == alert

    hass.states.async_set(
        "sensor.alerts",
        "Су-34 може йти на пуски КАБ в бік Харкова.",
    )
    await hass.async_block_till_done()

    state = hass.states.get(guided_bomb_id)
    assert state.state == STATE_ON
    assert state.attributes[ATTR_MATCHED_MESSAGE] == alert

    hass.states.async_set("sensor.alerts", "Відбій.")
    await hass.async_block_till_done()

    assert hass.states.get(guided_bomb_id).state == STATE_OFF


async def test_diagnostic_sensors_mirror_aggregate_detection(
    hass: HomeAssistant,
) -> None:
    """Test diagnostic sensors mirror aggregate match details."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    sensor_ids = {
        key: _diagnostic_sensor_id(hass, entry, key) for key in DIAGNOSTIC_SENSOR_KEYS
    }
    entity_registry = er.async_get(hass)
    for entity_id in sensor_ids.values():
        assert hass.states.get(entity_id).state == STATE_CLEAR
        assert (
            entity_registry.async_get(entity_id).entity_category
            is EntityCategory.DIAGNOSTIC
        )

    hass.states.async_set(
        "sensor.alerts",
        "Київ швидкісна!",
        {ATTR_FRIENDLY_NAME: "Telegram alerts"},
    )
    await hass.async_block_till_done()

    assert hass.states.get(sensor_ids[MATCHED_MESSAGE]).state == "Київ швидкісна!"
    assert hass.states.get(sensor_ids[MATCHED_AREA]).state == "Київ"
    assert hass.states.get(sensor_ids[MATCHED_DANGER]).state == "Київ швидкісна"
    assert hass.states.get(sensor_ids[MATCHED_SOURCE]).state == "Telegram alerts"

    hass.states.async_set("sensor.alerts", "Все тихо")
    await hass.async_block_till_done()
    for entity_id in sensor_ids.values():
        assert hass.states.get(entity_id).state == STATE_CLEAR

    hass.states.async_set("sensor.alerts", "Загроза БРСД.")
    await hass.async_block_till_done()
    assert hass.states.get(sensor_ids[MATCHED_AREA]).state == STATE_NATIONWIDE


@pytest.mark.parametrize(
    ("language", "clear", "nationwide"),
    [
        ("en", "Clear", "Nationwide"),
        ("uk", "Немає", "Вся країна"),
    ],
)
async def test_diagnostic_sensor_state_translations(
    hass: HomeAssistant,
    language: str,
    clear: str,
    nationwide: str,
) -> None:
    """Test diagnostic sensor states have backend translations."""
    translations = await async_get_translations(hass, language, "entity", {DOMAIN})
    prefix = f"component.{DOMAIN}.entity.sensor"

    for key in DIAGNOSTIC_SENSOR_KEYS:
        assert translations[f"{prefix}.{key}.state.clear"] == clear
    assert translations[f"{prefix}.{MATCHED_AREA}.state.nationwide"] == nationwide


async def test_aggregate_attributes_use_latest_active_detection(
    hass: HomeAssistant,
) -> None:
    """Test aggregate attributes follow the latest active detection."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.channel_a", "sensor.channel_b"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    danger_id = _entity_id(hass, entry, "danger")
    hass.states.async_set("sensor.channel_a", "Київ швидкісна!")
    await hass.async_block_till_done()
    hass.states.async_set("sensor.channel_b", "Нивки над вами БПЛА!")
    await hass.async_block_till_done()

    state = hass.states.get(danger_id)
    assert state.attributes[ATTR_MATCHED_MESSAGE] == "Нивки над вами БПЛА!"
    assert state.attributes[ATTR_SOURCE_ENTITY_ID] == "sensor.channel_b"

    hass.states.async_set("sensor.channel_b", "Все тихо")
    await hass.async_block_till_done()

    state = hass.states.get(danger_id)
    assert state.state == STATE_ON
    assert state.attributes[ATTR_MATCHED_MESSAGE] == "Київ швидкісна!"
    assert state.attributes[ATTR_SOURCE_ENTITY_ID] == "sensor.channel_a"


async def test_multiple_sources_keep_aggregate_danger_on(
    hass: HomeAssistant,
) -> None:
    """Test first matches from every source keep aggregate danger on."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.channel_a", "sensor.channel_b"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    ballistic_id = _entity_id(hass, entry, "ballistic")
    cruise_id = _entity_id(hass, entry, "cruise")
    drone_id = _entity_id(hass, entry, "drone")
    unknown_id = _entity_id(hass, entry, "unknown")
    danger_id = _entity_id(hass, entry, "danger")

    hass.states.async_set("sensor.channel_a", "Циркон на Київ!")
    await hass.async_block_till_done()
    hass.states.async_set("sensor.channel_b", "Шахед на Нивки!")
    await hass.async_block_till_done()

    assert hass.states.get(ballistic_id).state == STATE_ON
    assert hass.states.get(cruise_id).state == STATE_OFF
    assert hass.states.get(drone_id).state == STATE_ON
    assert hass.states.get(unknown_id).state == STATE_OFF
    assert hass.states.get(danger_id).state == STATE_ON

    hass.states.async_set("sensor.channel_a", "Все тихо")
    await hass.async_block_till_done()

    assert hass.states.get(ballistic_id).state == STATE_OFF
    assert hass.states.get(cruise_id).state == STATE_OFF
    assert hass.states.get(drone_id).state == STATE_ON
    assert hass.states.get(unknown_id).state == STATE_OFF
    assert hass.states.get(danger_id).state == STATE_ON

    hass.states.async_set("sensor.channel_b", "Все тихо")
    await hass.async_block_till_done()

    assert hass.states.get(drone_id).state == STATE_OFF
    assert hass.states.get(danger_id).state == STATE_OFF


async def test_latest_active_source_supplies_attributes(
    hass: HomeAssistant,
) -> None:
    """Test attributes use the latest active source for a danger type."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.channel_a", "sensor.channel_b"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    ballistic_id = _entity_id(hass, entry, "ballistic")
    hass.states.async_set("sensor.channel_a", "Київ швидкісна!")
    await hass.async_block_till_done()
    hass.states.async_set("sensor.channel_b", "Київ спуск!")
    await hass.async_block_till_done()

    state = hass.states.get(ballistic_id)
    assert state.attributes[ATTR_MATCHED_MESSAGE] == "Київ спуск!"
    assert state.attributes[ATTR_SOURCE_ENTITY_ID] == "sensor.channel_b"

    hass.states.async_set("sensor.channel_b", "Все тихо")
    await hass.async_block_till_done()

    state = hass.states.get(ballistic_id)
    assert state.state == STATE_ON
    assert state.attributes[ATTR_MATCHED_MESSAGE] == "Київ швидкісна!"
    assert state.attributes[ATTR_SOURCE_ENTITY_ID] == "sensor.channel_a"


@pytest.mark.parametrize("unavailable_state", [STATE_UNKNOWN, STATE_UNAVAILABLE])
async def test_unavailable_source_preserves_detection(
    hass: HomeAssistant,
    unavailable_state: str,
) -> None:
    """Test unavailable source states do not clear active detection."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    ballistic_id = _entity_id(hass, entry, "ballistic")
    hass.states.async_set("sensor.alerts", "Київ швидкісна!")
    await hass.async_block_till_done()
    hass.states.async_set("sensor.alerts", unavailable_state)
    await hass.async_block_till_done()

    state = hass.states.get(ballistic_id)
    assert state.state == STATE_ON
    assert state.attributes[ATTR_MATCHED_MESSAGE] == "Київ швидкісна!"


async def test_overlapping_entries_are_isolated(hass: HomeAssistant) -> None:
    """Test entries can share a source and unload independently."""
    data = {
        CONF_REGION_PATTERNS: [r"\bкиїв\b"],
        CONF_LOCALITY_PATTERNS: [],
        CONF_SOURCES: ["sensor.alerts"],
    }
    entry_a = _entry(data, title="Provider A")
    entry_b = _entry(data, title="Provider B")
    entry_a.add_to_hass(hass)
    entry_b.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry_a.entry_id)
    await hass.async_block_till_done()
    assert entry_b.state is ConfigEntryState.LOADED

    ballistic_a = _entity_id(hass, entry_a, "ballistic")
    ballistic_b = _entity_id(hass, entry_b, "ballistic")
    event_a = _event_entity_id(hass, entry_a)
    hass.states.async_set("sensor.alerts", "Київ швидкісна!")
    await hass.async_block_till_done()

    assert hass.states.get(ballistic_a).state == STATE_ON
    assert hass.states.get(ballistic_b).state == STATE_ON

    assert await hass.config_entries.async_unload(entry_a.entry_id)
    await hass.async_block_till_done()
    hass.states.async_set("sensor.alerts", "Все тихо")
    await hass.async_block_till_done()

    assert hass.states.get(ballistic_a).state == STATE_UNAVAILABLE
    assert hass.states.get(ballistic_b).state == STATE_OFF
    assert hass.states.get(event_a).state == STATE_UNAVAILABLE


async def test_same_type_detection_refreshes_attributes(
    hass: HomeAssistant,
) -> None:
    """Test same-type detections refresh entity attributes."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    hass.states.async_set("sensor.alerts", "Київ швидкісна!")
    await hass.async_block_till_done()
    assert hass.states.get("binary_sensor.aerial_danger_ballistic_danger").state == (
        STATE_ON
    )
    assert hass.states.get("binary_sensor.aerial_danger_danger").state == STATE_ON
    assert (
        hass.states.get("binary_sensor.aerial_danger_ballistic_danger").attributes[
            ATTR_MATCHED_MESSAGE
        ]
        == "Київ швидкісна!"
    )
    event_entity_id = _event_entity_id(hass, entry)
    event_state = hass.states.get(event_entity_id)
    assert event_state.attributes[ATTR_EVENT_TYPE] == EVENT_TYPE_BALLISTIC
    assert event_state.attributes[ATTR_MATCHED_MESSAGE] == "Київ швидкісна!"
    assert event_state.attributes[ATTR_MATCHED_AREA] == "Київ"
    assert event_state.attributes[ATTR_MATCHED_DANGER] == "Київ швидкісна"
    assert event_state.attributes[ATTR_SOURCE_ENTITY_ID] == "sensor.alerts"
    assert ATTR_TIMESTAMP in event_state.attributes

    hass.states.async_set("sensor.alerts", "Київ спуск!")
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.aerial_danger_ballistic_danger").state == (
        STATE_ON
    )
    assert hass.states.get("binary_sensor.aerial_danger_danger").state == STATE_ON
    assert (
        hass.states.get("binary_sensor.aerial_danger_ballistic_danger").attributes[
            ATTR_MATCHED_MESSAGE
        ]
        == "Київ спуск!"
    )
    assert (
        hass.states.get("binary_sensor.aerial_danger_ballistic_danger").attributes[
            ATTR_SOURCE_ENTITY_ID
        ]
        == "sensor.alerts"
    )
    event_state = hass.states.get(event_entity_id)
    assert event_state.attributes[ATTR_EVENT_TYPE] == EVENT_TYPE_BALLISTIC
    assert event_state.attributes[ATTR_MATCHED_MESSAGE] == "Київ спуск!"


@pytest.mark.parametrize(
    ("message", "event_type"),
    [
        ("Загроза БРСД.", EVENT_TYPE_IRBM),
        ("🔴❗️ РСЗВ на Харків!", EVENT_TYPE_MLRS),
        ("💣 КАБ у напрямку Харків.", EVENT_TYPE_GUIDED_BOMB),
        ("Київ швидкісна!", EVENT_TYPE_BALLISTIC),
        ("Київ увага КР!!", EVENT_TYPE_CRUISE),
        ("Нивки над вами БПЛА!", EVENT_TYPE_DRONE),
        ("Київ!", EVENT_TYPE_UNKNOWN),
    ],
)
async def test_event_entity_maps_danger_types(
    hass: HomeAssistant,
    message: str,
    event_type: str,
) -> None:
    """Test danger detections publish the expected native event type."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [r"\bнивки\b", r"\bхарків\b"],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    hass.states.async_set("sensor.alerts", message)
    await hass.async_block_till_done()

    state = hass.states.get(_event_entity_id(hass, entry))
    assert state.attributes[ATTR_EVENT_TYPE] == event_type
    assert state.attributes[ATTR_MATCHED_MESSAGE] == message


async def test_safe_detection_resets_attributes(
    hass: HomeAssistant,
) -> None:
    """Test safe messages reset detection attributes to None."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [r"\bнивки\b"],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    hass.states.async_set("sensor.alerts", "Київ швидкісна!")
    await hass.async_block_till_done()
    hass.states.async_set("sensor.alerts", "Все тихо")
    await hass.async_block_till_done()

    state = hass.states.get("binary_sensor.aerial_danger_ballistic_danger")
    assert state.state == STATE_OFF
    assert all(state.attributes[attr] is None for attr in DETECTION_ATTRIBUTE_KEYS)


async def test_match_details_are_logged(
    hass: HomeAssistant,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test a match logs exact values and regex patterns at debug level."""
    area_pattern = r"\bкиїв\b"
    entry = _entry(
        {
            CONF_REGION_PATTERNS: [area_pattern],
            CONF_LOCALITY_PATTERNS: [],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    with caplog.at_level("DEBUG", logger="custom_components.aerial_danger"):
        hass.states.async_set("sensor.alerts", "КИЇВ ШВИДКІСНА!")
        await hass.async_block_till_done()

    record = next(
        record
        for record in caplog.records
        if record.message.startswith("Detected danger for entry")
    )
    assert record.args == (
        entry.entry_id,
        "sensor.alerts",
        "ballistic",
        "КИЇВ ШВИДКІСНА!",
        "КИЇВ",
        "КИЇВ ШВИДКІСНА",
        area_pattern,
        rf"{area_pattern} швидкісна",
    )


async def test_setup_rejects_invalid_stored_pattern(
    hass: HomeAssistant,
) -> None:
    """Test setup fails cleanly for invalid stored regex."""
    entry = _entry(
        {
            CONF_REGION_PATTERNS: ["("],
            CONF_LOCALITY_PATTERNS: [],
            CONF_SOURCES: ["sensor.alerts"],
        }
    )
    entry.add_to_hass(hass)

    assert not await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    config_entry = hass.config_entries.async_get_entry(entry.entry_id)
    assert config_entry is not None
    assert config_entry.state is ConfigEntryState.SETUP_ERROR


@pytest.mark.parametrize(
    "data",
    [
        {
            CONF_REGION_PATTERNS: [],
            CONF_LOCALITY_PATTERNS: [],
            CONF_SOURCES: ["sensor.alerts"],
        },
        {
            CONF_REGION_PATTERNS: [r"\bкиїв\b"],
            CONF_LOCALITY_PATTERNS: [],
            CONF_SOURCES: [],
        },
    ],
)
async def test_setup_rejects_incomplete_stored_config(
    hass: HomeAssistant,
    data: dict[str, object],
) -> None:
    """Test setup rejects entries without patterns or sources."""
    entry = _entry(data)
    entry.add_to_hass(hass)

    assert not await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    config_entry = hass.config_entries.async_get_entry(entry.entry_id)
    assert config_entry is not None
    assert config_entry.state is ConfigEntryState.SETUP_ERROR
