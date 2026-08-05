---
title: Generic danger precision
date: 2026-08-03
status: done
related_paths:
  - custom_components/aerial_danger/danger/keywords.py
  - tests/danger/
  - agents.md
---

# Generic danger precision

## Background

Builds on [Danger phrase precision](2026-07-28-danger-phrase-precision.md).

## Problem

Generic target and area-tail patterns match inside weapon-specific messages.
Locality-gated drone, MLRS, and guided-bomb alerts can therefore fall through
as unknown danger when they mention only a configured region.

## Decision

- ✅ Keep detector logic and danger types unchanged.
- ✅ Make bare area, direct target, and course/vector generic patterns match
  complete terse messages instead of substrings.
- ✅ Preserve observed type-neutral route and timing alerts with narrow
  positive patterns.
- ✅ Keep explicit ballistic and cruise wording in their specific domains,
  including messages prefixed by alert and rocket emojis.
- ✅ Reserve `☄`/`☄️` for ballistic detection and `🛵` for locality-gated
  drone detection; neither marker may fall through a generic area match.
- ❌ Do not use new safety gates, negative weapon lists, or matcher variables.

## Verification

- [x] Reported drone messages stay neutral with region-only configuration.
- [x] Bare `КИЇВ!`, `НИВКИ!`, direct target, and route alerts still match.
- [x] Emoji-prefixed ballistic and cruise messages keep their specific types.
- [x] `☄`/`☄️` messages are ballistic and explicitly do not match generic.
- [x] `🛵` messages match configured localities, not region-only configuration.
- [x] MLRS/GAB region-only regression cases cover the open PR's future rebase.
- [x] `scripts/test` — 118 passed.
- [x] `scripts/lint`

## Implementation Notes

2026-08-03 — Replaced generic area substrings and suffixes with complete-message
patterns. Kept existing type-neutral route/timing alerts through narrow positive
forms, and moved overlapping fixtures to drone, ballistic, and cruise tests.
No detector logic, danger types, or safety gates changed.

2026-08-03 — Reserved comet markers for a bounded ballistic-to-area pattern and
removed them from generic prefixes. Moved the reported scooter examples into
drone tests: configured localities match as drone; a region alone stays neutral.
