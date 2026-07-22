# Kyiv neighborhood preset research

Status: safe locality presets added to `presets.py`. Higher-risk, informal, broad-zone, and administrative candidates still require review.

## Scope

- Window: 2026-06-24 through 2026-07-21.
- Kyiv-specific channels:
  - [Kyivskyi Kupol](https://telegram.me/s/nebo_raketa): 1,180 posts.
  - [Kyiv AirDefense](https://telegram.me/s/kyiv_airdef): 2,765 posts.
  - [Monitoring Kyiv](https://telegram.me/s/kyiv_monit0ring): 641 posts.
- Nationwide channels:
  - [Operatyvnyi Inform](https://telegram.me/s/operinform): 1,006 posts.
  - [War Monitor](https://telegram.me/s/war_monitor): 891 posts.
  - [Aeris Rimor](https://telegram.me/s/AerisRimor): 2,993 posts.
  - [Air Force of Ukraine](https://telegram.me/s/kpszsu): 3,430 posts.
- Total: 12,906 dated posts. The national pass added 8,320 posts.
- Nationwide posts were counted only as locality evidence when they contained live target-routing or warning language. Aftermath reports, forecasts, and unrelated same-name places were excluded.
- The Air Force channel reports mostly at region or settlement level. It did not provide reliable Kyiv-locality validation in this window, but it exposed collisions for district adjectives such as `Дніпровський`, `Шевченківський`, and `Харківський`.
- Names were cross-checked against the Wikipedia category [Kyiv localities alphabetically](https://uk.wikipedia.org/wiki/Категорія:Місцевості_Києва_за_алфавітом). Telegram alert wording remains the source for proposed matching.

Regexes assume `re.IGNORECASE | re.UNICODE`. Similar spelling or grammatical forms are grouped into one regex. Different aliases use separate regexes.

## National-channel validation

The national pass independently confirmed live alert use for these existing entries:

- Existing presets: Sviatoshyn, Akademmistechko (`Академ`), Antonov, Nyvky, and Vynohradar.
- Strong candidates: Obolon, Troieshchyna, Pechersk, Darnytsia, Zhuliany, Podil, DVRZ, Lukianivka, Pozniaky, Osokorky, Bortnychi, Voskresenka, Rusanivka, Berkovets, Pushcha-Vodytsia, Rembaza, Vydubychi, Demiivka, Shuliavka, Telychka, Lisovyi Masyv, Minskyi Masyv, and Livoberezhnyi Masyv.
- Higher-risk entries: generic Borshchahivka, Solomianka, Kharkivskyi Masyv, Center, Left Bank, Right Bank, and Dniprovskyi district.

Representative cross-channel evidence: [Nyvky and Syrets](https://t.me/operinform/54722), [Obolon and Kurenivka](https://t.me/war_monitor/41313), [Antonov, Lukianivka, and Syrets](https://t.me/AerisRimor/75984), [DVRZ and Lisovyi Masyv](https://t.me/operinform/55001), and [Telychka and Vydubychi](https://t.me/war_monitor/41366).

No additional live national-channel evidence was found for Mysholovka, Klov, Lypky, Government Quarter, Poshtova Ploshcha, Mykilska Borshchahivka, or Pivdenna Borshchahivka. Holosiiv appeared only as a district in aftermath reports; its shorthand `Голос` did appear in one live route update.

## New candidates from nationwide channels

These names were absent from the Kyiv-only pass but appeared in live Kyiv target-routing messages from nationwide channels.

## Informal, overlapping, or higher-risk candidates

### Ipodrom (`kyiv_ipodrom`)

- Seen: `Іподром` grouped with Teremky and Zhuliany.
- Proposed only if accepted: `r"\bіподром(у|і|ом|а)?\b"`.
- Evidence: [Kyiv route](https://t.me/AerisRimor/73795).
- Risk: a landmark, not a neighborhood, and the same channel also uses `Іподром` for Odesa.

### Vokzal (`kyiv_vokzal`)

- Seen: `Вокзал` grouped with Zhuliany.
- Proposed only if accepted: `r"\bвокзал(у|і|ом|а)?\b"`.
- Evidence: [direct route](https://t.me/AerisRimor/75884), [paired route](https://t.me/AerisRimor/75909).
- Risk: a broad landmark name used in every city.

### Nova Zabudova (`kyiv_nova_zabudova`)

- Seen: `нова забудова` paired separately with Solomianka and Zhuliany.
- Proposed only if accepted: `r"\bнов(а|ої|ій|у|ою) забудов(а|и|і|у|ою)\b"`.
- Evidence: [Solomianka route](https://t.me/war_monitor/41303), [Zhuliany route](https://t.me/war_monitor/41309).
- Risk: generic wording rather than a stable locality label.

### Holos alias for Holosiiv

- Seen: `Голос` paired with Telychka and Demiivka.
- Optional risky alias for `kyiv_holosiiv`: `r"\bголос\b"`.
- Evidence: [drone route](https://t.me/AerisRimor/73886).
- Risk: an ordinary Ukrainian word and the name of unrelated organizations.

### Zaspa alias for Koncha-Zaspa

- Seen: `Заспа` as a standalone route label.
- Optional risky alias for `kyiv_koncha_zaspa`: `r"\bзасп(а|и|і|у|ою)\b"`.
- Evidence: [Kyiv drone route](https://t.me/AerisRimor/74325), [direct warning](https://t.me/AerisRimor/73879).
- Risk: the shorthand omits `Конча` and may be ambiguous outside Kyiv-specific alert context.

### Borshchahivka / Borshchaha (`kyiv_borshchahivka`)

- Seen: `Борщагівка`, `Борщагівки`, `Борщагу`; national channels also use plural shorthand `Борщаги`.
- Proposed: `r"\bборщаг(а|и|у|ою|івк(а|и|у|ою|ці)|івок)\b"`.
- Evidence: [generic locality](https://t.me/kyiv_airdef/41898), [slang](https://t.me/kyiv_airdef/40131), [national-channel shorthand](https://t.me/AerisRimor/75985).
- Risk: also matches Petropavlivska and Sofiivska Borshchahivka outside Kyiv.

### Mykilska Borshchahivka (`kyiv_mykilska_borshchahivka`)

- Seen: `Микільська` inside a Borshchahivka list; `Микільську Борщагу`.
- Proposed: `r"\bмикільськ(а|ої|ій|у|ою) борщаг(а|и|у|ою|івк(а|и|у|ою|ці))\b"`.
- Evidence: [direct route](https://t.me/kyiv_airdef/40131), [grouped warning](https://t.me/kyiv_airdef/41075).
- Risk: overlaps the generic Borshchahivka preset.

### Pivdenna Borshchahivka (`kyiv_pivdenna_borshchahivka`)

- Seen only as shorthand `Південна` inside a Borshchahivka list.
- Safer proposed: `r"\bпівденн(а|ої|ій|у|ою) борщагівк(а|и|у|ою|ці)\b"`.
- Evidence: [grouped warning](https://t.me/kyiv_airdef/41075).
- Risk: the safe regex does not match the observed shorthand; bare `Південна` is too broad.

### Solomianka / Soloma (`kyiv_solomianka`)

- Seen: slang `Солома`; administrative `Солом'янський`, `Соломʼянський`, `Солом’янський`.
- Proposed: `r"\bсолом(а|['’ʼ]?янк(а|и|у|ою|ці))\b"`; `r"\bсолом['’ʼ]?янськ(ий|ого|ому|им)\b"`.
- Evidence: [slang alert](https://t.me/kyiv_airdef/40793), [district warning](https://t.me/nebo_raketa/36672).
- Risk: bare `солома` is an ordinary Ukrainian word.

### Kharkivskyi Masyv (`kyiv_kharkivskyi_masyv`)

- Seen: `Харківський масив`; shorthand `Харківський`.
- Safer: `r"\bхарківськ(ий|ого|ому|им) масив(у|і|ом|а)?\b"`.
- Optional risky alias: `r"\bхарківськ(ий|ого|ому|им)\b"`.
- Evidence: [full name](https://t.me/kyiv_airdef/40137), [shorthand missile alert](https://t.me/kyiv_airdef/41374).
- Risk: shorthand also describes Kharkiv city, district, or oblast.

### Center (`kyiv_center`)

- Seen: `Центр` in direct drone, cruise, and ballistic warnings.
- Proposed: `r"\bцентр(у|і|ом|а)?\b"`.
- Evidence: [ballistic alert](https://t.me/nebo_raketa/36223), [drone alert](https://t.me/nebo_raketa/35936).
- Risk: very broad; also matches shopping centers and the center of any city or region.

### Poshtova Ploshcha (`kyiv_poshtova_ploshcha`)

- Seen: `Поштова площа`.
- Proposed: `r"\bпоштов(а|ої|ій|у|ою) площ(а|і|у|ею)\b"`.
- Evidence: [direct warning](https://t.me/kyiv_airdef/40235).

### Government Quarter (`kyiv_government_quarter`)

- Seen: `Урядового кварталу`.
- Proposed: `r"\bурядов(ий|ого|ому|им) квартал(у|і|ом|а)?\b"`.
- Evidence: [area warning](https://t.me/kyiv_airdef/41075).

### Khutir (`kyiv_khutir`)

- Seen: bare `Хутір` paired with Rembaza; likely Chervonyi Khutir.
- Proposed only if accepted: `r"\bхутір\b"`.
- Evidence: [direct warning](https://t.me/kyiv_monit0ring/26550).
- Risk: extremely ambiguous and may refer to any settlement or locality.

### Left Bank (`kyiv_left_bank`)

- Seen: `лівий берег`, `ЛІВИЙ БЕРЕГ`; national channels also use `лівобережжя`, `лівобережжя столиці`.
- Proposed: `r"\bлів(ий|ого|ому|им) берег(а|у|ом|і)?\b"`; `r"\bлівобережж(я|і|ю|ям)\b"`.
- Evidence: [missile warning](https://t.me/nebo_raketa/36054), [drone warning](https://t.me/kyiv_monit0ring/27057), [national-channel shorthand](https://t.me/AerisRimor/76069).
- Note: useful alert zone, but not a neighborhood.

### Right Bank (`kyiv_right_bank`)

- Seen: `правий берег`; national channels also use `Правобережжя`.
- Proposed: `r"\bправ(ий|ого|ому|им) берег(а|у|ом|і)?\b"`; `r"\bправобережж(я|і|ю|ям)\b"`.
- Evidence: [missile warning](https://t.me/nebo_raketa/36260), [drone warning](https://t.me/kyiv_monit0ring/26750), [national-channel shorthand](https://t.me/AerisRimor/73884).
- Note: useful alert zone, but not a neighborhood.

## Administrative district candidates

Several locality presets above can also absorb their same-root district form: Pechersk, Darnytsia, Holosiiv, Obolon, Podil, Solomianka, and Sviatoshyn. Three district names have no equivalent locality candidate in this note.

### Shevchenkivskyi district (`kyiv_shevchenkivskyi`)

- Seen: `Шевченківський`, `Шевченківському`.
- Proposed: `r"\bшевченківськ(ий|ого|ому|им)\b"`.
- Evidence: [district warning](https://t.me/nebo_raketa/36672).

### Desnianskyi district (`kyiv_desnianskyi`)

- Seen: `Деснянський`, `Деснянському`.
- Proposed: `r"\bдеснянськ(ий|ого|ому|им)\b"`.
- Evidence: [district warning](https://t.me/nebo_raketa/36672).
- Do not add bare `Десна`: recent route posts use the Desna settlement north of Kyiv.

### Dniprovskyi district (`kyiv_dniprovskyi`)

- Seen: `Дніпровський`, `Дніпровському`.
- Proposed: `r"\bдніпровськ(ий|ого|ому|им)\b"`.
- Evidence: [district report](https://t.me/nebo_raketa/36991).
- Risk: the same adjective is used for other places and organizations.

## Nearby or non-Kyiv names found in the same alerts

Do not nest these under the Kyiv city preset without an explicit product decision:

- `Бровари`; slang `Борік`.
- `Бориспіль`; `Борисполя`, `Борисполем`.
- `Вишгород`, `Вишневе`, `Ірпінь`, `Буча`, `Гостомель`, `Ворзель`.
- `Петропавлівська Борщагівка`, `Софіївська Борщагівка`, `ЖК Софія`.
- `Чайки`, `Коцюбинське`, `Проліски`, `Гнідин`, `Козин`, `Обухів`, `Васильків`.
- `Погреби`, `Зазим'я`, `Хотянівка`, `Петрівці`, `Димер`, `Десна`.
- `Русанів` is a separate settlement and must not be treated as an inflection of Kyiv's `Русанівка`.

## False-positive traps found during extraction

- `Віта` was extracted from `Віталій` and the verb `вітають`; it is not evidence for a Vita preset.
- `Ліски` was extracted from `Проліски`; it is not evidence for the Kyiv locality.
- `Поштова` in [this grouped alert](https://t.me/war_monitor/41027) is part of `Віта-Поштова`, not evidence for Poshtova Ploshcha.
- `Райдужний`, `Школьний`, `Вузівський`, `Іподром`, and `Черемушки` occur in an Odesa routing sequence; only the separate Kyiv `Іподром/Теремки/Жуляни` sequence counts as Kyiv evidence.
- `Дорогожичі` and `Новокараваєві Дачі` remain fuzzy-search false positives; no exact recent live alert mention was found in either pass.
- `Березняки`, `Почайна`, `Куренівка`, and `Пріорка` are no longer considered false positives: national channels supplied direct live alert evidence.
- Bare district adjectives are unsafe nationally: `Дніпровський`, `Шевченківський`, and `Харківський` frequently describe non-Kyiv places. Prefer a Kyiv context or a full locality phrase such as `Харківський масив`.
- `Спуск` means a missile launch in these channels, not a Kyiv locality.

## Review questions

1. Include administrative districts as selectable presets, or only localities?
2. Include broad zones (`Center`, `Left Bank`, `Right Bank`)?
3. Keep risky shorthand (`Soloma`, `Minskyi`, `Lisovyi`, `Kharkivskyi`, `Khutir`)?
4. Keep both generic and specific Borshchahivka presets despite overlap?
5. After selection, should repeated/forwarded Telegram posts be added as explicit regex test cases?
