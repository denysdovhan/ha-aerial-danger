---
title: Danger phrase precision
date: 2026-07-28
status: done
related_paths:
  - agents.md
  - custom_components/aerial_danger/danger/danger.py
  - custom_components/aerial_danger/danger/keywords.py
  - tests/danger/
  - tests/test_init.py
---

# Danger phrase precision

## Background

Builds on [Reactive drone detection](2026-07-20-reactive-drone-detection.md)
and [IRBM danger detection](2026-07-21-irbm-danger-detection.md).

## Problem

Real Telegram alerts use terse and reordered area phrases that are not all
covered. Broad weapon and area expressions also match aftermath, summaries,
and edited posts whose original alert text remains quoted. The collected
fixtures also need to stay concise, domain-oriented, and faithful to the
detector's separate region/locality inputs.

## Decision

- ✅ Keep detection area-gated except for explicit active IRBM alerts.
- ✅ Add simple, bounded live-message variants observed in the listed Telegram
  channels; split bidirectional cases when that is clearer.
- ✅ Reject high-confidence resolved, retrospective, and aftermath wording
  through shared `SAFETY` patterns before danger matching.
- ✅ Require active direction, movement, or short alert shapes in broad
  ballistic weapon-and-area patterns.
- ✅ Keep retrospective strike-correction news neutral, not explicit safety.
- ✅ Keep domain negative messages in one list covered by one loop test.
- ✅ Keep fixtures only in ballistic, cruise, drone, generic, IRBM, safety, or
  detector-domain tests; remove research/source-oriented test files and IDs.
- ✅ Keep ordinary positive fixtures as strings and supply their areas through
  shared, separate `REGION_PATTERNS` and `LOCALITY_PATTERNS`.
- ✅ Keep locality/count shorthand in `DRONE_DANGER`; keep type-neutral
  target/vector wording in `GENERIC_DANGER`.
- ✅ Keep bare configured-area alerts and the `🚛` rocket marker as ballistic.
- ✅ Deduplicate fixtures that differ only by area while preserving meaningful
  wording, order, punctuation, and multiline variants.
- ❌ Do not infer a weapon type from an area or target count alone.
- ❌ Do not match possible/future launches or official strike summaries.
- ❌ Do not keep a generic area-pattern bucket, per-case `.*` entries, or
  targeted-case collections.

## Verification

- [x] Researched live alerts and aftermath examples are covered by domain tests.
- [x] Browser-observed aftermath and resolved posts stay inactive.
- [x] Ordinary positive domain fixtures contain strings only.
- [x] No research-only test files, message IDs, `AREA_PATTERNS`, or
      `TARGETED_*` collections remain.
- [x] Reported ballistic news remains neutral and does not match `SAFETY`.
- [x] `scripts/test` passes: 110 tests.
- [x] `scripts/lint` passes.

## Implementation Notes

2026-07-28 — Browser research covered all seven listed Telegram channels and
neighboring alert sequences. Added bounded danger patterns and shared safety
vetoes, then distributed collected and researched messages across domain tests.

Review refinements simplified regexes, removed area-only duplicate fixtures,
restored drone locality shorthand, split region/locality test inputs, converted
ordinary cases to strings, classified `🔴🚛Ракета Київ!` as ballistic, and
placed Kherson, Bila Tserkva, Bryansk, and Chornomorsk in shared region
patterns.

2026-08-05 — Tightened broad ballistic patterns around active direction,
movement, and short alert shapes. Added the exported `коригував удари` news
message to one ballistic negative-case list and loop test. `scripts/test`
passed 121 tests; `scripts/lint` passed.
