# Kyiv neighborhood preset research

Status: review required. No new presets have been added to `presets.py` yet.

## Scope

- Window: 2026-06-24 through 2026-07-21.
- Kyiv-specific channels:
  - [Kyivskyi Kupol](https://telegram.me/s/nebo_raketa): 1,180 posts.
  - [Kyiv AirDefense](https://telegram.me/s/kyiv_airdef): 2,765 posts.
  - [Monitoring Kyiv](https://telegram.me/s/kyiv_monit0ring): 641 posts.
- Total: 4,586 dated posts; 1,555 contained alert or target-routing language.
- `kyivblabla` was not used: it now points to an unrelated channel created on 2026-07-15.
- Nationwide channels were not needed for this pass because the Kyiv sources provided enough recent evidence.
- Names were cross-checked against the Wikipedia category [Kyiv localities alphabetically](https://uk.wikipedia.org/wiki/Категорія:Місцевості_Києва_за_алфавітом). Telegram alert wording remains the source for proposed matching.

Regexes assume `re.IGNORECASE | re.UNICODE`. Similar spelling or grammatical forms are grouped into one regex. Different aliases use separate regexes.

## Existing presets

These are already in `presets.py`. Suggested changes are called out explicitly.

### Sviatoshyn (`kyiv_sviatoshyn`)

- Seen: `Святошин`, `Святошино`, `Святошинський`, `Святошинському`, `Святошинського`.
- Keep: `r"\bсвятошин(о|а|і)?\b"`.
- Add: `r"\bсвятошинськ(ий|ого|ому|им)\b"`.
- Evidence: [district form](https://t.me/nebo_raketa/36103), [locality form](https://t.me/kyiv_airdef/41898).

### Akademmistechko (`kyiv_akademmistechko`)

- Seen: `Академмістечко`; the existing short form `Академ` was found in earlier research.
- Keep: `r"\bакадем\b"`; `r"\bакадеммістечк(о|а|у|ом)\b"`.
- Evidence: [target route](https://t.me/nebo_raketa/37056).

### Antonov (`kyiv_antonov`)

- Seen: `Антонов` as the local alert label.
- Keep: `r"\bантонов(а)?\b"`.
- Evidence: [neighborhood list](https://t.me/kyiv_airdef/40137), [ballistic warning](https://t.me/kyiv_airdef/42528).
- Risk: can also refer to the company or airport.

### Nyvky (`kyiv_nyvky`)

- Seen: `Нивки`, `Нивок`.
- Keep: `r"\bнив(ки|ках|ками|ок)\b"`.
- Evidence: [ballistic warning](https://t.me/kyiv_airdef/42528).

### Vynohradar (`kyiv_vynohradar`)

- Seen: `Виноградар`.
- Keep: `r"\bвиноградар(а|і|ем)?\b"`.
- Evidence: [area warning](https://t.me/kyiv_airdef/41075).

## Strong new locality candidates

### Obolon (`kyiv_obolon`)

- Seen: `Оболонь`, `Оболонський`.
- Proposed: `r"\bоболон(ь|і|ню)\b"`; `r"\bоболонськ(ий|ого|ому|им)\b"`.
- Evidence: [drone route](https://t.me/kyiv_monit0ring/26928), [district warning](https://t.me/nebo_raketa/36672).

### Troieshchyna (`kyiv_troieshchyna`)

- Seen: `Троєщина`, `Троєщину`, `Троєщини`; slang `Троя`, `Трою`, `Трої`.
- Proposed: `r"\bтроєщин(а|и|і|у|ою)\b"`; `r"\bтро(я|ї|ю)\b"`.
- Evidence: [full name](https://t.me/nebo_raketa/36543), [slang](https://t.me/nebo_raketa/36953), [both channels](https://t.me/kyiv_monit0ring/26860).

### Pechersk (`kyiv_pechersk`)

- Seen: `Печерськ`, `Печерський`.
- Proposed: `r"\bпечерськ(ий|ого|ому|им)?\b"`.
- Evidence: [missile alert](https://t.me/nebo_raketa/36062), [area warning](https://t.me/kyiv_airdef/41075).

### Darnytsia (`kyiv_darnytsia`)

- Seen: `Дарниця`, `Дарницю`, `Дарницький`, `Дарницькому`.
- Proposed: `r"\bдарниц(я|і|ю|ею)\b"`; `r"\bдарницьк(ий|ого|ому|им)\b"`.
- Evidence: [direct warning](https://t.me/kyiv_monit0ring/26742), [district alert](https://t.me/kyiv_monit0ring/26629).

### Holosiiv (`kyiv_holosiiv`)

- Seen mostly as `Голосіївський` / `Голосіївському`.
- Proposed: `r"\bголосі(їв|єва|єві|єву|євом)\b"`; `r"\bголосіївськ(ий|ого|ому|им)\b"`.
- Evidence: [missile alert](https://t.me/nebo_raketa/36258), [district warning](https://t.me/nebo_raketa/36672).

### Zhuliany (`kyiv_zhuliany`)

- Seen: `Жуляни`, `Жулян`.
- Proposed: `r"\bжулян(и|ах|ами)?\b"`.
- Evidence: [neighborhood list](https://t.me/kyiv_airdef/40137), [area warning](https://t.me/kyiv_airdef/41075).

### Podil (`kyiv_podil`)

- Seen: `Поділ`, `Подільський`.
- Proposed: `r"\bпод(іл|олу|олі|олом)\b"`; `r"\bподільськ(ий|ого|ому|им)\b"`.
- Evidence: [direct warning](https://t.me/kyiv_monit0ring/26742), [district warning](https://t.me/nebo_raketa/36672).

### DVRZ (`kyiv_dvrz`)

- Seen: `ДВРЗ`, `дврз`.
- Proposed: `r"\bдврз\b"`.
- Evidence: [drone alert](https://t.me/nebo_raketa/36310), [route](https://t.me/kyiv_airdef/41623).

### Lukianivka (`kyiv_lukianivka`)

- Seen with straight and typographic apostrophes: `Лук'янівка`, `Лукʼянівка`.
- Proposed: `r"\bлук['’ʼ]?янів(ка|ки|ці|ку|кою)\b"`.
- Evidence: [alert](https://t.me/nebo_raketa/36972), [area warning](https://t.me/kyiv_airdef/41898).

### Pozniaky (`kyiv_pozniaky`)

- Seen: `Позняки`.
- Proposed: `r"\bпозняк(и|ів|ах|ами)\b"`.
- Evidence: [route](https://t.me/nebo_raketa/36287), [area warning](https://t.me/kyiv_airdef/41075).

### Osokorky (`kyiv_osokorky`)

- Seen: `Осокорки`.
- Proposed: `r"\bосокорк(и|ів|ах|ами)\b"`.
- Evidence: [drone route](https://t.me/nebo_raketa/36301), [paired warning](https://t.me/nebo_raketa/36275).

### Bortnychi (`kyiv_bortnychi`)

- Seen: `Бортничі`.
- Proposed: `r"\bбортнич(і|ів|ах|ами)\b"`.
- Evidence: [direct warning](https://t.me/kyiv_monit0ring/26742), [target route](https://t.me/nebo_raketa/36496).

### Voskresenka (`kyiv_voskresenka`)

- Seen: `Воскресенка`, `Воскресенку`; misspelling `Восресенку`.
- Proposed: `r"\bвос(к)?ресенк(а|и|у|ою|ці)\b"`.
- Evidence: [warning](https://t.me/kyiv_airdef/41806), [route](https://t.me/kyiv_airdef/41736).

### Mysholovka (`kyiv_mysholovka`)

- Seen: `Мишоловка`.
- Proposed: `r"\bмишоловк(а|и|у|ою|ці)\b"`.
- Evidence: [drone alert](https://t.me/nebo_raketa/36051), [paired route](https://t.me/nebo_raketa/36275).

### Rusanivka (`kyiv_rusanivka`)

- Seen: `Русанівка`.
- Proposed: `r"\bрусанів(ка|ки|ці|ку|кою)\b"`.
- Evidence: [missile alert](https://t.me/nebo_raketa/35862), [multi-area drone alert](https://t.me/nebo_raketa/36236).
- Do not add bare `Русанів`: recent posts use it for the separate Kyiv Oblast settlement.

### Berkovets (`kyiv_berkovets`)

- Seen: `Берковець`.
- Proposed: `r"\bберков(ець|ця|ці|цем)\b"`.
- Evidence: [drone alert](https://t.me/kyiv_airdef/40985).

### Pushcha-Vodytsia (`kyiv_pushcha_vodytsia`)

- Seen: `Пуща-Водиця`, `Пуща-Водицю`.
- Proposed: `r"\bпущ(а|і|у|ею)[ -]водиц(я|і|ю|ею)\b"`.
- Evidence: [drone alert](https://t.me/nebo_raketa/36239), [route](https://t.me/kyiv_airdef/40191).

### Rembaza (`kyiv_rembaza`)

- Seen: `Рембаза`.
- Proposed: `r"\bрембаз(а|и|і|у|ою)\b"`.
- Evidence: [direct warning](https://t.me/kyiv_monit0ring/26550), [area warning](https://t.me/kyiv_airdef/41075).

### Vydubychi (`kyiv_vydubychi`)

- Seen: `Видубичі`.
- Proposed: `r"\bвидубич(і|ів|ах|ами)\b"`.
- Evidence: [missile alert](https://t.me/nebo_raketa/36255).

### Demiivka (`kyiv_demiivka`)

- Seen: `Деміївка`.
- Proposed: `r"\bдеміївк(а|и|у|ою|ці)\b"`.
- Evidence: [area warning](https://t.me/kyiv_airdef/41075).

### Klov (`kyiv_klov`)

- Seen: `Клов`.
- Proposed: `r"\bклов(у|і|ом|а)?\b"`.
- Evidence: [area warning](https://t.me/kyiv_airdef/41075).

### Lypky (`kyiv_lypky`)

- Seen: `Липки`.
- Proposed: `r"\bлип(ки|ок|ках|ками)\b"`.
- Evidence: [area warning](https://t.me/kyiv_airdef/41075).

### Koncha-Zaspa (`kyiv_koncha_zaspa`)

- Seen: `Конча-Заспу`.
- Proposed: `r"\bконч(а|і)[ -]засп(а|и|і|у|ою)\b"`.
- Evidence: [drone route](https://t.me/nebo_raketa/36022), [course update](https://t.me/kyiv_airdef/40104).

### Shuliavka (`kyiv_shuliavka`)

- Seen: `Шулявка`.
- Proposed: `r"\bшулявк(а|и|у|ою|ці)\b"`.
- Evidence: [missile alert](https://t.me/nebo_raketa/36262), [area warning](https://t.me/kyiv_airdef/41075).

### Telychka (`kyiv_telychka`)

- Seen: `Теличка`, `Теличку`.
- Proposed: `r"\bтеличк(а|и|у|ою|ці)\b"`.
- Evidence: [drone route](https://t.me/nebo_raketa/36022), [city locality list](https://t.me/kyiv_airdef/40137).

### Lisovyi Masyv (`kyiv_lisovyi_masyv`)

- Seen: `Лісовий масив`; shorthand `Лісовий`.
- Safer: `r"\bлісов(ий|ого|ому|им) масив(у|і|ом|а)?\b"`.
- Optional risky alias: `r"\bлісов(ий|ого|ому|им)\b"`.
- Evidence: [full name](https://t.me/nebo_raketa/35960), [shorthand](https://t.me/kyiv_airdef/41857).

### Minskyi Masyv (`kyiv_minskyi_masyv`)

- Seen: `Мінський масив`; shorthand `Мінський`.
- Safer: `r"\bмінськ(ий|ого|ому|им) масив(у|і|ом|а)?\b"`.
- Optional risky alias: `r"\bмінськ(ий|ого|ому|им)\b"`.
- Evidence: [full name](https://t.me/nebo_raketa/36100), [shorthand](https://t.me/kyiv_airdef/40903).
- Risk: shorthand can describe Minsk rather than the Kyiv locality.

### Livoberezhnyi Masyv (`kyiv_livoberezhnyi_masyv`)

- Seen: `Лівобережний масив`.
- Proposed: `r"\bлівобережн(ий|ого|ому|им) масив(у|і|ом|а)?\b"`.
- Evidence: [route](https://t.me/kyiv_airdef/41736), [ballistic warning](https://t.me/kyiv_airdef/42528).

## Informal, overlapping, or higher-risk candidates

### Borshchahivka / Borshchaha (`kyiv_borshchahivka`)

- Seen: `Борщагівка`, `Борщагівки`, `Борщагу`; generic plural `Борщагівки`.
- Proposed: `r"\bборщаг(а|и|у|ою|івк(а|и|у|ою|ці)|івок)\b"`.
- Evidence: [generic locality](https://t.me/kyiv_airdef/41898), [slang](https://t.me/kyiv_airdef/40131).
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

- Seen: `лівий берег`, `ЛІВИЙ БЕРЕГ`.
- Proposed: `r"\bлів(ий|ого|ому|им) берег(а|у|ом|і)?\b"`.
- Evidence: [missile warning](https://t.me/nebo_raketa/36054), [drone warning](https://t.me/kyiv_monit0ring/27057).
- Note: useful alert zone, but not a neighborhood.

### Right Bank (`kyiv_right_bank`)

- Seen: `правий берег`.
- Proposed: `r"\bправ(ий|ого|ому|им) берег(а|у|ом|і)?\b"`.
- Evidence: [missile warning](https://t.me/nebo_raketa/36260), [drone warning](https://t.me/kyiv_monit0ring/26750).
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
- `Березняки` was confused with `Березань` and the month `березня`; no alert evidence was found.
- `Почайна` appeared only in a transport-news post, not a danger report.
- `Дорогожичі`, `Куренівка`, `Пріорка`, and `Новокараваєві Дачі` were fuzzy-search false positives; no exact recent alert mention was found.
- `Спуск` means a missile launch in these channels, not a Kyiv locality.

## Review questions

1. Include administrative districts as selectable presets, or only localities?
2. Include broad zones (`Center`, `Left Bank`, `Right Bank`)?
3. Keep risky shorthand (`Soloma`, `Minskyi`, `Lisovyi`, `Kharkivskyi`, `Khutir`)?
4. Keep both generic and specific Borshchahivka presets despite overlap?
5. After selection, should repeated/forwarded Telegram posts be added as explicit regex test cases?
