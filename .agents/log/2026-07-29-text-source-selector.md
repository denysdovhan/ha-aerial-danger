---
title: Text source selector
date: 2026-07-29
status: wip
related_paths:
  - custom_components/aerial_danger/config_flow.py
  - tests/test_config_flow.py
  - agents.md
---

# Text source selector

## Background

This resolves the text-like source filtering deferred by
[Aerial Danger product direction](2026-07-10-aerial-danger-product-direction.md).
The integration reads only the selected entity's state as a danger message.

## Problem

The source selector currently shows every Home Assistant entity, including
domains whose state is numeric, binary, a timestamp, or an operational mode.

## Decision

- Filter config and options selectors to `sensor`, `text`, and `input_text`.
- Use the current `EntitySelectorConfig.filter` API.
- Keep all sensors because Home Assistant cannot filter sensor entities by the
  runtime type of `native_value`.
- Exclude fixed-choice `select` and `input_select` entities because they model
  control options rather than free-form message sources.
- Keep runtime and stored configuration unchanged.

## Tradeoffs & Alternatives

Filtering `sensor` by device class or unit would hide valid Scrape, template,
MQTT, and other text sensors without reliably removing numeric sensors.
Runtime state inspection cannot drive the standard entity selector filter.

## Verification

- [x] Config and options selectors expose the same domain filter.
- [x] Existing config and options flow tests pass.
- [x] `scripts/lint`
- [x] `scripts/test`

## Implementation Notes

2026-07-29: Added the shared `sensor`, `text`, and `input_text` domain filter
to setup and options selectors. `scripts/lint` and all 111 tests pass.
