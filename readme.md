[![SWUbanner](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua/)

# 🛰️ HA Aerial Danger

> Home Assistant custom integration that matches danger messages from your own HA entities (e.g. Telegram bots, scrapers) using configurable area regexes and built‑in danger keywords.

## Status

- ✅ Danger detection library with keyword sets and pytest coverage
- ✅ Config/option flows for name, area patterns, and source entities
- ✅ Binary sensors for ballistic, cruise, drone, unknown, and aggregate danger
- ✅ Events per danger type with match details
- ⏳ Polishing, UX, and HA-level tests

## Installation (development)

Add this repository to HACS as a custom integration or copy `custom_components/aerial_danger` into your Home Assistant `custom_components` directory. Configure via UI: provide area regexes (one per line) and select source entities whose state text contains incoming alerts. The integration listens to state changes (local_push) and updates safety binary_sensors plus emits events per danger type.

## Contributing

Contributions are welcome once functionality planning is complete. Please check `contributing.md` for general guidance.

## License

MIT © [Denys Dovhan](https://github.com/denysdovhan)
