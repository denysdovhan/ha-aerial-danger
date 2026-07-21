---
title: Kyiv area presets
date: 2026-07-21
status: done
related_paths:
  - custom_components/aerial_danger/config_flow.py
  - custom_components/aerial_danger/danger/pattern_utils.py
  - custom_components/aerial_danger/danger/presets.py
  - custom_components/aerial_danger/diagnostics.py
  - custom_components/aerial_danger/translations/
  - readme.md
  - tests/
---

## Background

This follows [Aerial Danger product direction](2026-07-10-aerial-danger-product-direction.md) while preserving its event-driven runtime and existing detector contract.

## Problem

Users must currently author every area regex. Kyiv users need stable region and neighborhood choices without losing custom-pattern support.

## Questions & Answers

- **Initial region scope?** Kyiv city only; exclude Kyiv Oblast.
- **Initial neighborhood scope?** Sviatoshyn, Akademmistechko, Antonov, Nyvky, and Vynohradar only.
- **Flow layout?** Name and sources, then region presets plus custom YAML regex patterns, then neighborhood presets plus custom YAML regex patterns.
- **Selection behavior?** Presets are optional searchable multi-select dropdowns; custom patterns remain optional YAML object fields.
- **Diagnostics privacy?** Show code-defined preset IDs; redact custom patterns and source entities.
- **Safety warning placement?** Initial setup and README only; keep options concise.

## Decision

- Store optional stable preset IDs separately from custom regex lists.
- Nest every neighborhood under its owning region; first iteration contains Kyiv only.
- Keep canonical preset names with patterns and ownership metadata.
- Keep preset data in `presets.py` and pattern lookup/resolution helpers in `pattern_utils.py`, with custom patterns first and ordered deduplication before detector construction.
- Configure name/sources, regions, then neighborhoods; options mirror the same dependency order without editing the native entry name.
- Present preset choices as searchable multiple-selection dropdowns.
- Explain source setup, preset multiplicity and optionality, and custom regex formatting in both supported languages.
- Warn during initial setup and in the README that detection is fallible and unofficial; direct users to official alerts and shelters, with no accuracy or safety guarantee from the author or maintainer. Keep routine options free of the disclaimer.
- Expose code-defined preset IDs in diagnostics while redacting custom patterns and sources.
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

2026-07-21: Preserved YAML-list custom-regex fields and normalized stored lists. Added nested Kyiv definitions, dependent selectors, old-entry fallback, pruning, diagnostics redaction, and runtime resolution. `scripts/lint` passed, all 67 tests passed, and `config_flow.py` coverage is 100%.

2026-07-21: Review refinement added canonical preset names, renamed the registry to `PRESETS`, and split region and neighborhood resolution by domain.

2026-07-21: Review refinement made preset selectors searchable dropdowns, exposed non-sensitive preset IDs in diagnostics, and clarified schema-builder names.

2026-07-21: Review refinement moved preset lookup and pattern resolution into `pattern_utils.py`, made the preset selector builder public-style, and simplified inline-linked regex guidance.

2026-07-22: Synced English and Ukrainian flow guidance, added Scrape and Telegram source examples, documented optional multiple presets, and added a prominent safety and no-warranty disclaimer to the flows and README.

2026-07-22: Follow-up synced English to the user-edited Ukrainian copy and removed the disclaimer from both options flows.

2026-07-22: Follow-up mirrored the shortened Ukrainian options intro in English; source setup examples remain on initial setup only.

2026-07-22: Clarified in both languages that region matching covers fast approaching threats, while neighborhood matching covers drones and every threat type.

2026-07-22: Finalized after review. `scripts/lint` passed, all 67 tests passed, and config-flow coverage remained 100%.
