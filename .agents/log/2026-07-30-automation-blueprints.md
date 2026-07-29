---
title: Automation blueprints
date: 2026-07-30
status: wip
related_paths:
  - .pre-commit-config.yaml
  - blueprints/aerial_danger_critical_notification.yaml
  - blueprints/telegram_scrape_refresh.yaml
  - readme.md
---

# Automation blueprints

## Background

The [Aerial Danger product direction](2026-07-10-aerial-danger-product-direction.md)
keeps Telegram collection outside the integration. Reusable blueprints cover
external source refreshing and critical danger notifications.

## Problem

Users need reusable automations for frequent Telegram source refreshing and
critical danger notifications without excessive repeat alerts.

## Decision

- Send iOS/Android-compatible critical notifications and hold a configurable
  cooldown after each notification. Use `single` mode to ignore triggers during
  that delay.
- Require one or more `sensor` entities provided by the Scrape integration.
- Offer native 5- or 10-second time-pattern intervals, defaulting to 5 seconds.
  Do not trigger every second to emulate arbitrary intervals.
- Accept an optional list of Ukraine Alarm safety binary sensors and refresh
  while any selected sensor is `on`.
- Use `homeassistant.update_entity` with `restart` mode.
- Place My Home Assistant import buttons beside the corresponding Scrape
  refresh and critical-notification instructions in `readme.md`.
- Disable YAML Language Server schema validation because Home Assistant has no
  official public blueprint JSON schema and SchemaStore selects Torque.

Ukraine Alarm devices expose separate safety binary sensors rather than one
device-level danger state. Users should select each region's Air sensor.

## Verification

- [x] Both blueprints load through Home Assistant's blueprint schema
- [x] Default and configured inputs produce valid automation structures
- [x] `scripts/lint`
- [x] `scripts/test`

## Implementation Notes

2026-07-30: Added the Telegram Scrape refresh blueprint and clarified schema
suppression in both blueprint files.

2026-07-30: Validated with Home Assistant 2026.7.2. Both default and configured
inputs passed automation schema validation. The optional gate rendered true
with no sensors, false with all sensors off, and true with any sensor on. Lint
passed; 111 tests passed.

2026-07-30: Broadened this entry to all new blueprints. Added a configurable
critical-notification cooldown, user-entered 5–10 second Scrape intervals, and
`restart` mode for Scrape refreshes. Home Assistant 2026.7.2 accepted default
and configured inputs, including a 30-second cooldown and 7-second refresh
interval. Lint passed; 111 tests passed.

2026-07-30: Review rolled the Scrape interval back to native `/5` and `/10`
choices so the automation does not trigger every second. Excluded `blueprints/`
from generic `check-yaml`; Home Assistant's loader validates its custom `!input`
tags instead. Home Assistant 2026.7.2 accepted default and configured inputs;
lint passed; 111 tests passed.

2026-07-30: Published the blueprints and added their My Home Assistant import
buttons to the matching README sections.
