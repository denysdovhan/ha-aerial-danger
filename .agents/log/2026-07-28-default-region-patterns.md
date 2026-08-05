---
title: Default region patterns
date: 2026-07-28
status: done
related_paths:
  - custom_components/aerial_danger/config_flow.py
  - custom_components/aerial_danger/const.py
  - custom_components/aerial_danger/translations/
  - tests/test_config_flow.py
---

# Default region patterns

## Background

This follows [Kyiv area presets](2026-07-21-area-presets.md). The region form
shows two Kyiv regex examples, but new entries need useful contextual defaults
that also work outside Kyiv.

## Decision

- Prefill new entries with `(до|на) нас` and
  `наш(у|ої) област(ь|і)?`.
- Keep the Kyiv regexes as translated documentation examples only.
- Keep the values editable and removable.
- Do not apply these defaults to existing entries or the options flow.

## Verification

- [x] New config flows show both default patterns
- [x] Options flows preserve stored patterns
- [x] `scripts/lint`
- [x] `scripts/test`

## Implementation Notes

2026-07-28: Added the two contextual region phrases as new-entry schema
defaults while retaining the Kyiv regexes as examples. Existing options and
stored values remain unchanged. `scripts/lint` passed and all 110 tests passed.

2026-07-28: Removed the single-quote requirement from custom regex guidance;
YAML examples remain quoted.
