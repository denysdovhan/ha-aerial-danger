[![SWUbanner](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua/)

<p align="center">
    <img src="./logo.png" alt="Logo Image" width="200"/>
</p>

# 🛰️ HA Aerial Danger

> Home Assistant custom integration that matches danger messages from your own HA entities (e.g. Telegram bots, scrapers) using configurable area regexes and built‑in danger keywords.

## What it does

Aerial Danger listens to configured Home Assistant source entities whose state contains alert text. It tracks danger independently per source, matches messages against your region and neighborhood regex patterns plus built-in Ukrainian aerial-danger keywords, then updates safety binary sensors for ballistic, cruise missile, drone, unknown, and aggregate danger.

## Status

- ✅ Danger detection library with keyword sets and pytest coverage
- ✅ Multi-entry config flow with editable area patterns and source entities
- ✅ Binary sensors for ballistic, cruise, drone, unknown, and aggregate danger
- ✅ Native Home Assistant event entity with danger types and match details
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

Repeat these steps to create separate named detection entries for other
providers, areas, or source groups.

## Configuration

- **Name**: detection entry and device name. Rename the entry with Home Assistant's standard integration rename action.
- **Region regex patterns**: one region-level Python regex per line.
- **Neighborhood regex patterns**: one neighborhood-level Python regex per line.
- **Source entities**: entities whose state text contains alert messages. Each source keeps its own active detection; a non-danger message clears only that source.

At least one area pattern and one source entity are required. Invalid regex patterns are rejected in the config and options flows. Unknown and unavailable source states do not clear active detections. The integration uses local push updates from source entity state changes; it does not poll.

## Entities

The integration creates these safety binary sensors:

- Ballistic danger
- Cruise missile danger
- Drone danger
- Unknown danger
- Danger

The aggregate **Danger** sensor is on while any type-specific danger sensor is on. Every binary sensor exposes `matched_message`, `matched_area`, `matched_danger`, and `source_entity_id`. Type-specific sensors use their latest active detection; the aggregate sensor uses the latest active detection across all types. When a sensor has no active detection, these attributes remain present with `null` values.

## Events

Each detection entry creates a **Danger detected** event entity. It reports one of these event types:

- `ballistic`
- `cruise`
- `drone`
- `unknown`

Event attributes include `matched_message`, `matched_area`, `matched_danger`, `source_entity_id`, and `timestamp`. Startup state seeding does not trigger an event.

Debug logging records each match with these values and the area and danger regex patterns that matched. Normal logging remains quiet during high-volume message periods.

## Actions, triggers, and conditions

This integration does not register custom service actions, automation triggers, or automation conditions. Use standard Home Assistant state triggers with the binary sensors or the event entity.

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
