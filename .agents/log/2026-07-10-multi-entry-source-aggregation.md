---
title: Multi-entry source aggregation
date: 2026-07-10
status: wip
related_paths:
  - custom_components/aerial_danger/
  - tests/
  - readme.md
  - agents.md
---

## Background

This follows [Aerial Danger product direction](2026-07-10-aerial-danger-product-direction.md).
An entry may monitor multiple Home Assistant entities, including Telegram
channels, and users need separate named entries for different detection setups.

## Problem

The current flow permits one entry only and every source message replaces the
whole entry state. This lets a safe message from one source clear danger from
another. The stored `name` can also diverge from the config entry title.

Entries must also reject empty source and area-pattern configuration. The
integration is unreleased, so its raw danger-event contract can be replaced
without compatibility migration by discoverable Home Assistant event entities.

## Questions & Answers

- Keep a coordinator out of this change; reconsider it later if requirements
  justify one.
- Keep performance in mind without adding benchmarks or concurrency machinery.
- Aggregate danger must remain on while any type danger is on.
- Let users name entries at creation and rename them afterward.
- Require at least one source and at least one region or neighborhood pattern.
- Replace raw events completely; no compatibility migration is required.
- Area presets and branding remain future work.
- Keep native entry rename refreshing device names.

## Decision

- Keep direct, event-driven runtime data in `ConfigEntry.runtime_data`.
- Track active detections per source; a safe message clears only that source.
- Derive type sensors from all active sources and aggregate danger as the OR of
  ballistic, cruise, drone, and unknown states.
- Allow multiple config entries and overlapping source selections.
- Use `ConfigEntry.title` as the authoritative detection name. New entries do
  not duplicate the name in data or options; native Home Assistant rename is
  used after creation.
- Keep manifest `iot_class` as `calculated`.
- Reject config and options forms with no sources or no area patterns, and
  reject equivalent invalid stored entries during setup.
- Expose one event entity per config entry with `ballistic`, `cruise`, `drone`,
  and `unknown` event types plus detection details.
- Share runtime and device setup through a common base entity.
- Keep the config-entry update listener. `OptionsFlowWithReload` rejects entries
  with update listeners, while this listener also reloads native title changes
  so device names stay synchronized.

## Tradeoffs & Alternatives

`DataUpdateCoordinator` is deferred. The current source is Home Assistant state
events rather than a shared API fetch, so direct callbacks remain smaller and
avoid another update layer.

Duplicate-entry prevention is intentionally not applied. Entries are named
detection configurations rather than unique external devices or services, and
overlapping source selections are supported.

Four raw bus events were replaced instead of renamed. A native event entity is
discoverable in Home Assistant and avoids maintaining a second event contract.

`OptionsFlowWithReload` was rejected because it cannot coexist with the update
listener required for native title-rename device refreshes.

## Implementation Plan

- Extend runtime state with per-source detections and startup seeding.
- Update config/options flows and entity naming.
- Add multi-source, multi-entry, rename, lifecycle, and event regression tests.
- Validate required sources and area patterns in config, options, and setup.
- Replace raw events with one native event entity per entry.
- Update user and agent documentation.

## Verification

- [x] `scripts/lint`
- [x] `scripts/test`
- [x] Multiple entries and overlapping sources remain isolated
- [x] Aggregate danger stays on while any type remains active
- [x] Native entry rename updates the integration device name
- [x] Empty sources and area patterns are rejected
- [x] Event entity setup, payload, repeated-event, and unload behavior
- [x] Config-flow coverage is 100%
- [x] Development server registers event entities without integration errors
- [ ] Final developer review and approval

## Implementation Notes

2026-07-10: Implemented direct per-source active detection state, startup
seeding, latest-source attributes, multi-entry configuration, and authoritative
`ConfigEntry.title` naming. Kept `iot_class` as `calculated` and did not add a
coordinator or migration. `scripts/lint` passed and all 24 tests passed.

2026-07-13: Added required source and area-pattern validation to config,
options, and stored-entry setup. Replaced four raw bus events with one native
event entity per entry and four translated event types. Added a shared base
entity for common device/runtime setup.

Kept the update listener because `OptionsFlowWithReload` cannot be combined
with one, and the listener is also required to reload native title changes so
device names stay synchronized. Tests cover options reload behavior.

`scripts/lint` passed, all 36 tests passed, and config-flow coverage is 100%.
The development server registered both existing entries' event entities without
integration errors. Area presets and branding remain deferred.
