"""Area pattern presets for Aerial Danger."""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class LocalityPreset:
    """Locality preset definition."""

    name: str
    patterns: tuple[str, ...]


@dataclass(frozen=True)
class RegionPreset:
    """Region preset definition and its localities."""

    name: str
    patterns: tuple[str, ...]
    localities: dict[str, LocalityPreset]


PRESETS: Final = {
    "kyiv": RegionPreset(
        name="Київ",
        patterns=(
            r"\bки(їв|єва|єві|єву|євом)\b",
            r"\bстолиц(я|і|ю|ею)\b",
        ),
        localities={
            "kyiv_akademmistechko": LocalityPreset(
                name="Академмістечко",
                patterns=(r"\bакадем\b", r"\bакадеммістечк(о|а|у|ом)\b"),
            ),
            "kyiv_antonov": LocalityPreset(
                name="Антонов", patterns=(r"\bантонов(а)?\b",)
            ),
            "kyiv_berezniaky": LocalityPreset(
                name="Березняки", patterns=(r"\bберезняк(и|ів|ах|ами)\b",)
            ),
            "kyiv_berkovets": LocalityPreset(
                name="Берковець", patterns=(r"\bберков(ець|ця|ці|цем)\b",)
            ),
            "kyiv_bilychi": LocalityPreset(
                name="Біличі", patterns=(r"\bбілич(і|ів|ах|ами)\b",)
            ),
            "kyiv_borshchahivka": LocalityPreset(
                name="Борщагівка",
                patterns=(r"\bборщаг(а|и|у|ою|івк(а|и|у|ою|ці)|івок)\b",),
            ),
            "kyiv_bortnychi": LocalityPreset(
                name="Бортничі", patterns=(r"\bбортнич(і|ів|ах|ами)\b",)
            ),
            "kyiv_bykivnia": LocalityPreset(
                name="Биківня", patterns=(r"\bбиківн(я|і|ю|ею)\b",)
            ),
            "kyiv_center": LocalityPreset(
                name="Центр", patterns=(r"\bцентр(у|і|ом|а)?\b",)
            ),
            "kyiv_chokolivka": LocalityPreset(
                name="Чоколівка", patterns=(r"\bчоколівк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_darnytsia": LocalityPreset(
                name="Дарниця",
                patterns=(
                    r"\bдарниц(я|і|ю|ею)\b",
                    r"\bдарницьк(ий|ого|ому|им)(?: масив(у|і|ом|а)?)?\b",
                ),
            ),
            "kyiv_demiivka": LocalityPreset(
                name="Деміївка", patterns=(r"\bдеміївк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_dorohzhychi": LocalityPreset(
                name="Дорогожичі", patterns=(r"\bдорогожич(і|ів|ам|ами|ах)\b",)
            ),
            "kyiv_dvrz": LocalityPreset(name="ДВРЗ", patterns=(r"\bдврз\b",)),
            "kyiv_halahany": LocalityPreset(
                name="Галагани", patterns=(r"\bгалаган(и|ів|ам|ами|ах)?\b",)
            ),
            "kyiv_hidropark": LocalityPreset(
                name="Гідропарк", patterns=(r"\bгідропарк(у|і|ом|а)?\b",)
            ),
            "kyiv_holosiiv": LocalityPreset(
                name="Голосіїв",
                patterns=(
                    r"\bголосі(їв|єва|єві|єву|євом)\b",
                    r"\bголосіївськ(ий|ого|ому|им)\b",
                    r"\bголос\b",
                ),
            ),
            "kyiv_ipodrom": LocalityPreset(
                name="Іподром", patterns=(r"\bіподром(у|і|ом|а)?\b",)
            ),
            "kyiv_karavaievi_dachi": LocalityPreset(
                name="Караваєві Дачі",
                patterns=(
                    r"\bкараваєв(і дачі|их дач|им дачам|ими дачами|их дачах)\b",
                    r"\bкардач(і|ів|ам|ами|ах)\b",
                ),
            ),
            "kyiv_kharkivskyi_masyv": LocalityPreset(
                name="Харківський масив",
                patterns=(r"\bхарківськ(ий|ого|ому|им)(?: масив(у|і|ом|а)?)?\b",),
            ),
            "kyiv_khutir": LocalityPreset(
                name="Червоний Хутір",
                patterns=(
                    r"\bчервон(ий|ого|ому|им) хут(ір|ор(а|у|і|ом|е))\b",
                    r"\bхутір\b",
                ),
            ),
            "kyiv_klov": LocalityPreset(
                name="Клов", patterns=(r"\bклов(у|і|ом|а)?\b",)
            ),
            "kyiv_koncha_zaspa": LocalityPreset(
                name="Конча-Заспа",
                patterns=(
                    r"\bконч(а|і)[ -]засп(а|и|і|у|ою)\b",
                    r"\bзасп(а|и|і|у|ою)\b",
                ),
            ),
            "kyiv_kpi": LocalityPreset(name="КПІ", patterns=(r"\bкпі\b",)),
            "kyiv_kurenivka": LocalityPreset(
                name="Куренівка", patterns=(r"\bкуренівк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_left_bank": LocalityPreset(
                name="Лівий берег",
                patterns=(
                    r"\bлів(ий|ого|ому|им) берег(а|у|ом|і)?\b",
                    r"\bлівобережж(я|і|ю|ям)\b",
                ),
            ),
            "kyiv_lisovyi_masyv": LocalityPreset(
                name="Лісовий масив",
                patterns=(r"\bлісов(ий|ого|ому|им)(?: масив(у|і|ом|а)?)?\b",),
            ),
            "kyiv_livoberezhnyi_masyv": LocalityPreset(
                name="Лівобережний масив",
                patterns=(r"\bлівобережн(ий|ого|ому|им)(?: масив(у|і|ом|а)?)?\b",),
            ),
            "kyiv_lukianivka": LocalityPreset(
                name="Лукʼянівка",
                patterns=(r"\bлук['’ʼ]?янів(ка|ки|ці|ку|кою)\b",),
            ),
            "kyiv_lypky": LocalityPreset(
                name="Липки", patterns=(r"\bлип(ки|ок|ках|ками)\b",)
            ),
            "kyiv_minskyi_masyv": LocalityPreset(
                name="Мінський масив",
                patterns=(r"\bмінськ(ий|ого|ому|им)(?: масив(у|і|ом|а)?)?\b",),
            ),
            "kyiv_muromets": LocalityPreset(
                name="Острів Муромець",
                patterns=(r"\b(острів )?муром(ець|ця|ці|цем)\b",),
            ),
            "kyiv_mysholovka": LocalityPreset(
                name="Мишоловка", patterns=(r"\bмишоловк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_nova_zabudova": LocalityPreset(
                name="Нова Забудова",
                patterns=(r"\bнов(а|ої|ій|у|ою) забудов(а|и|і|у|ою)\b",),
            ),
            "kyiv_nyvky": LocalityPreset(
                name="Нивки", patterns=(r"\bнив(ки|ках|ками|ок)\b",)
            ),
            "kyiv_nyzhni_sady": LocalityPreset(
                name="Нижні Сади",
                patterns=(r"\bнижн(і|іх|ім|ими) сад(и|ів|ах|ами)\b",),
            ),
            "kyiv_obolon": LocalityPreset(
                name="Оболонь",
                patterns=(
                    r"\bоболон(ь|і|ню)\b",
                    r"\bоболонськ(ий|ого|ому|им)\b",
                ),
            ),
            "kyiv_osokorky": LocalityPreset(
                name="Осокорки", patterns=(r"\bосокорк(и|ів|ах|ами)\b",)
            ),
            "kyiv_pechersk": LocalityPreset(
                name="Печерськ", patterns=(r"\bпечерськ(ий|ого|ому|им)?\b",)
            ),
            "kyiv_pochaiana": LocalityPreset(
                name="Почайна", patterns=(r"\bпочайн(а|и|і|у|ою|ої)\b",)
            ),
            "kyiv_podil": LocalityPreset(
                name="Поділ",
                patterns=(
                    r"\bпод(іл|олу|олі|олом)\b",
                    r"\bподільськ(ий|ого|ому|им)\b",
                ),
            ),
            "kyiv_pozniaky": LocalityPreset(
                name="Позняки",
                patterns=(r"\bпозняк(и|ів|ах|ами)\b",),
            ),
            "kyiv_priorka": LocalityPreset(
                name="Пріорка", patterns=(r"\bпріорк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_pushcha_vodytsia": LocalityPreset(
                name="Пуща-Водиця",
                # TODO: пуща  # noqa: TD002
                patterns=(r"\bпущ(а|і|у|ею)[ -]водиц(я|і|ю|ею)\b",),
            ),
            "kyiv_rembaza": LocalityPreset(
                name="Рембаза", patterns=(r"\bрембаз(а|и|і|у|ою)\b",)
            ),
            "kyiv_right_bank": LocalityPreset(
                name="Правий берег",
                patterns=(
                    r"\bправ(ий|ого|ому|им) берег(а|у|ом|і)?\b",
                    r"\bправобережж(я|і|ю|ям)\b",
                ),
            ),
            "kyiv_rusanivka": LocalityPreset(
                name="Русанівка", patterns=(r"\bрусанів(ка|ки|ці|ку|кою)\b",)
            ),
            "kyiv_rusanivski_sady": LocalityPreset(
                name="Русанівські Сади",
                patterns=(r"\bрусанівськ(і|их|им|ими) сад(и|ів|ах|ами)\b",),
            ),
            "kyiv_shuliavka": LocalityPreset(
                name="Шулявка", patterns=(r"\bшулявк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_solomianka": LocalityPreset(
                name="Солом'янка",
                patterns=(
                    r"\bсолом(а|['’ʼ]?янк(а|и|у|ою|ці))\b",
                    r"\bсолом['’ʼ]?янськ(ий|ого|ому|им)\b",
                ),
            ),
            "kyiv_sviatoshyn": LocalityPreset(
                name="Святошин",
                patterns=(
                    r"\bсвятошин(о|а|і)?\b",
                    r"\bсвятошинськ(ий|ого|ому|им)\b",
                ),
            ),
            "kyiv_syrets": LocalityPreset(
                name="Сирець", patterns=(r"\bсир(ець|ця|ці|цем)\b",)
            ),
            "kyiv_telychka": LocalityPreset(
                name="Теличка", patterns=(r"\bтеличк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_teremky": LocalityPreset(
                name="Теремки", patterns=(r"\bтеремк(и|ів|ах|ами)\b",)
            ),
            "kyiv_troieshchyna": LocalityPreset(
                name="Троєщина",
                patterns=(
                    r"\bтроєщин(а|и|і|у|ою)\b",
                    r"\bтро(я|ї|ю)\b",
                ),
            ),
            "kyiv_vidradnyi": LocalityPreset(
                name="Відрадний", patterns=(r"\bвідра(д|нд)н(ий|ого|ому|им)\b",)
            ),
            "kyiv_vita_lytovska": LocalityPreset(
                name="Віта-Литовська",
                patterns=(r"\bвіта[ -]литовськ(а|ої|ій|у|ою)\b",),
            ),
            "kyiv_voskresenka": LocalityPreset(
                name="Воскресенка", patterns=(r"\bвос(к)?ресенк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_vydubychi": LocalityPreset(
                name="Видубичі", patterns=(r"\bвидубич(і|ів|ах|ами)\b",)
            ),
            "kyiv_vynohradar": LocalityPreset(
                name="Виноградар", patterns=(r"\bвиноградар(а|і|ем)?\b",)
            ),
            "kyiv_zhuliany": LocalityPreset(
                name="Жуляни", patterns=(r"\bжулян(и|ах|ами)?\b",)
            ),
            "kyiv_zvirynets": LocalityPreset(
                name="Звіринець", patterns=(r"\bзвірин(ець|ця|ці|цем)\b",)
            ),
        },
    ),
    "kyiv_oblast": RegionPreset(
        name="Київська область",
        patterns=(
            r"\bкиївщин(а|и|і|у|ою)\b",
            r"\bкиївськ(а|ої|ій|у|ою|і|их|им|ими) област(ь|і|ю|ей|ям|ями|ях)\b",
        ),
        localities={
            "kyiv_oblast_boryspil": LocalityPreset(
                name="Бориспіль",
                patterns=(
                    r"\bборисп(іль|оля|олю|олем|олі)\b",
                    r"\bборік\b",
                ),
            ),
            "kyiv_oblast_brovary": LocalityPreset(
                name="Бровари",
                patterns=(r"\bбровар(и|ів|ам|ами|ах)\b",),
            ),
            "kyiv_oblast_bucha": LocalityPreset(
                name="Буча", patterns=(r"\bбуч(а|і|у|ею)\b",)
            ),
            "kyiv_oblast_chaiky": LocalityPreset(
                name="Чайки", patterns=(r"\bчайк(и|ів|ам|ами|ах)\b",)
            ),
            "kyiv_oblast_dymer": LocalityPreset(
                name="Димер", patterns=(r"\bдимер(а|у|ом|і)?\b",)
            ),
            "kyiv_oblast_hnidyn": LocalityPreset(
                name="Гнідин", patterns=(r"\bгнідин(а|у|ом|і)?\b",)
            ),
            "kyiv_oblast_hostomel": LocalityPreset(
                name="Гостомель", patterns=(r"\bгостомел(ь|я|ю|ем|і)\b",)
            ),
            "kyiv_oblast_hotianivka": LocalityPreset(
                name="Хотянівка", patterns=(r"\bхотянівк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_oblast_irpin": LocalityPreset(
                name="Ірпінь", patterns=(r"\bірп(інь|еня|еню|енем|ені)\b",)
            ),
            "kyiv_oblast_kotsiubynske": LocalityPreset(
                name="Коцюбинське", patterns=(r"\bкоцюбинськ(е|ого|ому|им|ім)\b",)
            ),
            "kyiv_oblast_kozyn": LocalityPreset(
                name="Козин", patterns=(r"\bкозин(а|у|ом|і)?\b",)
            ),
            "kyiv_oblast_obukhiv": LocalityPreset(
                name="Обухів", patterns=(r"\bобух(ів|ова|ову|овом|ові)\b",)
            ),
            "kyiv_oblast_petrivtsi": LocalityPreset(
                name="Петрівці", patterns=(r"\bпетрівц(і|ів|ям|ями|ях)\b",)
            ),
            "kyiv_oblast_petropavlivska_borshchahivka": LocalityPreset(
                name="Петропавлівська Борщагівка",
                patterns=(
                    r"\bпетропавлівськ(а|ої|ій|у|ою) борщагівк(а|и|і|у|ою|ці)\b",
                ),
            ),
            "kyiv_oblast_pohreby": LocalityPreset(
                name="Погреби", patterns=(r"\bпогреб(и|ів|ам|ами|ах)\b",)
            ),
            "kyiv_oblast_prolisky": LocalityPreset(
                name="Проліски", patterns=(r"\bпроліс(ки|ків|кам|ками|ках)\b",)
            ),
            "kyiv_oblast_sofiivska_borshchahivka": LocalityPreset(
                name="Софіївська Борщагівка",
                patterns=(r"\bсофіївськ(а|ої|ій|у|ою) борщагівк(а|и|і|у|ою|ці)\b",),
            ),
            "kyiv_oblast_ukrainka": LocalityPreset(
                name="Українка", patterns=(r"\bукраїнк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_oblast_vasylkiv": LocalityPreset(
                name="Васильків", patterns=(r"\bвасильков(а|у|ом|і)?\b",)
            ),
            "kyiv_oblast_vorzel": LocalityPreset(
                name="Ворзель", patterns=(r"\bворзел(ь|я|ю|ем|і)\b",)
            ),
            "kyiv_oblast_vyshhorod": LocalityPreset(
                name="Вишгород", patterns=(r"\bвишгород(у|і|ом|а)?\b",)
            ),
            "kyiv_oblast_vyshneve": LocalityPreset(
                name="Вишневе", patterns=(r"\bвишнев(е|ого|ому|им|ім)\b",)
            ),
            "kyiv_oblast_zazyma": LocalityPreset(
                name="Зазим'я", patterns=(r"\bзазим['’ʼ]?(я|ї|ям)\b",)
            ),
            "kyiv_oblast_zhk_sofiia": LocalityPreset(
                name="ЖК Софія", patterns=(r"\bжк[. ]+[«\"]?софі(я|ї|ю|єю)\b",)
            ),
        },
    ),
}
