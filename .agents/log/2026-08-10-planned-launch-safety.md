---
title: Planned-launch safety wording
date: 2026-08-10
status: wip
related_paths:
  - custom_components/aerial_danger/danger/keywords.py
  - tests/danger/test_safety.py
---

# Planned-launch safety wording

## Background

This overrides the neutral-only treatment from
[Danger phrase precision](2026-07-28-danger-phrase-precision.md) for two
explicit forecast markers.

## Decision

- Treat `підготовка до пусків` and `планується залучення` as `SAFETY` wording.
- Keep the existing OTRK and Iskander ballistic matcher unchanged.
- Verify the supplied forecast messages raise no danger and match `SAFETY`.

## Verification

- [x] Exact forecast messages match `SAFETY` and no danger type.
- [x] `scripts/lint`
- [x] `scripts/test`

## Implementation Notes

2026-08-10: Added the two PR-derived safety patterns and exact message fixtures.
Focused safety and ballistic tests passed 29 tests; the full suite passed 123
tests; `scripts/lint` passed.
