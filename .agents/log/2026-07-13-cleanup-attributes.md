---
title: Cleanup attributes
date: 2026-07-13
status: done
related_paths:
  - custom_components/aerial_danger/binary_sensor.py
  - custom_components/aerial_danger/event.py
  - custom_components/aerial_danger/const.py
  - custom_components/aerial_danger/danger/
  - custom_components/aerial_danger/runtime.py
  - custom_components/aerial_danger/translations/
  - tests/
  - readme.md
  - agents.md
---

## Background

This follows
[Multi-entry source aggregation](2026-07-10-multi-entry-source-aggregation.md).
Binary sensors and the native event entity now expose detection and aggregate
attributes used by dashboards and automations.

## Problem

The attribute contract needs a focused review. Remove redundant or unclear
attributes, use Home Assistant exports and integration constants where
appropriate, and preserve useful direct-push state without stale data.

## Questions & Answers

- All binary sensors should expose the same stable detection attribute keys:
  matched message, matched area, matched danger, and triggering entity ID.
- When a sensor has no current detection, keep every detection attribute key
  present and use `None` rather than the literal Home Assistant state string
  `"unknown"`.
- Matched area and danger contain the exact text matched by their regular
  expressions, preserving source-message casing.
- The aggregate sensor uses the latest active detection across all types.
- Remove aggregate per-type boolean attributes; separate type sensors already
  expose those states.
- The event entity uses the same detection attribute names and retains its
  timestamp.
- Log matched values plus their area and danger regex patterns in the Home
  Assistant integration layer. Keep the future standalone `danger/` library
  logger-free. Use debug level so normal logging remains quiet during intensive
  message flow.

## Decision

- Every binary sensor always exposes `matched_message`, `matched_area`,
  `matched_danger`, and `source_entity_id`.
- Inactive binary-sensor detection attributes are `None`.
- Type sensors select their latest active detection. Aggregate danger selects
  the latest active detection across every type and source.
- Event data uses the same four detection attributes plus `timestamp`.
- Detections retain exact matched area and danger text together with the regex
  patterns used. Regex patterns are debug-log data, not entity attributes.
- Regex helpers return `PatternMatch(text, pattern)` objects rather than
  positional tuples; the `Detection` model keeps its flat attribute contract.
- Cache aggregate latest detection during runtime state derivation; entity
  properties remain constant-time and I/O-free.

## Tradeoffs & Alternatives

Literal `"unknown"` attribute values were rejected because they would conflate
missing data with Home Assistant entity state semantics. `None` keeps a stable
attribute schema without inventing a value.

Info-level match logging was rejected because expected critical-message bursts
could flood normal logs. Debug logging keeps the requested diagnostics opt-in.

## Implementation Plan

- Inventory current binary-sensor and event attributes.
- Compare them with Home Assistant entity and event conventions.
- Use the integration-specific `source_entity_id` key because Home Assistant's
  reserved `entity_id` key is not rendered as an ordinary custom attribute.
- Preserve exact matched text and regex patterns in detection models.
- Cache the latest aggregate detection in runtime state.
- Update constants, entities, tests, and documentation together.

## Verification

- [x] Attribute contract documented
- [x] Attribute behavior covered by tests
- [x] `scripts/lint`
- [x] `scripts/test`
- [x] Manual Home Assistant verification

## Implementation Notes

2026-07-13: Implemented the stable four-attribute binary-sensor contract,
latest-active aggregate selection, aligned event data, exact case-preserving
regex matches, and debug match logging in the Home Assistant layer. The danger
library remains logger-free. `scripts/lint` passed and all 39 tests passed.

2026-07-13: Replaced the reserved `entity_id` attribute with visible
`source_entity_id` after runtime UI verification showed the former was omitted.
Added English and Ukrainian labels for all four detection attributes on
binary-sensor and event entities. Labels are duplicated per entity translation
key because runtime custom-integration translation files do not resolve shared
string references.

2026-07-13: Restarted Home Assistant and verified the active ballistic sensor
in Browser: all four translated labels and values render, including
`input_text.alternative_message` as Source entity. Verified an inactive cruise
sensor renders the same four labels with Unknown values.

2026-07-14: Replaced internal regex-match tuples with the named `PatternMatch`
dataclass while preserving the existing `Detection` and entity attributes.
`scripts/lint` passed and all 40 tests passed.

2026-07-15: Developer approved the final attribute contract and completed the
feature review.
