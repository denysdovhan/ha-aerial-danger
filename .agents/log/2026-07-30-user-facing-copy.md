---
title: User-facing copy
date: 2026-07-30
status: wip
related_paths:
  - readme.md
  - custom_components/aerial_danger/translations/
---

# User-facing copy

## Background

The canonical README is Ukrainian-first, while the integration UI supports
English and Ukrainian. Existing behavior and safety contracts are recorded in
[Aerial Danger product direction](2026-07-10-aerial-danger-product-direction.md),
[Kyiv area presets](2026-07-21-area-presets.md), and
[Target-based danger triggers](2026-07-23-target-danger-triggers.md).

## Problem

Users need a clearer path from installation to message sources, area selection,
entities, and automations. Some interface strings are repetitive, inconsistent,
or do not explain how to fix invalid input.

## Decision

- Keep the English masthead and Ukrainian practical guide.
- Preserve safety guidance, external source boundaries, detection behavior,
  blueprint instructions, entity contracts, and notification settings.
- Use direct, consistent terminology across the README and both translations.
- Keep Home Assistant trigger descriptions phrased as "Triggers when..."
- Keep English detection labels aligned with the `matched_*` attribute contract.
- Use «Джерело повідомлень» consistently in Ukrainian source labels.
- Make errors explain the corrective action.
- Keep translation keys and preset names unchanged.
- Keep external links in translated flow copy via description placeholders.

## Verification

- [x] English and Ukrainian translation structures match
- [x] JSON, Markdown, links, and YAML examples validate
- [x] `scripts/lint`
- [x] `scripts/test`
- [ ] Hassfest accepts translated external-link placeholders

## Implementation Notes

2026-07-30: Reworked the setup path, entity explanations, automations,
troubleshooting, and removal guidance without changing behavior. Aligned
English and Ukrainian flow descriptions, recovery-focused errors, trigger
descriptions, and entity labels. Lint passed, all 111 tests passed, and focused
pre-commit checks validated JSON and formatted the changed files.

2026-07-30: Applied review feedback: restored "Triggers when..." descriptions
and all English "Matched" labels, restored the original Ukrainian entry/device
name description, standardized Ukrainian source labels on «Джерело
повідомлень», and removed diagnostic sensors from the English introduction.
Lint passed and all 111 tests passed after the revisions.

2026-07-30: Hassfest rejected literal URLs in five English flow strings.
Replaced them with config and options flow description placeholders while
keeping the links in both supported locales. Added flow-result regression
coverage; lint passed and all 112 tests passed. Exact Hassfest recheck remains
pending because the local Docker daemon is unavailable.
