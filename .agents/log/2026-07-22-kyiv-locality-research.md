---
title: Kyiv locality research
date: 2026-07-22
status: wip
related_paths:
  - custom_components/aerial_danger/danger/presets.py
  - custom_components/aerial_danger/translations/
  - tests/danger/test_presets.py
  - kyiv-neighborhood-implement.md
---

## Background

This extends [Kyiv area presets](2026-07-21-area-presets.md). The first iteration
contained five Kyiv localities; monitoring channels use many more formal,
informal, administrative, and landmark names when describing target routes.

Research covered 12,906 posts dated 2026-06-24 through 2026-07-21: Kyivskyi
Kupol, Kyiv AirDefense, Monitoring Kyiv, Operatyvnyi Inform, War Monitor, Aeris
Rimor, and the Air Force of Ukraine. Nationwide posts counted only when they
described a live Kyiv target route or warning. Aftermath, forecasts, and
same-name places outside Kyiv were excluded. Names were cross-checked against
[Kyiv localities alphabetically](https://uk.wikipedia.org/wiki/Категорія:Місцевості_Києва_за_алфавітом),
but monitoring-channel wording is the authority for matching.

## Problem

Kyiv alerts frequently name smaller localities and informal zones instead of
the city. Missing those names delays neighborhood-level detection; accepting
ambiguous shorthand can instead create false alerts from unrelated places or
ordinary words.

## Questions & Answers

- **Which findings ship now?** All reviewed safe localities.
- **How are spelling variants represented?** One regex for grammatical or close
  spelling variants; separate regexes for genuinely different aliases.
- **How are `масив` names handled?** The suffix is optional, so both the full
  locality and observed shorthand match.
- **What remains open?** Informal, broad-zone, administrative, and overlapping
  candidates stay in `kyiv-neighborhood-implement.md` for manual review.

## Decision

- Add 62 Kyiv city locality presets, nested under the Kyiv region and ordered
  by stable preset key.
- Add Kyiv Oblast as a separate region preset without localities for now.
- Add the reviewed Kyiv Oblast localities only under that region, preserving the
  Kyiv city catalog.
- Use Ukrainian canonical names. Translations provide localized dropdown labels.
- Accept grammatical forms, observed spelling errors, and established alert
  shorthand where the reviewed evidence is sufficiently specific.
- Keep ambiguous candidates out until separately approved.
- Keep nearby settlements outside the Kyiv city preset.

### Accepted localities from Kyiv-focused channels

| Locality             | Matching explanation                                                                                                                                                                         | Evidence                                                                                                                                                                                           |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Академмістечко       | Full inflections and the established `Академ` shorthand.                                                                                                                                     | [target route](https://t.me/nebo_raketa/37056)                                                                                                                                                     |
| Антонов              | `Антонов` and the observed genitive; may refer to the airport/company, but Kyiv channels use it as an alert zone.                                                                            | [locality list](https://t.me/kyiv_airdef/40137), [ballistic warning](https://t.me/kyiv_airdef/42528)                                                                                               |
| Берковець            | Grammatical forms of the locality name.                                                                                                                                                      | [drone alert](https://t.me/kyiv_airdef/40985)                                                                                                                                                      |
| Борщагівка / Борщага | City locality forms and the observed `Борщага` / `Борщаги` shorthand. This deliberately also matches Petropavlivska and Sofiivska Borshchahivka references.                                  | [locality](https://t.me/kyiv_airdef/41898), [slang](https://t.me/kyiv_airdef/40131), [national shorthand](https://t.me/AerisRimor/75985)                                                           |
| Бортничі             | Plural grammatical forms.                                                                                                                                                                    | [direct warning](https://t.me/kyiv_monit0ring/26742), [target route](https://t.me/nebo_raketa/36496)                                                                                               |
| Центр                | Central Kyiv alert zone with observed grammatical forms. `Центр` also matches shopping centers and the center of any city or region, so it is an explicit recall-over-precision tradeoff.    | [ballistic alert](https://t.me/nebo_raketa/36223), [drone alert](https://t.me/nebo_raketa/35936), [Kyiv ballistic context](https://t.me/s/deraketaua?before=57948)                                 |
| Виноградар           | Common grammatical forms.                                                                                                                                                                    | [area warning](https://t.me/kyiv_airdef/41075)                                                                                                                                                     |
| Видубичі             | Plural grammatical forms.                                                                                                                                                                    | [missile alert](https://t.me/nebo_raketa/36255)                                                                                                                                                    |
| Воскресенка          | Accept the observed `Восресенка` misspelling.                                                                                                                                                | [warning](https://t.me/kyiv_airdef/41806), [route](https://t.me/kyiv_airdef/41736)                                                                                                                 |
| Голосіїв             | Locality, same-root district adjective, and the observed `Голос` shorthand. The shorthand is an ordinary word and organization name, so it is accepted only as a deliberate recall tradeoff. | [missile alert](https://t.me/nebo_raketa/36258), [district warning](https://t.me/nebo_raketa/36672), [drone route](https://t.me/AerisRimor/73886)                                                  |
| Дарниця              | Locality, district adjective, and optional `масив` suffix.                                                                                                                                   | [direct warning](https://t.me/kyiv_monit0ring/26742), [district alert](https://t.me/kyiv_monit0ring/26629), [Дарницький масив](https://t.me/war_monitor/41307)                                     |
| Деміївка             | Common grammatical forms.                                                                                                                                                                    | [area warning](https://t.me/kyiv_airdef/41075)                                                                                                                                                     |
| Дорогожичі           | User-directed addition with standard Ukrainian plural case forms. No exact live-alert mention appeared in the all-channel search.                                                            | User request                                                                                                                                                                                       |
| ДВРЗ                 | Case-insensitive abbreviation.                                                                                                                                                               | [drone alert](https://t.me/nebo_raketa/36310), [route](https://t.me/kyiv_airdef/41623)                                                                                                             |
| Галагани             | Plural locality case forms plus the observed bare `Галаган` shorthand.                                                                                                                       | [area warning](https://t.me/kyiv_airdef/20143), [route](https://t.me/kyiv_airdef/30466), [shorthand](https://t.me/kyiv_airdef/36875)                                                               |
| Жуляни               | Observed plural and stem forms.                                                                                                                                                              | [locality list](https://t.me/kyiv_airdef/40137), [area warning](https://t.me/kyiv_airdef/41075)                                                                                                    |
| Клов                 | Common grammatical forms.                                                                                                                                                                    | [area warning](https://t.me/kyiv_airdef/41075)                                                                                                                                                     |
| Конча-Заспа          | Hyphen or space plus grammatical forms and the observed `Заспа` shorthand. The shorthand omits `Конча`, so it is an explicit recall-over-precision tradeoff.                                 | [drone route](https://t.me/nebo_raketa/36022), [course update](https://t.me/kyiv_airdef/40104), [Kyiv drone route](https://t.me/AerisRimor/74325), [direct warning](https://t.me/AerisRimor/73879) |
| КПІ                  | Observed abbreviation, including `район КПІ`; nationwide monitoring also uses it for live Kyiv routes. No additional Ukrainian alias was found in the channel search.                        | [alert](https://t.me/kyiv_airdef/27642), [район КПІ](https://t.me/kyiv_airdef/29635), [nationwide route](https://t.me/AerisRimor/32162)                                                            |
| Липки                | Plural grammatical forms.                                                                                                                                                                    | [area warning](https://t.me/kyiv_airdef/41075)                                                                                                                                                     |
| Лісовий масив        | Full name and observed `Лісовий` shorthand via optional `масив`.                                                                                                                             | [full name](https://t.me/nebo_raketa/35960), [shorthand](https://t.me/kyiv_airdef/41857)                                                                                                           |
| Лівобережний масив   | Full name and short adjective via optional `масив`.                                                                                                                                          | [route](https://t.me/kyiv_airdef/41736), [ballistic warning](https://t.me/kyiv_airdef/42528)                                                                                                       |
| Лукʼянівка           | Straight, curly, modifier-letter, or omitted apostrophe plus inflections.                                                                                                                    | [alert](https://t.me/nebo_raketa/36972), [area warning](https://t.me/kyiv_airdef/41898)                                                                                                            |
| Мишоловка            | Common grammatical forms.                                                                                                                                                                    | [drone alert](https://t.me/nebo_raketa/36051), [paired route](https://t.me/nebo_raketa/36275)                                                                                                      |
| Мінський масив       | Full name and observed `Мінський` shorthand via optional `масив`; shorthand can also refer to Minsk.                                                                                         | [full name](https://t.me/nebo_raketa/36100), [shorthand](https://t.me/kyiv_airdef/40903)                                                                                                           |
| Нивки                | Observed plural grammatical forms.                                                                                                                                                           | [ballistic warning](https://t.me/kyiv_airdef/42528)                                                                                                                                                |
| Оболонь              | Locality and same-root district adjective.                                                                                                                                                   | [drone route](https://t.me/kyiv_monit0ring/26928), [district warning](https://t.me/nebo_raketa/36672)                                                                                              |
| Осокорки             | Plural grammatical forms.                                                                                                                                                                    | [drone route](https://t.me/nebo_raketa/36301), [paired warning](https://t.me/nebo_raketa/36275)                                                                                                    |
| Печерськ             | Locality and same-root district adjective.                                                                                                                                                   | [missile alert](https://t.me/nebo_raketa/36062), [area warning](https://t.me/kyiv_airdef/41075)                                                                                                    |
| Поділ                | Locality and same-root district adjective.                                                                                                                                                   | [direct warning](https://t.me/kyiv_monit0ring/26742), [district warning](https://t.me/nebo_raketa/36672)                                                                                           |
| Позняки              | Plural grammatical forms.                                                                                                                                                                    | [route](https://t.me/nebo_raketa/36287), [area warning](https://t.me/kyiv_airdef/41075)                                                                                                            |
| Пуща-Водиця          | Hyphen or space plus grammatical forms; bare `Пуща` remains under review.                                                                                                                    | [drone alert](https://t.me/nebo_raketa/36239), [route](https://t.me/kyiv_airdef/40191)                                                                                                             |
| Рембаза              | Common grammatical forms.                                                                                                                                                                    | [direct warning](https://t.me/kyiv_monit0ring/26550), [area warning](https://t.me/kyiv_airdef/41075)                                                                                               |
| Русанівка            | Locality inflections; bare `Русанів` is excluded because it is a separate Kyiv Oblast settlement.                                                                                            | [missile alert](https://t.me/nebo_raketa/35862), [multi-area alert](https://t.me/nebo_raketa/36236)                                                                                                |
| Солом'янка / Солома  | Accepted `Солома` slang plus locality and district forms with apostrophe variants. Bare `солома` is an ordinary word, so this is a deliberate recall-over-precision tradeoff.                | [slang alert](https://t.me/kyiv_airdef/40793), [district warning](https://t.me/nebo_raketa/36672)                                                                                                  |
| Святошин             | `Святошин`, `Святошино`, and same-root district adjective.                                                                                                                                   | [district form](https://t.me/nebo_raketa/36103), [locality form](https://t.me/kyiv_airdef/41898)                                                                                                   |
| Шулявка              | Common grammatical forms.                                                                                                                                                                    | [missile alert](https://t.me/nebo_raketa/36262), [area warning](https://t.me/kyiv_airdef/41075)                                                                                                    |
| Теличка              | Common grammatical forms.                                                                                                                                                                    | [drone route](https://t.me/nebo_raketa/36022), [locality list](https://t.me/kyiv_airdef/40137)                                                                                                     |
| Троєщина             | Full name plus established `Троя`, `Трої`, and `Трою` slang.                                                                                                                                 | [full name](https://t.me/nebo_raketa/36543), [slang](https://t.me/nebo_raketa/36953), [cross-channel use](https://t.me/kyiv_monit0ring/26860)                                                      |

### Accepted localities validated by nationwide channels

| Locality          | Matching explanation                                                                                                                                                                                                    | Evidence                                                                                                                                                                                |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Березняки         | Plural grammatical forms.                                                                                                                                                                                               | [paired route](https://t.me/operinform/54745), [missile alert](https://t.me/war_monitor/41110)                                                                                          |
| Біличі            | Plural grammatical forms.                                                                                                                                                                                               | [paired route](https://t.me/operinform/54724), [missile route](https://t.me/war_monitor/41115)                                                                                          |
| Биківня           | Common grammatical forms.                                                                                                                                                                                               | [paired route](https://t.me/operinform/54223), [missile route](https://t.me/war_monitor/41307)                                                                                          |
| Відрадний         | Accept the observed `Відрандний` misspelling.                                                                                                                                                                           | [paired route](https://t.me/operinform/54723), [reactive-drone alert](https://t.me/war_monitor/41367)                                                                                   |
| Віта-Литовська    | Require the full two-word name with a hyphen or space; bare `Віта` is ambiguous.                                                                                                                                        | [drone route](https://t.me/war_monitor/41081)                                                                                                                                           |
| Гідропарк         | Common grammatical forms.                                                                                                                                                                                               | [drone route](https://t.me/operinform/54208)                                                                                                                                            |
| Іподром           | Landmark used as a Kyiv alert zone; accept its grammatical forms because multiple Kyiv alerts group it with Теремки and Жуляни. The same label can occur in Odesa, so it remains scoped under the selected Kyiv region. | [original route](https://t.me/AerisRimor/73795), [Kyiv grouping](https://t.me/s/kievreal1?before=83349), [Holosiiv/Teremky route](https://t.me/s/darnicalive?after=79274)               |
| Караваєві Дачі    | Canonical locality name with standard phrase case forms and the `Кардачі` alias. No exact full-name alert mention appeared in the all-channel search; the alias appears in a live drone route.                          | [Кардачами](https://t.me/AerisRimor/60953)                                                                                                                                              |
| Лівий берег       | Broad Kyiv alert zone matching `лівий берег` and `лівобережжя`, including `лівобережжя столиці`. It is not a neighborhood and can occur outside Kyiv, so it is an explicit recall-over-precision tradeoff.              | [missile warning](https://t.me/nebo_raketa/36054), [drone warning](https://t.me/kyiv_monit0ring/27057), [national shorthand](https://t.me/AerisRimor/76069)                             |
| Харківський масив | Full locality name and observed shorthand through optional `масив`. The shorthand also describes Kharkiv city, district, or oblast, so it is an explicit recall-over-precision tradeoff.                                | [full name](https://t.me/kyiv_airdef/40137), [shorthand alert](https://t.me/kyiv_airdef/41374), [Kyiv drone route](https://t.me/s/kievreal1?before=94917)                               |
| Червоний Хутір    | Full-name grammatical forms plus the observed bare `Хутір` alias. Bare `Хутір` may refer to any settlement or locality, so it is an explicit recall-over-precision tradeoff.                                            | [nominative route](https://t.me/kyiv_monit0ring/14241), [genitive wording](https://t.me/kyiv_monit0ring/21634), [Kyiv route with Рембаза](https://t.me/s/kiev_levyy_bereg?before=54300) |
| Правий берег      | Broad Kyiv alert zone matching `правий берег` and `правобережжя`. It is not a neighborhood and can occur outside Kyiv, so it is an explicit recall-over-precision tradeoff.                                             | [missile warning](https://t.me/nebo_raketa/36260), [drone warning](https://t.me/kyiv_monit0ring/26750), [national shorthand](https://t.me/AerisRimor/73884)                             |
| Звіринець         | Common grammatical forms.                                                                                                                                                                                               | [drone alert](https://t.me/war_monitor/41316), [paired route](https://t.me/war_monitor/41087)                                                                                           |
| Куренівка         | Common grammatical forms.                                                                                                                                                                                               | [missile alert](https://t.me/operinform/55021), [drone route](https://t.me/war_monitor/41155)                                                                                           |
| Нижні Сади        | Both words inflect as a phrase.                                                                                                                                                                                         | [paired route](https://t.me/operinform/54718), [direct warning](https://t.me/operinform/54568)                                                                                          |
| Нова Забудова     | Generic phrase, accepted after repeated use as a named Kyiv route zone alongside Деміївка and Жуляни.                                                                                                                   | [cruise route](https://t.me/s/war_monitor?before=41329), [drone route](https://t.me/s/war_monitor?before=33470), [repeated Kyiv route](https://t.me/s/war_monitor?before=30768)         |
| Острів Муромець   | `Острів` is optional; useful alert zone although it is an island, not a neighborhood.                                                                                                                                   | [direct warning](https://t.me/operinform/54249), [route](https://t.me/war_monitor/41289)                                                                                                |
| Почайна           | Observed grammatical forms.                                                                                                                                                                                             | [Obolon route](https://t.me/operinform/54382), [reactive-drone alert](https://t.me/war_monitor/41075), [paired route](https://t.me/AerisRimor/75931)                                    |
| Пріорка           | Common grammatical forms.                                                                                                                                                                                               | [drone route](https://t.me/operinform/54298)                                                                                                                                            |
| Русанівські Сади  | Both words inflect as a phrase.                                                                                                                                                                                         | [drone warning](https://t.me/operinform/54741), [missile alert](https://t.me/operinform/54330)                                                                                          |
| Сирець            | Common grammatical forms.                                                                                                                                                                                               | [paired route](https://t.me/operinform/54722), [route correction](https://t.me/AerisRimor/76007)                                                                                        |
| Теремки           | Plural grammatical forms.                                                                                                                                                                                               | [reactive-drone route](https://t.me/war_monitor/41136), [paired route](https://t.me/AerisRimor/74334)                                                                                   |
| Чоколівка         | Common grammatical forms.                                                                                                                                                                                               | [Kyiv alert](https://t.me/war_monitor/41142)                                                                                                                                            |

### Kyiv Oblast region

| Region           | Matching explanation                                                                           | Evidence                                                                                                                                          |
| ---------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Київська область | Kyivshchyna case forms and full inflected Kyiv Oblast phrases. It has no locality presets yet. | [Київщини](https://t.me/war_monitor/12271), [Київська область](https://t.me/operinform/13633), [Київській області](https://t.me/operinform/14852) |

### Kyiv Oblast localities

| Locality                                                                           | Matching explanation                                                            |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Бориспіль                                                                          | Standard singular case forms and the observed `Борік` shorthand.                |
| Бровари                                                                            | Standard plural case forms.                                                     |
| Буча, Вишгород, Вишневе, Ірпінь, Гостомель, Ворзель                                | Standard singular locality case forms.                                          |
| Петропавлівська Борщагівка, Софіївська Борщагівка                                  | Both words match standard phrase case forms.                                    |
| ЖК Софія                                                                           | Requires the `ЖК` prefix to avoid matching a person name or unrelated locality. |
| Чайки, Проліски, Погреби, Петрівці                                                 | Standard plural locality case forms.                                            |
| Коцюбинське, Гнідин, Козин, Обухів, Васильків, Українка, Димер, Зазим'я, Хотянівка | Standard Ukrainian locality case forms.                                         |

Live monitoring-channel searches confirmed [Бровари](https://t.me/operinform/54348),
[Борік](https://t.me/AerisRimor/45536),
[Петропавлівська Борщагівка](https://t.me/kyiv_airdef/14855),
[Софіївська Борщагівка](https://t.me/war_monitor/28401),
[ЖК Софія](https://t.me/operinform/39385), and
[Зазим'я](https://t.me/kyiv_monit0ring/9630).
All remain nested under Kyiv Oblast.

### Deferred findings

| Candidate             | Why deferred                                                                      | Evidence                                                                                          |
| --------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Озерна                | Adjective/place name occurs elsewhere and may mean the metro station.             | [grouped warning](https://t.me/operinform/54499), [route](https://t.me/operinform/54377)          |
| Вокзал                | Broad landmark used in every city.                                                | [direct route](https://t.me/AerisRimor/75884), [paired route](https://t.me/AerisRimor/75909)      |
| Микільська Борщагівка | Overlaps a possible generic Borshchahivka preset.                                 | [direct route](https://t.me/kyiv_airdef/40131), [grouped warning](https://t.me/kyiv_airdef/41075) |
| Південна Борщагівка   | Only bare `Південна` was observed, while the safe full phrase would not match it. | [grouped warning](https://t.me/kyiv_airdef/41075)                                                 |
| Поштова площа         | Specific phrase, but landmark status and sparse evidence need review.             | [direct warning](https://t.me/kyiv_airdef/40235)                                                  |
| Урядовий квартал      | Specific phrase, but it is an alert zone rather than a neighborhood.              | [area warning](https://t.me/kyiv_airdef/41075)                                                    |
| Шевченківський район  | Administrative adjective is unsafe without Kyiv context.                          | [district warning](https://t.me/nebo_raketa/36672)                                                |
| Деснянський район     | Bare `Десна` must remain excluded because it names a settlement north of Kyiv.    | [district warning](https://t.me/nebo_raketa/36672)                                                |
| Дніпровський район    | Same adjective is widely used for other places and organizations.                 | [district report](https://t.me/nebo_raketa/36991)                                                 |

Nearby settlements such as Brovary, Boryspil, Vyshhorod, Vyshneve, Irpin,
Bucha, Hostomel, Vorzel, Chaiky, Kotsiubynske, Hnidyn, Kozyn, Obukhiv, and
Vasylkiv remain excluded from the Kyiv city preset. `Русанів` is also excluded:
it is a separate settlement, not an inflection of `Русанівка`.

## Tradeoffs & Alternatives

Adding every observed token would maximize recall but would conflate ordinary
words, landmarks, administrative areas, nearby settlements, and same-name
places across Ukraine. The selected set favors locality-specific live-alert
language. Some reviewed shorthand (`Мінський`, `Лісовий`, `Лівобережний`) is
still intentionally accepted to match how Kyiv channels report approaching
targets.

## Verification

- [x] Every accepted preset compiles.
- [x] Preset keys and selector translations stay in registry order.
- [x] Focused spelling, shorthand, and boundary tests pass.
- [x] `scripts/lint`
- [x] `scripts/test` — 90 tests passed.

## Implementation Notes

2026-07-22: Added all reviewed safe localities with Ukrainian canonical names,
alphabetically ordered stable keys, translation coverage, and focused regex
tests. Deferred ambiguous findings remain in `kyiv-neighborhood-implement.md`.

2026-07-22: Accepted Іподром after validating repeated Kyiv alert use alongside
Теремки, Жуляни, and Голосіїв. Kept the preset nested under Kyiv because the same
landmark name is also used in Odesa.

2026-07-22: Accepted Нова Забудова after repeated live Kyiv cruise and drone
routes paired it with Деміївка and Жуляни. Its generic wording remains a
false-positive risk outside Kyiv-focused source messages.

2026-07-22: Added `Голос` as a Голосіїв alias after a route paired it with
Теличка and Деміївка. It remains an explicit recall-over-precision tradeoff.

2026-07-22: Added `Заспа` as a Конча-Заспа alias from Kyiv drone-route evidence.
The shorthand omits `Конча` and remains an explicit recall-over-precision tradeoff.

2026-07-22: Added generic Борщагівка / Борщага with the initially reviewed
variants only. It deliberately matches nearby Kyiv Oblast Borshchahivka names;
additional variants remain deferred for separate review.

2026-07-22: Added Солом'янка / Солома with slang and district apostrophe
variants. Bare `солома` is an ordinary word and remains an explicit
recall-over-precision tradeoff.

2026-07-22: Added Харківський масив with its observed shorthand through an
optional `масив` suffix. The shorthand can describe Kharkiv outside Kyiv and
remains an explicit recall-over-precision tradeoff.

2026-07-22: Added Центр with observed inflections. It can match shopping centers
and any city or region center, so it remains an explicit recall-over-precision
tradeoff.

2026-07-22: Added Червоний Хутір using the bare `Хутір` alias. The alias can
refer to any settlement or locality and remains an explicit recall-over-precision
tradeoff. Expanded the full name for observed nominative and genitive wording,
plus standard singular case forms.

2026-07-22: Added Лівий берег and Правий берег as broad Kyiv alert zones, with
the `лівобережжя` and `правобережжя` forms. Neither represents a neighborhood;
both remain explicit recall-over-precision tradeoffs.

2026-07-22: Added Галагани with Ukrainian plural case forms and the observed
bare `Галаган` shorthand from Kyiv AirDefense alerts.

2026-07-22: Added КПІ for the observed abbreviation only. A subsequent pass
across all configured monitoring channels confirmed active Kyiv-route use in
Aeris Rimor; no additional Ukrainian matching form was found.

2026-07-22: Added Дорогожичі at the user's direction with standard Ukrainian
plural case forms. The all-channel search returned no exact live-alert mention.

2026-07-22: Merged Караваєві Дачі and Кардачі into one locality preset. The
canonical name is Караваєві Дачі; `Кардачі` remains its live-route alias.

2026-07-22: Added Kyiv Oblast as an independent region, with no locality
presets. It matches Kyivshchyna forms and inflected full region phrases.

2026-07-22: Added 24 user-directed Kyiv Oblast localities, including `Борік`
for Бориспіль and a `ЖК`-scoped Софія pattern. They are available only after
selecting Kyiv Oblast.

2026-07-22: Review correction moved `Борік` from Бровари to a dedicated
Бориспіль preset and removed Десна because it is outside Kyiv Oblast.
`scripts/lint` passed; all 90 tests passed.
