---
title: MLRS and guided bomb detection
date: 2026-07-31
status: wip
related_paths:
  - custom_components/aerial_danger/__init__.py
  - custom_components/aerial_danger/danger/
  - custom_components/aerial_danger/binary_sensor.py
  - custom_components/aerial_danger/event.py
  - custom_components/aerial_danger/icons.json
  - custom_components/aerial_danger/trigger.py
  - tests/danger/
  - tests/test_init.py
  - mlrs-guided-bomb-area-research.md
---

# MLRS and guided bomb detection

## Background

Builds on [Danger phrase precision](2026-07-28-danger-phrase-precision.md),
[Diagnostic match sensors](2026-07-27-diagnostic-match-sensors.md), and
[Target-based danger triggers](2026-07-23-target-danger-triggers.md).

## Problem

The detector does not classify MLRS attacks or guided bombs as native danger
types. Live Telegram wording also exposes region and locality candidates not
yet represented by built-in presets.

## Decision

- ✅ Add `mlrs` and `guided_bomb` as native binary-sensor and event types.
- ✅ Require a configured locality for both types, matching drone gating;
  configured regions alone do not activate them.
- ✅ Recognize `РСЗВ`, inflected `КАБ` forms, compact guided-air-bomb wording,
  and official `керовані авіаційні бомби` wording.
- ✅ Treat exact `🟡💣` plus a configured locality as a terse guided-bomb alert;
  support observed `повз` and `вектор` locality forms.
- ✅ Check both types before broader ballistic, cruise, drone, and generic
  matchers while preserving first-match-per-source behavior.
- ✅ Keep the four aggregate diagnostic sensors unchanged.
- ✅ Add exact live positive fixtures, non-matching forecast/aftermath fixtures,
  and explicit all-clear negatives from the listed Telegram channels.
- ✅ Use multiple strict positive MLRS and guided-bomb regexes instead of a
  shared negative guard list.
- ✅ Keep non-matching MLRS and guided-bomb posts neutral: no new danger and no
  clearing of the source's active detection.
- ✅ Keep `Detection` limited to match data; runtime queries
  `DangerDetector.is_safe()` before clearing a source.
- ✅ Use `mdi:fire-truck` for MLRS entity and trigger icons.
- ✅ Use IRBM, MLRS, and GAB in short English labels and БРСД, РСЗВ, and КАБ
  in short Ukrainian labels; spell out terms with parenthesized abbreviations
  in descriptions and document README abbreviations with footnotes.
- ❌ Do not add MLRS or guided-bomb forecast, analysis, or aftermath wording to
  `SAFETY`.
- ✅ Keep review fixture expansions focused on distinct live wording, order,
  punctuation, and multiline forms rather than area-only duplicates.
- ✅ Record researched areas as candidates only; do not add presets in this
  change.
- ❌ Do not bypass locality gating from channel context.

## Verification

- [x] New detector-domain tests pass.
- [x] Event, trigger, runtime, translation, and diagnostics tests pass.
- [x] Full `scripts/test` passes: 131 tests.
- [x] `scripts/lint` passes.

## Implementation Notes

2026-07-31 — Browser research covered all seven listed Telegram channels.
Official and monitoring-channel posts showed weapon-first and area-first
phrasing, plus inflected `КАБ` forms and the official `керованих авіаційних
бомб` term. Candidate areas are recorded separately from runtime presets.

Implementation added two area-gated detector domains, binary sensors, native
event types, target triggers, English/Ukrainian translations, icons, and
focused regression fixtures. The aggregate diagnostic sensor set remains
unchanged.

Review follow-up expanded both detector-domain suites with previously captured
live alerts, replaced synthetic Kyiv examples with observed Kharkiv wording,
and added one narrow MLRS pattern for the observed area/newline/weapon form.

A second review follow-up replaced the broad bidirectional MLRS and guided-bomb
patterns with strict live-message forms. Non-matching posts containing those
weapon terms now preserve the active per-source detection, while explicit
clear messages retain the existing source-clear behavior. The generic direct
target matcher is anchored to complete terse alerts so it cannot reclassify a
non-matching weapon post. No negative guard list is used.

A third review follow-up removed the temporary `Detection.clear` field. Safety
classification now stays in `DangerDetector.is_safe()`, and runtime uses that
method when deciding whether to clear a source.

A fourth review follow-up changed both MLRS icons to `mdi:fire-truck`.

A fifth review follow-up restricted MLRS and guided-bomb detection to configured
localities, matching drone detection. Live region-only fixtures now remain
neutral.

A sixth review follow-up added the observed `🟡💣` guided-bomb signature for
terse locality-only alerts, plus `повз` and `вектор` locality wording.

A seventh review follow-up standardized short entity, event-state, and trigger
labels on IRBM/MLRS/GAB and БРСД/РСЗВ/КАБ. Longer trigger descriptions now
introduce each full term with its abbreviation, and the README defines all six
abbreviations through the existing footnote format.
