"""Area pattern presets for Aerial Danger."""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class NeighborhoodPreset:
    """Neighborhood preset definition."""

    name: str
    patterns: tuple[str, ...]


@dataclass(frozen=True)
class RegionPreset:
    """Region preset definition and its neighborhoods."""

    name: str
    patterns: tuple[str, ...]
    neighborhoods: dict[str, NeighborhoodPreset]


PRESETS: Final = {
    "kyiv": RegionPreset(
        name="Київ",
        patterns=(
            r"\bки(їв|єва|єві|єву|євом)\b",
            r"\bстолиц(я|і|ю|ею)\b",
        ),
        neighborhoods={
            "kyiv_akademmistechko": NeighborhoodPreset(
                name="Академмістечко",
                patterns=(r"\bакадем\b", r"\bакадеммістечк(о|а|у|ом)\b"),
            ),
            "kyiv_antonov": NeighborhoodPreset(
                name="Антонов", patterns=(r"\bантонов(а)?\b",)
            ),
            "kyiv_berezniaky": NeighborhoodPreset(
                name="Березняки", patterns=(r"\bберезняк(и|ів|ах|ами)\b",)
            ),
            "kyiv_berkovets": NeighborhoodPreset(
                name="Берковець", patterns=(r"\bберков(ець|ця|ці|цем)\b",)
            ),
            "kyiv_bilychi": NeighborhoodPreset(
                name="Біличі", patterns=(r"\bбілич(і|ів|ах|ами)\b",)
            ),
            "kyiv_borshchahivka": NeighborhoodPreset(
                name="Борщагівка",
                patterns=(r"\bборщаг(а|и|у|ою|івк(а|и|у|ою|ці)|івок)\b",),
            ),
            "kyiv_bortnychi": NeighborhoodPreset(
                name="Бортничі", patterns=(r"\bбортнич(і|ів|ах|ами)\b",)
            ),
            "kyiv_bykivnia": NeighborhoodPreset(
                name="Биківня", patterns=(r"\bбиківн(я|і|ю|ею)\b",)
            ),
            "kyiv_center": NeighborhoodPreset(
                name="Центр", patterns=(r"\bцентр(у|і|ом|а)?\b",)
            ),
            "kyiv_chokolivka": NeighborhoodPreset(
                name="Чоколівка", patterns=(r"\bчоколівк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_darnytsia": NeighborhoodPreset(
                name="Дарниця",
                patterns=(
                    r"\bдарниц(я|і|ю|ею)\b",
                    r"\bдарницьк(ий|ого|ому|им)(?: масив(у|і|ом|а)?)?\b",
                ),
            ),
            "kyiv_demiivka": NeighborhoodPreset(
                name="Деміївка", patterns=(r"\bдеміївк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_dorohzhychi": NeighborhoodPreset(
                name="Дорогожичі", patterns=(r"\bдорогожич(і|ів|ам|ами|ах)\b",)
            ),
            "kyiv_dvrz": NeighborhoodPreset(name="ДВРЗ", patterns=(r"\bдврз\b",)),
            "kyiv_halahany": NeighborhoodPreset(
                name="Галагани", patterns=(r"\bгалаган(и|ів|ам|ами|ах)?\b",)
            ),
            "kyiv_hidropark": NeighborhoodPreset(
                name="Гідропарк", patterns=(r"\bгідропарк(у|і|ом|а)?\b",)
            ),
            "kyiv_holosiiv": NeighborhoodPreset(
                name="Голосіїв",
                patterns=(
                    r"\bголосі(їв|єва|єві|єву|євом)\b",
                    r"\bголосіївськ(ий|ого|ому|им)\b",
                    r"\bголос\b",
                ),
            ),
            "kyiv_ipodrom": NeighborhoodPreset(
                name="Іподром", patterns=(r"\bіподром(у|і|ом|а)?\b",)
            ),
            "kyiv_karavaievi_dachi": NeighborhoodPreset(
                name="Караваєві Дачі",
                patterns=(
                    r"\bкараваєв(і дачі|их дач|им дачам|ими дачами|их дачах)\b",
                    r"\bкардач(і|ів|ам|ами|ах)\b",
                ),
            ),
            "kyiv_kharkivskyi_masyv": NeighborhoodPreset(
                name="Харківський масив",
                patterns=(r"\bхарківськ(ий|ого|ому|им)(?: масив(у|і|ом|а)?)?\b",),
            ),
            "kyiv_khutir": NeighborhoodPreset(
                name="Червоний Хутір",
                patterns=(
                    r"\bчервон(ий|ого|ому|им) хут(ір|ор(а|у|і|ом|е))\b",
                    r"\bхутір\b",
                ),
            ),
            "kyiv_klov": NeighborhoodPreset(
                name="Клов", patterns=(r"\bклов(у|і|ом|а)?\b",)
            ),
            "kyiv_koncha_zaspa": NeighborhoodPreset(
                name="Конча-Заспа",
                patterns=(
                    r"\bконч(а|і)[ -]засп(а|и|і|у|ою)\b",
                    r"\bзасп(а|и|і|у|ою)\b",
                ),
            ),
            "kyiv_kpi": NeighborhoodPreset(name="КПІ", patterns=(r"\bкпі\b",)),
            "kyiv_kurenivka": NeighborhoodPreset(
                name="Куренівка", patterns=(r"\bкуренівк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_left_bank": NeighborhoodPreset(
                name="Лівий берег",
                patterns=(
                    r"\bлів(ий|ого|ому|им) берег(а|у|ом|і)?\b",
                    r"\bлівобережж(я|і|ю|ям)\b",
                ),
            ),
            "kyiv_lisovyi_masyv": NeighborhoodPreset(
                name="Лісовий масив",
                patterns=(r"\bлісов(ий|ого|ому|им)(?: масив(у|і|ом|а)?)?\b",),
            ),
            "kyiv_livoberezhnyi_masyv": NeighborhoodPreset(
                name="Лівобережний масив",
                patterns=(r"\bлівобережн(ий|ого|ому|им)(?: масив(у|і|ом|а)?)?\b",),
            ),
            "kyiv_lukianivka": NeighborhoodPreset(
                name="Лукʼянівка",
                patterns=(r"\bлук['’ʼ]?янів(ка|ки|ці|ку|кою)\b",),
            ),
            "kyiv_lypky": NeighborhoodPreset(
                name="Липки", patterns=(r"\bлип(ки|ок|ках|ками)\b",)
            ),
            "kyiv_minskyi_masyv": NeighborhoodPreset(
                name="Мінський масив",
                patterns=(r"\bмінськ(ий|ого|ому|им)(?: масив(у|і|ом|а)?)?\b",),
            ),
            "kyiv_muromets": NeighborhoodPreset(
                name="Острів Муромець",
                patterns=(r"\b(острів )?муром(ець|ця|ці|цем)\b",),
            ),
            "kyiv_mysholovka": NeighborhoodPreset(
                name="Мишоловка", patterns=(r"\bмишоловк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_nova_zabudova": NeighborhoodPreset(
                name="Нова Забудова",
                patterns=(r"\bнов(а|ої|ій|у|ою) забудов(а|и|і|у|ою)\b",),
            ),
            "kyiv_nyvky": NeighborhoodPreset(
                name="Нивки", patterns=(r"\bнив(ки|ках|ками|ок)\b",)
            ),
            "kyiv_nyzhni_sady": NeighborhoodPreset(
                name="Нижні Сади",
                patterns=(r"\bнижн(і|іх|ім|ими) сад(и|ів|ах|ами)\b",),
            ),
            "kyiv_obolon": NeighborhoodPreset(
                name="Оболонь",
                patterns=(
                    r"\bоболон(ь|і|ню)\b",
                    r"\bоболонськ(ий|ого|ому|им)\b",
                ),
            ),
            "kyiv_osokorky": NeighborhoodPreset(
                name="Осокорки", patterns=(r"\bосокорк(и|ів|ах|ами)\b",)
            ),
            "kyiv_pechersk": NeighborhoodPreset(
                name="Печерськ", patterns=(r"\bпечерськ(ий|ого|ому|им)?\b",)
            ),
            "kyiv_pochaiana": NeighborhoodPreset(
                name="Почайна", patterns=(r"\bпочайн(а|и|і|у|ою|ої)\b",)
            ),
            "kyiv_podil": NeighborhoodPreset(
                name="Поділ",
                patterns=(
                    r"\bпод(іл|олу|олі|олом)\b",
                    r"\bподільськ(ий|ого|ому|им)\b",
                ),
            ),
            "kyiv_pozniaky": NeighborhoodPreset(
                name="Позняки",
                patterns=(r"\bпозняк(и|ів|ах|ами)\b",),
            ),
            "kyiv_priorka": NeighborhoodPreset(
                name="Пріорка", patterns=(r"\bпріорк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_pushcha_vodytsia": NeighborhoodPreset(
                name="Пуща-Водиця",
                # TODO: пуща  # noqa: TD002
                patterns=(r"\bпущ(а|і|у|ею)[ -]водиц(я|і|ю|ею)\b",),
            ),
            "kyiv_rembaza": NeighborhoodPreset(
                name="Рембаза", patterns=(r"\bрембаз(а|и|і|у|ою)\b",)
            ),
            "kyiv_right_bank": NeighborhoodPreset(
                name="Правий берег",
                patterns=(
                    r"\bправ(ий|ого|ому|им) берег(а|у|ом|і)?\b",
                    r"\bправобережж(я|і|ю|ям)\b",
                ),
            ),
            "kyiv_rusanivka": NeighborhoodPreset(
                name="Русанівка", patterns=(r"\bрусанів(ка|ки|ці|ку|кою)\b",)
            ),
            "kyiv_rusanivski_sady": NeighborhoodPreset(
                name="Русанівські Сади",
                patterns=(r"\bрусанівськ(і|их|им|ими) сад(и|ів|ах|ами)\b",),
            ),
            "kyiv_shuliavka": NeighborhoodPreset(
                name="Шулявка", patterns=(r"\bшулявк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_solomianka": NeighborhoodPreset(
                name="Солом'янка",
                patterns=(
                    r"\bсолом(а|['’ʼ]?янк(а|и|у|ою|ці))\b",
                    r"\bсолом['’ʼ]?янськ(ий|ого|ому|им)\b",
                ),
            ),
            "kyiv_sviatoshyn": NeighborhoodPreset(
                name="Святошин",
                patterns=(
                    r"\bсвятошин(о|а|і)?\b",
                    r"\bсвятошинськ(ий|ого|ому|им)\b",
                ),
            ),
            "kyiv_syrets": NeighborhoodPreset(
                name="Сирець", patterns=(r"\bсир(ець|ця|ці|цем)\b",)
            ),
            "kyiv_telychka": NeighborhoodPreset(
                name="Теличка", patterns=(r"\bтеличк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_teremky": NeighborhoodPreset(
                name="Теремки", patterns=(r"\bтеремк(и|ів|ах|ами)\b",)
            ),
            "kyiv_troieshchyna": NeighborhoodPreset(
                name="Троєщина",
                patterns=(
                    r"\bтроєщин(а|и|і|у|ою)\b",
                    r"\bтро(я|ї|ю)\b",
                ),
            ),
            "kyiv_vidradnyi": NeighborhoodPreset(
                name="Відрадний", patterns=(r"\bвідра(д|нд)н(ий|ого|ому|им)\b",)
            ),
            "kyiv_vita_lytovska": NeighborhoodPreset(
                name="Віта-Литовська",
                patterns=(r"\bвіта[ -]литовськ(а|ої|ій|у|ою)\b",),
            ),
            "kyiv_voskresenka": NeighborhoodPreset(
                name="Воскресенка", patterns=(r"\bвос(к)?ресенк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_vydubychi": NeighborhoodPreset(
                name="Видубичі", patterns=(r"\bвидубич(і|ів|ах|ами)\b",)
            ),
            "kyiv_vynohradar": NeighborhoodPreset(
                name="Виноградар", patterns=(r"\bвиноградар(а|і|ем)?\b",)
            ),
            "kyiv_zhuliany": NeighborhoodPreset(
                name="Жуляни", patterns=(r"\bжулян(и|ах|ами)?\b",)
            ),
            "kyiv_zvirynets": NeighborhoodPreset(
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
        neighborhoods={
            "kyiv_oblast_boryspil": NeighborhoodPreset(
                name="Бориспіль",
                patterns=(
                    r"\bборисп(іль|оля|олю|олем|олі)\b",
                    r"\bборік\b",
                ),
            ),
            "kyiv_oblast_brovary": NeighborhoodPreset(
                name="Бровари",
                patterns=(r"\bбровар(и|ів|ам|ами|ах)\b",),
            ),
            "kyiv_oblast_bucha": NeighborhoodPreset(
                name="Буча", patterns=(r"\bбуч(а|і|у|ею)\b",)
            ),
            "kyiv_oblast_chaiky": NeighborhoodPreset(
                name="Чайки", patterns=(r"\bчайк(и|ів|ам|ами|ах)\b",)
            ),
            "kyiv_oblast_dymer": NeighborhoodPreset(
                name="Димер", patterns=(r"\bдимер(а|у|ом|і)?\b",)
            ),
            "kyiv_oblast_hnidyn": NeighborhoodPreset(
                name="Гнідин", patterns=(r"\bгнідин(а|у|ом|і)?\b",)
            ),
            "kyiv_oblast_hostomel": NeighborhoodPreset(
                name="Гостомель", patterns=(r"\bгостомел(ь|я|ю|ем|і)\b",)
            ),
            "kyiv_oblast_hotianivka": NeighborhoodPreset(
                name="Хотянівка", patterns=(r"\bхотянівк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_oblast_irpin": NeighborhoodPreset(
                name="Ірпінь", patterns=(r"\bірп(інь|еня|еню|енем|ені)\b",)
            ),
            "kyiv_oblast_kotsiubynske": NeighborhoodPreset(
                name="Коцюбинське", patterns=(r"\bкоцюбинськ(е|ого|ому|им|ім)\b",)
            ),
            "kyiv_oblast_kozyn": NeighborhoodPreset(
                name="Козин", patterns=(r"\bкозин(а|у|ом|і)?\b",)
            ),
            "kyiv_oblast_obukhiv": NeighborhoodPreset(
                name="Обухів", patterns=(r"\bобух(ів|ова|ову|овом|ові)\b",)
            ),
            "kyiv_oblast_petrivtsi": NeighborhoodPreset(
                name="Петрівці", patterns=(r"\bпетрівц(і|ів|ям|ями|ях)\b",)
            ),
            "kyiv_oblast_petropavlivska_borshchahivka": NeighborhoodPreset(
                name="Петропавлівська Борщагівка",
                patterns=(
                    r"\bпетропавлівськ(а|ої|ій|у|ою) борщагівк(а|и|і|у|ою|ці)\b",
                ),
            ),
            "kyiv_oblast_pohreby": NeighborhoodPreset(
                name="Погреби", patterns=(r"\bпогреб(и|ів|ам|ами|ах)\b",)
            ),
            "kyiv_oblast_prolisky": NeighborhoodPreset(
                name="Проліски", patterns=(r"\bпроліс(ки|ків|кам|ками|ках)\b",)
            ),
            "kyiv_oblast_sofiivska_borshchahivka": NeighborhoodPreset(
                name="Софіївська Борщагівка",
                patterns=(r"\bсофіївськ(а|ої|ій|у|ою) борщагівк(а|и|і|у|ою|ці)\b",),
            ),
            "kyiv_oblast_ukrainka": NeighborhoodPreset(
                name="Українка", patterns=(r"\bукраїнк(а|и|у|ою|ці)\b",)
            ),
            "kyiv_oblast_vasylkiv": NeighborhoodPreset(
                name="Васильків", patterns=(r"\bвасильков(а|у|ом|і)?\b",)
            ),
            "kyiv_oblast_vorzel": NeighborhoodPreset(
                name="Ворзель", patterns=(r"\bворзел(ь|я|ю|ем|і)\b",)
            ),
            "kyiv_oblast_vyshhorod": NeighborhoodPreset(
                name="Вишгород", patterns=(r"\bвишгород(у|і|ом|а)?\b",)
            ),
            "kyiv_oblast_vyshneve": NeighborhoodPreset(
                name="Вишневе", patterns=(r"\bвишнев(е|ого|ому|им|ім)\b",)
            ),
            "kyiv_oblast_zazyma": NeighborhoodPreset(
                name="Зазим'я", patterns=(r"\bзазим['’ʼ]?(я|ї|ям)\b",)
            ),
            "kyiv_oblast_zhk_sofiia": NeighborhoodPreset(
                name="ЖК Софія", patterns=(r"\bжк[. ]+[«\"]?софі(я|ї|ю|єю)\b",)
            ),
        },
    ),
}
