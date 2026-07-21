---
title: Kyiv area presets
date: 2026-07-21
status: wip
related_paths:
  - custom_components/aerial_danger/config_flow.py
  - custom_components/aerial_danger/danger/presets.py
  - custom_components/aerial_danger/translations/
  - tests/
---

## Background

This follows [Aerial Danger product direction](2026-07-10-aerial-danger-product-direction.md) while preserving its event-driven runtime and existing detector contract.

## Problem

Users must currently author every area regex. Kyiv users need stable region and neighborhood choices without losing custom-pattern support.

## Decision

- Store optional stable preset IDs separately from custom regex lists.
- Nest every neighborhood under its owning region; first iteration contains Kyiv only.
- Keep canonical preset names with patterns and ownership metadata.
- Resolve region and neighborhood patterns through separate domain functions, with custom patterns first and ordered deduplication before detector construction.
- Configure name/sources, regions, then neighborhoods; options mirror the same dependency order without editing the native entry name.
- Keep drone matching neighborhood-only and IRBM matching nationwide.

## Tradeoffs & Alternatives

A global neighborhood catalog and Kyiv Oblast are deferred. Stored IDs keep definitions correctable without config-entry migration, while custom regex lists retain advanced control.

## Verification

- [x] Preset registry, variants, and boundary tests
- [x] Config/options flow coverage
- [x] Diagnostics redaction and runtime resolution tests
- [x] `scripts/lint`
- [x] `scripts/test`

## Implementation Notes

2026-07-21: Created narrow WIP entry for the approved Kyiv preset implementation.

2026-07-21: Preserved multiline custom-regex fields and normalized stored lists. Added nested Kyiv definitions, dependent selectors, old-entry fallback, pruning, diagnostics redaction, and runtime resolution. `scripts/lint` passed, all 67 tests passed, and `config_flow.py` coverage is 100%.

2026-07-21: Review refinement added canonical preset names, renamed the registry to `PRESETS`, and split region and neighborhood resolution by domain.
