---
title: Regional area presets
date: 2026-08-03
status: done
related_paths:
  - contributing.md
  - custom_components/aerial_danger/config_flow.py
  - custom_components/aerial_danger/danger/presets.py
  - custom_components/aerial_danger/translations/
  - tests/danger/test_presets.py
  - tests/test_config_flow.py
  - mlrs-guided-bomb-area-research.md
---

# Regional area presets

## Background

This extends [Kyiv area presets](2026-07-21-area-presets.md) using the candidate
areas captured during
[MLRS and guided bomb detection](2026-07-31-mlrs-guided-bomb-detection.md).

## Problem

Built-in presets do not cover every Ukrainian oblast. Users in uncovered
oblasts must maintain custom regexes for region names already observed in live
alert wording.

## Decision

- Cover all 24 Ukrainian oblasts under stable, alphabetized IDs; keep Kyiv city
  as a separate region preset.
- Nest cities and other localities under their owning oblast; include
  Zaporizhzhia city with the other requested oblast centers.
- Use official Ukrainian oblast names and Ukrainian canonical locality names.
- Match researched grammatical forms conservatively; include explicitly
  requested Kharkiv and Odesa city landmarks and districts as localities.
- For the 19 additional oblasts, match official oblast-name inflections plus
  live-alert regional aliases confirmed in Telegram. Include researched
  `Буковина` and `Франківщина`; include `Чернівеччина` by explicit request
  despite aftermath-only evidence. Exclude unobserved `Закарпаття`,
  `Прикарпаття`, and `Кропивниччина`.
- Add the administrative center as a locality for every oblast except Kyiv
  Oblast, whose center is already the separate Kyiv region. Use conservative
  canonical forms for Donetsk and Luhansk because research found no city-target
  alert wording, and avoid city forms that overlap their oblast names.
- Accept bare `Пʼятихатки` and `Салтівка`; constrain the port preset to
  `Одеський порт` / `Одеса Порт`. Keep forecasts, analysis, and aftermath out.
- Match the researched Zaporizhzhia alias as `зп` so lowercased source text works.
- Keep preset and English/Ukrainian selector order aligned.
- Define regions as administrative oblasts and localities as named places such
  as settlements, landmarks, and neighborhoods. Link custom-pattern fields to
  the contribution guide in the repository.

## Verification

- [x] Region and locality variants compile and match focused fixtures
- [x] Ownership, stable order, and selector translations remain aligned
- [x] `scripts/lint`
- [x] `scripts/test`

## Implementation Notes

2026-08-03: Added Dnipropetrovsk, Kharkiv, Odesa, and Zaporizhzhia oblasts
with 19 nested localities. Follow-up Telegram research confirmed active alert
wording and added Balakliia, Kamianske, Chornomorsk, Komyshuvakha, Orikhiv, and
Vilniansk beyond the root candidates. Ambiguous names, districts, landmarks,
Huliaipole, and the city/oblast-overlapping Zaporizhzhia shorthand were excluded.
Focused preset tests passed 65 tests; the full suite passed 164 tests;
`scripts/lint` and `git diff --check` passed.

2026-08-03: Review follow-up added five Kharkiv city localities (Derzhprom,
KhTZ, Kulynychi, Pivdenni Piatykhatky, and Saltivka) and four Odesa city
localities (Arcadia, Khadzhybeiskyi District, Odesa Port, and Peresyp), bringing
the regional addition to 28 localities. Telegram research kept bare
`Пʼятихатки` and `Порт` out and confirmed uppercase `ЗП` for Zaporizhzhia city.
Focused preset tests passed 77 tests; the full suite passed 176 tests;
`scripts/lint` and `git diff --check` passed.

2026-08-03: Review correction replaced the case-sensitive `ЗП` regex with `зп`
for lowercased source states and broadened the Kharkiv locality from Pivdenni
Piatykhatky to bare Piatykhatky. Detector-level regression coverage now verifies
`каб на зп!` instead of testing the regex in isolation. Focused preset tests
passed 78 tests; the full suite passed 177 tests; `scripts/lint` and
`git diff --check` passed.

2026-08-03: Review simplification removed the `Стара Салтівка` negative
lookbehinds. The plain inflected `Салтівка` pattern intentionally accepts that
overlap.

2026-08-03: Review follow-up consolidated all special preset spellings into one
`PRESET_EXAMPLES` mapping and one uniform test. Values contain only aliases,
inflections, or alternate punctuation, with tuples supporting multiple forms;
special Saltivka, port, and Zaporizhzhia detector tests were removed. Focused
preset tests passed 8 tests; the full suite passed 107 tests; `scripts/lint` and
`git diff --check` passed.

2026-08-03: Added contributor guidance defining regions as administrative
oblasts and localities as settlements, landmarks, neighborhoods, and similar
named places. Custom region/locality pattern fields now link to the anchored
guide in setup and options flows. Config-flow tests passed 15 tests;
the full suite passed 107 tests; `scripts/lint` passed.

2026-08-03: Added the remaining 19 Ukrainian oblasts, bringing the registry to
all 24 oblasts plus Kyiv city. Parallel research across `operinform`,
`war_monitor`, `AerisRimor`, and `kpszsu` confirmed live-alert regional aliases
for 17 oblasts; Chernivtsi and Zakarpattia initially used official oblast forms
only. Focused preset tests passed 8 tests; the full suite passed 107 tests;
`scripts/lint` and `git diff --check` passed.

2026-08-03: Follow-up research added the 19 missing oblast centers as
localities, plus active-alert `Буковина` and `Франківщина` region aliases.
`Прикарпаття` had no active-alert evidence and was excluded. `Чернівеччина` was
added by explicit request despite only aftermath evidence. Donetsk and Luhansk
use conservative canonical city patterns because no city-targeted alerts were
found; their genitive forms are excluded to avoid matching full oblast names.
Every region now owns at least one locality, with Kyiv kept as a separate region
instead of being duplicated under Kyiv Oblast. Focused preset tests passed 8
tests; the full suite passed 107 tests; `scripts/lint` and `git diff --check`
passed.
