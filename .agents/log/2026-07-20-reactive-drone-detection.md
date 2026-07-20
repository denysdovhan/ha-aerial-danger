---
title: Reactive drone detection
date: 2026-07-20
status: done
related_paths:
  - custom_components/aerial_danger/danger/keywords.py
  - tests/test_danger.py
---

## Background

The [Aerial Danger product direction](2026-07-10-aerial-danger-product-direction.md)
established an area-gated, keyword-driven detector. Monitoring channels now
report jet-powered drones with wording beyond the existing `шахед`, `мопед`,
and `бпла` forms.

## Problem

Immediate reactive-drone alerts use several word orders, inflections, and
shorthand forms. A broad `реактив*` match would also catch attack summaries,
damage reports, and analysis.

## Decision

Keep detection logic and exports unchanged. Extend only `DRONE_DANGER` keyword
templates and detector tests.

- Require `{area}` in every new pattern; Kyiv-only channel context does not
  replace an explicit configured area in the message.
- Cover observed immediate-alert forms: `реактивний` with direction,
  `реактивний дрон`, `реактивний БпЛА`, `реактивний Шахед`, bare `реактив`,
  plural `реактивних`, `реактивна ціль`, and the `реактивних клоунів`
  euphemism.
- Use bounded gaps where the area and danger phrase are separated.
- Group equivalent phrases with `|`; do not collapse all forms into one broad
  expression.
- Store positive test cases as `(area_pattern, danger_pattern, text)` and keep
  aftermath examples as explicit negative cases.

✅ Match location-directed, immediate danger reports.

❌ Do not match area-less posts, aftermath, generic model analysis, or ambiguous
`швидкісна` wording.

## Tradeoffs & Alternatives

Area gating avoids false positives but cannot detect terse Kyiv-only posts that
contain no configured location. Supporting those would require a separate
channel-context decision and matching-logic change.

Grouped alternations reduce duplication while remaining more explicit than a
generic reactive-word stem. The resulting expressions are denser than separate
patterns but preserve the same accepted phrases.

## Verification

- [x] `scripts/lint`
- [x] `scripts/test tests/test_danger.py` — 13 passed
- [x] Positive cases preserve the matched danger-pattern template.
- [x] Aftermath cases remain negative.

## Implementation Notes

2026-07-20: Researched seven monitoring-channel archives and added 23 immediate
alert cases plus two aftermath negatives. Review consolidated 23 initial
templates into 10 grouped patterns.

2026-07-20: Full `scripts/test` reached 44 passed and one unrelated existing
diagnostics-redaction failure in `tests/test_diagnostics.py`.
