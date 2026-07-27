---
title: Target-based danger triggers
date: 2026-07-23
status: done
related_paths:
  - custom_components/aerial_danger/trigger.py
  - custom_components/aerial_danger/triggers.yaml
  - custom_components/aerial_danger/translations/
  - tests/test_trigger.py
  - readme.md
---

## Background

Browser and runtime inspection showed that the new automation editor discovers
triggers through Home Assistant's target-trigger API. The legacy
`device_trigger.py` implementation is only returned by the older device
automation endpoint, so its five danger triggers do not appear in the current
picker.

## Decision

- Replace the legacy device trigger platform with target-based triggers.
- Register aggregate danger, IRBM, ballistic, cruise, drone, and unknown triggers
  in `trigger.py`.
- Limit each trigger to Aerial Danger event entities via `triggers.yaml`.
- Match every native event type for aggregate danger; otherwise filter the
  existing event entity's event-type attribute.
- Keep detector, runtime, binary-sensor, and event contracts unchanged.

## Verification

- [x] Device target discovery returns all six Aerial Danger triggers
- [x] Aggregate danger trigger invokes for every native danger type
- [x] Matching and repeated detections invoke the selected trigger
- [x] Non-matching danger types and detached triggers do not invoke it
- [x] `scripts/lint`
- [x] `scripts/test`

## Implementation Notes

2026-07-23: Added five target-based triggers backed by the existing event
entity and removed the unshipped legacy device-trigger implementation.
Target discovery now returns `aerial_danger.irbm`, `ballistic`, `cruise`,
`drone`, and `unknown` for the integration device. Event updates are accepted
even when two event timestamps fall within the same millisecond, then filtered
by event type. Browser verification confirmed the restarted development UI
loads the automation editor. `scripts/lint` and all 93 tests passed.

2026-07-25: Added `aerial_danger.danger` as the aggregate target trigger. It
matches every native danger event type and uses the aggregate danger sensor's
`mdi:alert-decagram` icon. Target discovery returns all six triggers.
`scripts/lint` and all 98 tests passed.
