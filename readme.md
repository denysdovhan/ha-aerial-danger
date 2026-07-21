[![SWUbanner](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua/)

<!-- markdownlint-disable-next-line no-inline-html -->
<img alt="HA Aerial Danger Logo" src="./assets/logo.png" width="250px">

# 💥 HA Aerial Danger

[![GitHub Release][gh-release-image]][gh-release-url]
[![GitHub Downloads][gh-downloads-image]][gh-downloads-url]
[![hacs][hacs-image]][hacs-url]
[![GitHub Sponsors][gh-sponsors-image]][gh-sponsors-url]
[![Buy Me A Coffee][buymeacoffee-image]][buymeacoffee-url]
[![Twitter][twitter-image]][twitter-url]

> [!NOTE]
> A [Home Assistant][home-assistant] integration that detects aerial danger alerts for your configured areas from text published by selected entities.

Aerial Danger monitors entities containing Ukrainian alert messages, matches them against your area patterns, and provides binary sensors and events for use in dashboards and automations.

It detects intermediate-range ballistic missiles, ballistic missiles, cruise missiles, drones, and unknown aerial dangers. A separate **Danger** sensor indicates when any supported danger is active.

## Sponsorship

Your generosity will help me maintain and develop more projects like this one.

- 💖 [Sponsor on GitHub][gh-sponsors-url]
- ☕️ [Buy Me A Coffee][buymeacoffee-url]
- Bitcoin: `bc1q7lfx6de8jrqt8mcds974l6nrsguhd6u30c6sg8`
- Ethereum: `0x6aF39C917359897ae6969Ad682C14110afe1a0a1`

## Installation

The quickest way to install this integration is via [HACS][hacs-url] by clicking the button below:

[![Add to HACS via My Home Assistant][hacs-install-image]][hasc-install-url]

If it doesn't work, add this repository to HACS manually by using this URL:

1. Visit **HACS** → **Integrations** → **...** (in the top right) → **Custom repositories**
2. Click **Add**
3. Paste `https://github.com/denysdovhan/ha-aerial-danger` into the **URL** field
4. Choose **Integration** as the **Category**
5. **Aerial Danger** will appear in the list of available integrations. Install it normally.

## Usage

Before setup, create or choose a Home Assistant entity whose state contains incoming alert text, such as an entity populated by a Telegram bot or scraper.

This integration is configurable via UI. On the **Devices and Services** page, click **Add Integration** and search for **Aerial Danger**.

Configure the integration with:

- **Name** — the name of the detection entry and device.
- **Source entities** — entities whose state contains alert messages.
- **Regions** — select built-in region presets, add custom Python regular expressions, or combine both.
- **Neighborhoods** — select presets belonging to the chosen regions, add custom regular expressions, or combine both.

The first built-in region is Kyiv, with Sviatoshyn, Akademmistechko, Antonov, Nyvky, and Vynohradar neighborhoods. At least one effective region or neighborhood pattern and one source entity are required. You can change sources, presets, and custom patterns later from the integration options. Rename the entry through Home Assistant's native entry rename action.

The integration creates a binary sensor for each supported danger type, an aggregate **Danger** binary sensor, and a **Danger detected** event entity. Repeat the setup to monitor different providers, areas, or source groups independently.

## Development

Want to contribute to the project?

First, thanks! Check the [contributing guideline](./contributing.md) for more information.

## License

MIT © [Denys Dovhan][denysdovhan]

<!-- Badges -->

[gh-release-url]: https://github.com/denysdovhan/ha-aerial-danger/releases/latest
[gh-release-image]: https://img.shields.io/github/v/release/denysdovhan/ha-aerial-danger?style=flat-square
[gh-downloads-url]: https://github.com/denysdovhan/ha-aerial-danger/releases
[gh-downloads-image]: https://img.shields.io/github/downloads/denysdovhan/ha-aerial-danger/total?style=flat-square
[hacs-url]: https://github.com/hacs/integration
[hacs-image]: https://img.shields.io/badge/hacs-default-orange.svg?style=flat-square
[gh-sponsors-url]: https://github.com/sponsors/denysdovhan
[gh-sponsors-image]: https://img.shields.io/github/sponsors/denysdovhan?style=flat-square
[buymeacoffee-url]: https://buymeacoffee.com/denysdovhan
[buymeacoffee-image]: https://img.shields.io/badge/support-buymeacoffee-222222.svg?style=flat-square
[twitter-url]: https://x.com/denysdovhan
[twitter-image]: https://img.shields.io/badge/follow-%40denysdovhan-000000.svg?style=flat-square

<!-- References -->

[home-assistant]: https://www.home-assistant.io/
[denysdovhan]: https://github.com/denysdovhan
[hasc-install-url]: https://my.home-assistant.io/redirect/hacs_repository/?owner=denysdovhan&repository=ha-aerial-danger&category=integration
[hacs-install-image]: https://my.home-assistant.io/badges/hacs_repository.svg
