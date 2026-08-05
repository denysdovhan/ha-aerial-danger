---
title: Source reset on non-danger messages
date: 2026-08-05
status: done
related_paths:
  - custom_components/aerial_danger/__init__.py
  - custom_components/aerial_danger/danger/keywords.py
  - tests/test_init.py
  - tests/danger/test_safety.py
  - agents.md
  - readme.md
  - readme.en.md
---

# Source reset on non-danger messages

## Background

Supersedes the neutral-message retention chosen in
[Multi-entry source aggregation](2026-07-10-multi-entry-source-aggregation.md)
and [MLRS and guided bomb detection](2026-07-31-mlrs-guided-bomb-detection.md).

## Problem

Home Assistant history showed one source detection remaining active through
many later non-danger source states. Aggregate danger stayed on until the
integration reloaded because runtime cleared a source only for explicit
`SAFETY` matches.

## Decision

- ✅ Treat every usable changed source state as its latest authoritative state.
- ✅ Store a danger match; otherwise remove that source's active detection.
- ✅ Keep danger from other sources active independently.
- ✅ Keep `unknown` and `unavailable` from clearing because they are not source
  messages.
- ✅ Expand safety vetoes with observed explicit clear wording, including
  `дорозвідка`, all-clear, clean-area, and ended-target messages.
- ❌ Do not retain danger through neutral or unrelated messages from that source.

## Tradeoffs & Alternatives

This can clear a channel's danger when it posts unrelated content before an
explicit all-clear. That is accepted because each source entity exposes only
its latest message and the requested contract makes that state authoritative.

## Verification

- [x] A non-danger message clears only its source.
- [x] Other active sources keep aggregate danger on.
- [x] `unknown` and `unavailable` preserve active detection.
- [x] Observed safety wording is classified without treating future all-clear
      wording as already safe.
- [x] `scripts/test`
- [x] `scripts/lint`

## Implementation Notes

2026-08-05 — Reproduced the stale source from Home Assistant history, changed
runtime to remove a source on every non-danger message, and added exact safety
fixtures from the export. `scripts/test` passed 120 tests; `scripts/lint` passed.
