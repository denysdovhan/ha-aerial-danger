---
title: Diagnostic match sensors
date: 2026-07-27
status: done
related_paths:
  - custom_components/aerial_danger/binary_sensor.py
  - custom_components/aerial_danger/const.py
  - custom_components/aerial_danger/sensor.py
  - custom_components/aerial_danger/translations/
  - custom_components/aerial_danger/icons.json
  - tests/test_diagnostics.py
  - tests/test_init.py
  - readme.md
  - agents.md
---

## Background

This follows the stable aggregate attribute contract from
[Cleanup attributes](2026-07-13-cleanup-attributes.md). The aggregate danger
binary sensor exposes the latest active detection's matched message, area,
danger, and source entity ID.

## Problem

Matched values are currently attributes, which makes them less convenient to
display and track as individual Home Assistant entities. Add diagnostic sensors
for these values without creating a second detection model.

## Questions & Answers

- Add sensors for matched message, area, and danger.
- Add a matched-source sensor only if the source entity ID can be resolved to
  its Home Assistant friendly name. `State.name` provides that resolution.
- Mirror the aggregate attributes rather than retaining the last detection.
- When no danger is active, use the translated custom state `clear` rather than
  Home Assistant's `unknown` or `unavailable` states.
- IRBM detections have no area match; expose translated `nationwide` instead.

## Decision

- Create one diagnostic sensor per matched value for each config entry.
- Use translated entity names, stable unique IDs, push updates, and the existing
  integration device.
- Read values from `RuntimeData.latest_detection`; do not duplicate detection
  state.
- Store `clear` and `nationwide` state constants in `const.py`.
- Resolve the source sensor value from its entity ID through Home Assistant's
  current state and expose `State.name`.

## Tradeoffs & Alternatives

Per-danger-type diagnostic sensor sets would duplicate the same four values for
every danger type and add unnecessary entity/history noise. The aggregate
latest detection is the intended source.

Retaining matches was rejected because "last matched" state would need restart
persistence to be trustworthy. Mirroring current aggregate attributes keeps the
new sensors stateless and makes `clear` explicitly mean no active detection.

## Implementation Plan

- Add the sensor platform and four diagnostic sensor descriptions.
- Add English and Ukrainian entity translations and translated icons.
- Cover setup, match updates, source friendly-name resolution, `clear`, and
  nationwide IRBM behavior.
- Run `scripts/lint` and `scripts/test`.

## Verification

- [x] Four diagnostic sensors register per config entry
- [x] Values follow the aggregate latest detection
- [x] Source entity ID resolves to its Home Assistant friendly name
- [x] Inactive sensors expose translated `clear` state
- [x] IRBM area exposes translated `nationwide` state
- [x] `scripts/lint`
- [x] `scripts/test`

## Implementation Notes

2026-07-27: Added four push-based diagnostic sensors using the aggregate latest
active detection. Added English and Ukrainian entity/state translations,
translated icons, friendly source-name resolution, `clear` inactive state, and
`nationwide` IRBM area state. Updated integration documentation and diagnostics
entity-count coverage. `scripts/lint` passed and all 102 tests passed.

2026-07-27: Applied review feedback: shortened Ukrainian inactive states to
`Немає`, changed nationwide to `Вся країна`, and changed the source icon to
`mdi:shape`.

2026-07-27: Centralized diagnostic entity keys in `const.py` without the
`ATTR_` prefix and restored binary-sensor description keys to existing
`STATE_*` constants. `scripts/lint` and all 102 tests passed after review
changes.

2026-07-27: Kept named sensor value helpers with the `state_` prefix.
