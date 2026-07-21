---
title: IRBM danger detection
date: 2026-07-21
status: done
related_paths:
  - custom_components/aerial_danger/danger/
  - custom_components/aerial_danger/binary_sensor.py
  - custom_components/aerial_danger/event.py
  - custom_components/aerial_danger/runtime.py
  - custom_components/aerial_danger/translations/
  - tests/
  - readme.md
---

## Background

The [Aerial Danger product direction](2026-07-10-aerial-danger-product-direction.md)
established area-gated danger types. Monitoring channels also publish
nationwide alerts for intermediate-range ballistic missiles, primarily
`БРСД`, `Орєшнік`, `Кедр`, `РС-26`, and `Рубіж`.

## Problem

Treating these alerts as ordinary ballistic danger hides the weapon type and
requires an area that nationwide posts often omit. Broad name matching would
also flag advance warnings, launch preparations, aftermath, and all-clear
posts.

## Questions & Answers

- Add a dedicated danger sensor instead of extending ballistic detection.
- Treat IRBM alerts as nationwide; no configured area is required in a post.
- Match explicit current danger and launch reports.
- Do not match preventive forecasts, readiness or preparation reports, future
  warning windows, aftermath, or all-clear posts.
- Use `IRBM` and `irbm` consistently; do not retain the earlier `MRBM` name.

## Decision

- Add `DangerType.IRBM`, `IRBM_DANGER`, and `DangerDetector.irbm_danger()`.
- Reuse the shared detector with `match_areas=False`; keep matching logic
  otherwise unchanged.
- Check IRBM before ordinary ballistic danger so specific alerts retain their
  type.
- Expose a dedicated safety binary sensor and native event type using the
  stable key `irbm`.
- Keep regexes explicit and nationwide. Similar spellings may share a small
  alternation; unrelated phrases remain separate patterns.
- Test production patterns through `IRBM_DANGER[index]`, ordered by index, with
  explicit potential-danger and aftermath negatives.

✅ Match explicit active danger, active-alert escalation, and confirmed launch
reports.

❌ Do not match preparation, readiness, possible future launches, attack
summaries, or cancellations.

This adds a sixth safety binary sensor and supersedes the five-sensor list in
the earlier product-direction entry.

## Tradeoffs & Alternatives

Area-independent matching intentionally activates IRBM danger for every entry
monitoring the same source. Reusing ballistic danger was rejected because it
loses the dedicated type and sensor state.

No `MRBM` compatibility alias or entity migration is kept because the name was
corrected to IRBM before this feature was committed.

## Verification

- [x] Immediate IRBM danger and launch samples match nationwide.
- [x] Preventive, preparation, aftermath, and all-clear samples remain negative.
- [x] Binary-sensor state and native event type use `irbm`.
- [x] Focused detector and integration tests — 37 passed.
- [x] `scripts/lint`.

## Implementation Notes

2026-07-21: Added the nationwide detector, sensor, event type, translations,
icons, documentation, and positive/negative regression coverage. Renamed the
feature from MRBM to IRBM before commit.

2026-07-21: Full `scripts/test` reached 48 passed and one unrelated existing
diagnostics-redaction failure in
`tests/test_diagnostics.py::test_config_entry_diagnostics_redacts_user_data`.
