[![SWUbanner](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua/)

# 🛰️ HA Aerial Danger

> Home Assistant custom integration that matches danger messages from your own HA entities (e.g. Telegram bots, scrapers) using configurable area regexes and built‑in danger keywords.

## What it does

Aerial Danger listens to configured Home Assistant source entities whose state contains alert text. It matches that text against your region and neighborhood regex patterns plus built-in Ukrainian aerial-danger keywords, then updates safety binary sensors for ballistic, cruise missile, drone, unknown, and aggregate danger.

## Status

- ✅ Danger detection library with keyword sets and pytest coverage
- ✅ Config/option flows for name, area patterns, and source entities
- ✅ Binary sensors for ballistic, cruise, drone, unknown, and aggregate danger
- ✅ Events per danger type with match details
- ✅ HA-level config flow and setup tests
- ⏳ Brands assets in the Home Assistant brands repository

## Prerequisites

- A Home Assistant entity whose state contains incoming alert text.
- Region and neighborhood patterns written as Python regular expressions.

## Installation

1. Add this repository to HACS as a custom integration, or copy `custom_components/aerial_danger` into your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. Go to **Settings** > **Devices & services**.
4. Select **Add integration**.
5. Search for **Aerial Danger**.
6. Enter a name, area regex patterns, and source entities.
7. Select **Submit**.

## Configuration

- **Name**: device and entity name prefix.
- **Region regex patterns**: one region-level Python regex per line.
- **Neighborhood regex patterns**: one neighborhood-level Python regex per line.
- **Source entities**: entities whose state text contains alert messages.

Invalid regex patterns are rejected in the config and options flows. The integration uses local push updates from source entity state changes; it does not poll.

## Entities

The integration creates these safety binary sensors:

- Ballistic danger
- Cruise missile danger
- Drone danger
- Unknown danger
- Danger

The aggregate **Danger** sensor exposes active danger types as attributes. Type-specific sensors expose match details when available.

## Events

When danger is detected, the integration fires one of these Home Assistant events:

- `ballistic_danger`
- `cruise_danger`
- `drone_danger`
- `unknown_danger`

Event data includes `type`, `area`, `match`, `message`, `entity_id`, and `timestamp`.

## Actions, triggers, and conditions

This integration does not register custom service actions, automation triggers, or automation conditions. Use standard Home Assistant state triggers with the binary sensors, or event triggers with the events listed above.

## Removal

1. Go to **Settings** > **Devices & services**.
2. Open **Aerial Danger**.
3. Select the three-dot menu.
4. Select **Delete**.
5. Remove the copied custom component files or the HACS custom repository if no longer needed.

## Quality scale

Bronze-target code, docs, and tests live in this repository. Full Bronze still requires branding assets in the separate Home Assistant brands repository.

## Contributing

Contributions are welcome once functionality planning is complete. Please check `contributing.md` for general guidance.

## License

MIT © [Denys Dovhan](https://github.com/denysdovhan)
