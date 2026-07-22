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

- Add 49 Kyiv locality presets, nested under the Kyiv region and ordered by
  stable preset key.
- Use Ukrainian canonical names. Translations provide localized dropdown labels.
- Accept grammatical forms, observed spelling errors, and established alert
  shorthand where the reviewed evidence is sufficiently specific.
- Keep ambiguous candidates out until separately approved.
- Keep nearby settlements outside the Kyiv city preset.

### Accepted localities from Kyiv-focused channels

| Locality | Matching explanation | Evidence |
|---|---|---|
| Академмістечко | Full inflections and the established `Академ` shorthand. | [target route](https://t.me/nebo_raketa/37056) |
| Антонов | `Антонов` and the observed genitive; may refer to the airport/company, but Kyiv channels use it as an alert zone. | [locality list](https://t.me/kyiv_airdef/40137), [ballistic warning](https://t.me/kyiv_airdef/42528) |
| Берковець | Grammatical forms of the locality name. | [drone alert](https://t.me/kyiv_airdef/40985) |
| Бортничі | Plural grammatical forms. | [direct warning](https://t.me/kyiv_monit0ring/26742), [target route](https://t.me/nebo_raketa/36496) |
| Виноградар | Common grammatical forms. | [area warning](https://t.me/kyiv_airdef/41075) |
| Видубичі | Plural grammatical forms. | [missile alert](https://t.me/nebo_raketa/36255) |
| Воскресенка | Accept the observed `Восресенка` misspelling. | [warning](https://t.me/kyiv_airdef/41806), [route](https://t.me/kyiv_airdef/41736) |
| Голосіїв | Locality and same-root district adjective; bare `Голос` remains excluded. | [missile alert](https://t.me/nebo_raketa/36258), [district warning](https://t.me/nebo_raketa/36672) |
| Дарниця | Locality, district adjective, and optional `масив` suffix. | [direct warning](https://t.me/kyiv_monit0ring/26742), [district alert](https://t.me/kyiv_monit0ring/26629), [Дарницький масив](https://t.me/war_monitor/41307) |
| Деміївка | Common grammatical forms. | [area warning](https://t.me/kyiv_airdef/41075) |
| ДВРЗ | Case-insensitive abbreviation. | [drone alert](https://t.me/nebo_raketa/36310), [route](https://t.me/kyiv_airdef/41623) |
| Жуляни | Observed plural and stem forms. | [locality list](https://t.me/kyiv_airdef/40137), [area warning](https://t.me/kyiv_airdef/41075) |
| Клов | Common grammatical forms. | [area warning](https://t.me/kyiv_airdef/41075) |
| Конча-Заспа | Hyphen or space plus grammatical forms; bare `Заспа` remains excluded. | [drone route](https://t.me/nebo_raketa/36022), [course update](https://t.me/kyiv_airdef/40104) |
| Липки | Plural grammatical forms. | [area warning](https://t.me/kyiv_airdef/41075) |
| Лісовий масив | Full name and observed `Лісовий` shorthand via optional `масив`. | [full name](https://t.me/nebo_raketa/35960), [shorthand](https://t.me/kyiv_airdef/41857) |
| Лівобережний масив | Full name and short adjective via optional `масив`. | [route](https://t.me/kyiv_airdef/41736), [ballistic warning](https://t.me/kyiv_airdef/42528) |
| Лукʼянівка | Straight, curly, modifier-letter, or omitted apostrophe plus inflections. | [alert](https://t.me/nebo_raketa/36972), [area warning](https://t.me/kyiv_airdef/41898) |
| Мишоловка | Common grammatical forms. | [drone alert](https://t.me/nebo_raketa/36051), [paired route](https://t.me/nebo_raketa/36275) |
| Мінський масив | Full name and observed `Мінський` shorthand via optional `масив`; shorthand can also refer to Minsk. | [full name](https://t.me/nebo_raketa/36100), [shorthand](https://t.me/kyiv_airdef/40903) |
| Нивки | Observed plural grammatical forms. | [ballistic warning](https://t.me/kyiv_airdef/42528) |
| Оболонь | Locality and same-root district adjective. | [drone route](https://t.me/kyiv_monit0ring/26928), [district warning](https://t.me/nebo_raketa/36672) |
| Осокорки | Plural grammatical forms. | [drone route](https://t.me/nebo_raketa/36301), [paired warning](https://t.me/nebo_raketa/36275) |
| Печерськ | Locality and same-root district adjective. | [missile alert](https://t.me/nebo_raketa/36062), [area warning](https://t.me/kyiv_airdef/41075) |
| Поділ | Locality and same-root district adjective. | [direct warning](https://t.me/kyiv_monit0ring/26742), [district warning](https://t.me/nebo_raketa/36672) |
| Позняки | Plural grammatical forms. | [route](https://t.me/nebo_raketa/36287), [area warning](https://t.me/kyiv_airdef/41075) |
| Пуща-Водиця | Hyphen or space plus grammatical forms; bare `Пуща` remains under review. | [drone alert](https://t.me/nebo_raketa/36239), [route](https://t.me/kyiv_airdef/40191) |
| Рембаза | Common grammatical forms. | [direct warning](https://t.me/kyiv_monit0ring/26550), [area warning](https://t.me/kyiv_airdef/41075) |
| Русанівка | Locality inflections; bare `Русанів` is excluded because it is a separate Kyiv Oblast settlement. | [missile alert](https://t.me/nebo_raketa/35862), [multi-area alert](https://t.me/nebo_raketa/36236) |
| Святошин | `Святошин`, `Святошино`, and same-root district adjective. | [district form](https://t.me/nebo_raketa/36103), [locality form](https://t.me/kyiv_airdef/41898) |
| Шулявка | Common grammatical forms. | [missile alert](https://t.me/nebo_raketa/36262), [area warning](https://t.me/kyiv_airdef/41075) |
| Теличка | Common grammatical forms. | [drone route](https://t.me/nebo_raketa/36022), [locality list](https://t.me/kyiv_airdef/40137) |
| Троєщина | Full name plus established `Троя`, `Трої`, and `Трою` slang. | [full name](https://t.me/nebo_raketa/36543), [slang](https://t.me/nebo_raketa/36953), [cross-channel use](https://t.me/kyiv_monit0ring/26860) |

### Accepted localities validated by nationwide channels

| Locality | Matching explanation | Evidence |
|---|---|---|
| Березняки | Plural grammatical forms. | [paired route](https://t.me/operinform/54745), [missile alert](https://t.me/war_monitor/41110) |
| Біличі | Plural grammatical forms. | [paired route](https://t.me/operinform/54724), [missile route](https://t.me/war_monitor/41115) |
| Биківня | Common grammatical forms. | [paired route](https://t.me/operinform/54223), [missile route](https://t.me/war_monitor/41307) |
| Відрадний | Accept the observed `Відрандний` misspelling. | [paired route](https://t.me/operinform/54723), [reactive-drone alert](https://t.me/war_monitor/41367) |
| Віта-Литовська | Require the full two-word name with a hyphen or space; bare `Віта` is ambiguous. | [drone route](https://t.me/war_monitor/41081) |
| Гідропарк | Common grammatical forms. | [drone route](https://t.me/operinform/54208) |
| Звіринець | Common grammatical forms. | [drone alert](https://t.me/war_monitor/41316), [paired route](https://t.me/war_monitor/41087) |
| Куренівка | Common grammatical forms. | [missile alert](https://t.me/operinform/55021), [drone route](https://t.me/war_monitor/41155) |
| Нижні Сади | Both words inflect as a phrase. | [paired route](https://t.me/operinform/54718), [direct warning](https://t.me/operinform/54568) |
| Острів Муромець | `Острів` is optional; useful alert zone although it is an island, not a neighborhood. | [direct warning](https://t.me/operinform/54249), [route](https://t.me/war_monitor/41289) |
| Почайна | Observed grammatical forms. | [Obolon route](https://t.me/operinform/54382), [reactive-drone alert](https://t.me/war_monitor/41075), [paired route](https://t.me/AerisRimor/75931) |
| Пріорка | Common grammatical forms. | [drone route](https://t.me/operinform/54298) |
| Русанівські Сади | Both words inflect as a phrase. | [drone warning](https://t.me/operinform/54741), [missile alert](https://t.me/operinform/54330) |
| Сирець | Common grammatical forms. | [paired route](https://t.me/operinform/54722), [route correction](https://t.me/AerisRimor/76007) |
| Теремки | Plural grammatical forms. | [reactive-drone route](https://t.me/war_monitor/41136), [paired route](https://t.me/AerisRimor/74334) |
| Чоколівка | Common grammatical forms. | [Kyiv alert](https://t.me/war_monitor/41142) |

### Deferred findings

| Candidate | Why deferred | Evidence |
|---|---|---|
| Озерна | Adjective/place name occurs elsewhere and may mean the metro station. | [grouped warning](https://t.me/operinform/54499), [route](https://t.me/operinform/54377) |
| Іподром | Landmark, not a neighborhood; same channel also uses it for Odesa. | [Kyiv route](https://t.me/AerisRimor/73795) |
| Вокзал | Broad landmark used in every city. | [direct route](https://t.me/AerisRimor/75884), [paired route](https://t.me/AerisRimor/75909) |
| Нова забудова | Generic wording rather than a stable locality label. | [Solomianka route](https://t.me/war_monitor/41303), [Zhuliany route](https://t.me/war_monitor/41309) |
| Голос | Ordinary word and unrelated organization name; ambiguous Holosiiv shorthand. | [drone route](https://t.me/AerisRimor/73886) |
| Заспа | Omits `Конча` and is ambiguous outside Kyiv-specific context. | [drone route](https://t.me/AerisRimor/74325), [direct warning](https://t.me/AerisRimor/73879) |
| Борщагівка / Борщага | Overlaps Petropavlivska and Sofiivska Borshchahivka outside Kyiv. | [locality](https://t.me/kyiv_airdef/41898), [slang](https://t.me/kyiv_airdef/40131), [national shorthand](https://t.me/AerisRimor/75985) |
| Микільська Борщагівка | Overlaps a possible generic Borshchahivka preset. | [direct route](https://t.me/kyiv_airdef/40131), [grouped warning](https://t.me/kyiv_airdef/41075) |
| Південна Борщагівка | Only bare `Південна` was observed, while the safe full phrase would not match it. | [grouped warning](https://t.me/kyiv_airdef/41075) |
| Соломʼянка / Солома | `Солома` is an ordinary word; district forms need apostrophe variants. | [slang alert](https://t.me/kyiv_airdef/40793), [district warning](https://t.me/nebo_raketa/36672) |
| Харківський масив | Bare adjective also describes Kharkiv city, district, or oblast. | [full name](https://t.me/kyiv_airdef/40137), [shorthand](https://t.me/kyiv_airdef/41374) |
| Центр | Matches shopping centers and the center of any city or region. | [ballistic alert](https://t.me/nebo_raketa/36223), [drone alert](https://t.me/nebo_raketa/35936) |
| Поштова площа | Specific phrase, but landmark status and sparse evidence need review. | [direct warning](https://t.me/kyiv_airdef/40235) |
| Урядовий квартал | Specific phrase, but it is an alert zone rather than a neighborhood. | [area warning](https://t.me/kyiv_airdef/41075) |
| Хутір | Extremely ambiguous bare word; likely means Червоний Хутір. | [direct warning](https://t.me/kyiv_monit0ring/26550) |
| Лівий берег | Useful broad alert zone, not a neighborhood. | [missile warning](https://t.me/nebo_raketa/36054), [drone warning](https://t.me/kyiv_monit0ring/27057), [national shorthand](https://t.me/AerisRimor/76069) |
| Правий берег | Useful broad alert zone, not a neighborhood. | [missile warning](https://t.me/nebo_raketa/36260), [drone warning](https://t.me/kyiv_monit0ring/26750), [national shorthand](https://t.me/AerisRimor/73884) |
| Шевченківський район | Administrative adjective is unsafe without Kyiv context. | [district warning](https://t.me/nebo_raketa/36672) |
| Деснянський район | Bare `Десна` must remain excluded because it names a settlement north of Kyiv. | [district warning](https://t.me/nebo_raketa/36672) |
| Дніпровський район | Same adjective is widely used for other places and organizations. | [district report](https://t.me/nebo_raketa/36991) |

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
- [x] `scripts/test` — 72 tests passed.

## Implementation Notes

2026-07-22: Added all reviewed safe localities with Ukrainian canonical names,
alphabetically ordered stable keys, translation coverage, and focused regex
tests. Deferred ambiguous findings remain in `kyiv-neighborhood-implement.md`.
