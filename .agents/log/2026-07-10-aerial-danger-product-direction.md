---
title: Aerial Danger product direction
date: 2026-07-10
status: done
related_paths:
  - custom_components/aerial_danger/
  - custom_components/aerial_danger/danger/
  - tests/
  - readme.md
---

## Background

Aerial Danger is a Home Assistant custom integration for detecting danger
messages from Telegram-channel data exposed through user-configured Home
Assistant sources. Users provide area patterns for regions and neighborhoods.
External data collection stays outside the integration; users can feed text via
scraping integrations, Telegram bots, templates, text helpers, or similar Home
Assistant entities.

The danger detection library already lives in
`custom_components/aerial_danger/danger/`. It exposes `DangerDetector`,
`Detection`, and `DangerType`, with keyword templates isolated in
`keywords.py`.

## Problem

The product direction and Step 3 integration plan were migrated from the
retired `plan/product.md`, but parts of that plan are already implemented.
Future work needs a concise record of the chosen boundaries and the current
split between implemented behavior and pending product direction.

## Decision

Configure each integration entry with:

- entry name
- region regex patterns
- neighborhood regex patterns
- source Home Assistant entity IDs whose state contains text

Use the existing danger library as the integration detection engine. Build one
`DangerDetector` per config entry from the configured patterns. Composite
detection checks ballistic, cruise missile, drone, then generic danger; first
match wins.

Use local push wiring for the first Home Assistant implementation. Subscribe to
state changes for configured source entities, process only actual text changes,
and avoid polling unless a later source type requires it.

Expose danger state through five safety binary sensors:

- ballistic danger
- cruise missile danger
- drone danger
- unknown/generic danger
- aggregate danger

Fire distinct danger events per detected type with payload fields for type,
area, match, message, source entity ID, and timestamp.

## Current Implementation

- Danger library is implemented in `custom_components/aerial_danger/danger/`
  with compiled regex matching, keyword templates, `DangerDetector`,
  `Detection`, and `DangerType`.
- Config flow is single-instance and captures name, region patterns,
  neighborhood patterns, and source entity IDs.
- Options flow allows editing the same fields and normalizes multiline pattern
  input into lists.
- Invalid regex patterns are rejected in config flow, options flow, and setup.
- Runtime data is stored on `ConfigEntry.runtime_data`.
- Source entity state changes are subscribed via Home Assistant push events; the
  integration ignores unchanged, unavailable, and unknown states.
- Each changed source state is passed to the composite detector in ballistic,
  cruise, drone, then generic order.
- Events are fired for detected danger types:
  `ballistic_danger`, `cruise_danger`, `drone_danger`, and `unknown_danger`.
- Five safety binary sensors are exposed: ballistic, cruise, drone, unknown,
  and aggregate danger.
- Type-specific sensors expose match attributes when active; the aggregate
  sensor exposes active danger-type flags.
- English and Ukrainian translations cover config/options fields and binary
  sensor names.
- README documents configuration, sensors, events, and current project status.
- Tests cover the danger library, config/options flows, setup, sensor updates,
  same-type attribute refresh, clear behavior, and invalid stored regex setup
  failure.

## Future Work

- Update `manifest.json` `iot_class`; it is currently `calculated`, while the
  state-change design points to `local_push`.
- Add richer source subentries for multiple source types and inferred source
  names.
- Support reading source attributes or templates; current implementation reads
  only entity state.
- Filter the source entity selector to text-like entities if Home Assistant API
  support is suitable.
- Add explicit event behavior tests if event contract stability becomes
  important.
- Add event descriptions/translations if Home Assistant supports them for this
  integration surface.
- Manually validate the full workflow in a development Home Assistant server.
- Add Home Assistant brands assets outside this repository.

## Tradeoffs & Alternatives

Direct Telegram integration is intentionally out of scope. Keeping data
collection external lets users choose existing Home Assistant sources and keeps
the first integration implementation smaller.

Polling is deferred. State-change subscriptions better match Home Assistant
local push semantics for configured source entities. Add scan intervals only if
future source types need polling.

Full source modeling is deferred. The first implementation reads only source
entity state text; attributes, templates, and typed source subentries are later
UX/product work.

## Implementation Plan

- Align manifest metadata with local-push behavior.
- Add source subentry model only when the desired source UX is clear.
- Extend sources beyond entity state text when needed: attributes, templates,
  or helper-specific handling.
- Add targeted tests around events and future source types as their contracts
  stabilize.
- Complete manual development-server validation.
- Add Home Assistant brands assets in the brands repository.

## Verification

- [x] Danger library has pytest coverage in `tests/test_danger.py`.
- [x] Config/options flow coverage exists in `tests/test_config_flow.py`.
- [x] Setup and binary sensor behavior coverage exists in `tests/test_init.py`.
- [x] Run `scripts/lint` after Python changes in the current worktree.
- [x] Run `scripts/test` before finalizing this entry.
- [x] Manually validate Home Assistant source state changes, danger events, and
      binary sensors in the dev server.

## Implementation Notes

2026-07-10: Entry seeded from `plan/product.md` while initializing
`.agents/log/`. No code validation run; this change only adds design-log
documentation.

2026-07-10: Reconciled entry against current repository state. Step 3 core
integration wiring is partly implemented and covered by HA-level tests; pending
work is now limited to metadata, richer source UX, event contract hardening,
manual validation, and external brands assets.

2026-07-10: Removed retired `plan/` folder after migrating product direction
into `.agents/log/`.

2026-07-10: Renamed city patterns to region patterns throughout the integration.
Config entry data and options migrate from `city_patterns` to `region_patterns`
at minor version 2; the old key remains a setup fallback for incomplete
migrations.

2026-07-10: `scripts/lint` passed. `scripts/test` could not spawn its `pytest`
entrypoint in the local uv environment; `uv run python -m pytest` passed all 17
tests instead.

2026-07-10: No compatibility migration is needed at this starting stage; removed
the migration, legacy key fallback, and migration test. Configuration now stores
only `region_patterns`.

2026-07-10: Validate configured regexes through the static
`DangerDetector.validate_patterns` helper before construction; config and setup
do not instantiate a detector to validate input.

2026-07-10: Finalized the initial implementation at commit `ca02f97`. Future
functionality will be recorded in separate design-log entries.
