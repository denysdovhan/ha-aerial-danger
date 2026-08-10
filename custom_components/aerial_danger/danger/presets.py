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
    "cherkasy_oblast": RegionPreset(
        name="Черкаська область",
        patterns=(
            r"\bчеркащин(а|и|і|у|ою)\b",
            r"\bчеркаськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "cherkasy_oblast_cherkasy": LocalityPreset(
                name="Черкаси", patterns=(r"\bчеркас(и|ам|ами|ах)?\b",)
            ),
        },
    ),
    "chernihiv_oblast": RegionPreset(
        name="Чернігівська область",
        patterns=(
            r"\bчернігівщин(а|и|і|у|ою)\b",
            r"\bчернігівськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "chernihiv_oblast_chernihiv": LocalityPreset(
                name="Чернігів", patterns=(r"\bчерніг(ів|ова|ову|овом|ові)\b",)
            ),
        },
    ),
    "chernivtsi_oblast": RegionPreset(
        name="Чернівецька область",
        patterns=(
            r"\bбуковин(а|и|і|у|ою)\b",
            r"\bчернівеччин(а|и|і|у|ою)\b",
            r"\bчернівецьк(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "chernivtsi_oblast_chernivtsi": LocalityPreset(
                name="Чернівці", patterns=(r"\bчернівц(і|ів|ям|ями|ях)\b",)
            ),
        },
    ),
    "dnipropetrovsk_oblast": RegionPreset(
        name="Дніпропетровська область",
        patterns=(
            r"\bдніпропетровщин(а|и|і|у|ою)\b",
            r"\bдніпропетровськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "dnipropetrovsk_oblast_dnipro": LocalityPreset(
                name="Дніпро", patterns=(r"\bдніпр(о|а|у|і|ом)\b",)
            ),
            "dnipropetrovsk_oblast_kamianske": LocalityPreset(
                name="Камʼянське",
                patterns=(r"\bкам['’ʼ]?янськ(е|ого|ому|им|ім)\b",),
            ),
            "dnipropetrovsk_oblast_kryvyi_rih": LocalityPreset(
                name="Кривий Ріг",
                patterns=(r"\bкрив(ий|ого|ому|им) р(іг|огу|озі|огом)\b",),
            ),
            "dnipropetrovsk_oblast_pavlohrad": LocalityPreset(
                name="Павлоград", patterns=(r"\bпавлоград(а|у|і|ом)?\b",)
            ),
        },
    ),
    "donetsk_oblast": RegionPreset(
        name="Донецька область",
        patterns=(
            r"\bдонеччин(а|и|і|у|ою)\b",
            r"\bдонецьк(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "donetsk_oblast_donetsk": LocalityPreset(
                name="Донецьк",
                patterns=(r"\bдонецьк(у|ом|і)?\b",),
            ),
        },
    ),
    "ivano_frankivsk_oblast": RegionPreset(
        name="Івано-Франківська область",
        patterns=(
            r"\bфранківщин(а|и|і|у|ою)\b",
            r"\bівано-франківщин(а|и|і|у|ою)\b",
            r"\bівано-франківськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "ivano_frankivsk_oblast_ivano_frankivsk": LocalityPreset(
                name="Івано-Франківськ",
                patterns=(r"\bівано-франківськ(у|ом|і)?\b",),
            ),
        },
    ),
    "kharkiv_oblast": RegionPreset(
        name="Харківська область",
        patterns=(
            r"\bхарківщин(а|и|і|у|ою)\b",
            r"\bхарківськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "kharkiv_oblast_balakliia": LocalityPreset(
                name="Балаклія", patterns=(r"\bбалаклі(я|ї|ю|єю)\b",)
            ),
            "kharkiv_oblast_bohodukhiv": LocalityPreset(
                name="Богодухів", patterns=(r"\bбогодух(ів|ова|ову|овом|ові)\b",)
            ),
            "kharkiv_oblast_derzhprom": LocalityPreset(
                name="Держпром", patterns=(r"\bдержпром(у|і|ом|а)?\b",)
            ),
            "kharkiv_oblast_kharkiv": LocalityPreset(
                name="Харків", patterns=(r"\bхарк(ів|ова|ову|овом|ові)\b",)
            ),
            "kharkiv_oblast_khtz": LocalityPreset(name="ХТЗ", patterns=(r"\bхтз\b",)),
            "kharkiv_oblast_kozacha_lopan": LocalityPreset(
                name="Козача Лопань",
                patterns=(r"\bкозач(а|у|ою) лопан(ь|і|ню|ью)\b",),
            ),
            "kharkiv_oblast_kulynychi": LocalityPreset(
                name="Кулиничі", patterns=(r"\bкулинич(і|ів|ам|ами|ах)\b",)
            ),
            "kharkiv_oblast_kupiansk": LocalityPreset(
                name="Купʼянськ",
                patterns=(r"\bкуп['’ʼ]?янськ(а|у|ом|і)?\b",),
            ),
            "kharkiv_oblast_piatykhatky": LocalityPreset(
                name="Пʼятихатки",
                patterns=(r"\bп['’ʼ]?ятихатк(и|ах|ам|ами)\b",),
            ),
            "kharkiv_oblast_saltivka": LocalityPreset(
                name="Салтівка",
                patterns=(r"\bсалтівк(а|и|і|у|ою|о)\b",),
            ),
        },
    ),
    "kherson_oblast": RegionPreset(
        name="Херсонська область",
        patterns=(
            r"\bхерсонщин(а|и|і|у|ою)\b",
            r"\bхерсонськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "kherson_oblast_kherson": LocalityPreset(
                name="Херсон", patterns=(r"\bхерсон(а|у|ом|і)?\b",)
            ),
        },
    ),
    "khmelnytskyi_oblast": RegionPreset(
        name="Хмельницька область",
        patterns=(
            r"\bхмельниччин(а|и|і|у|ою)\b",
            r"\bхмельницьк(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "khmelnytskyi_oblast_khmelnytskyi": LocalityPreset(
                name="Хмельницький",
                patterns=(r"\bхмельницьк(ий|ого|ому|им|ім)\b",),
            ),
        },
    ),
    "kirovohrad_oblast": RegionPreset(
        name="Кіровоградська область",
        patterns=(
            r"\bкіровоградщин(а|и|і|у|ою)\b",
            r"\bкіровоградськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "kirovohrad_oblast_kropyvnytskyi": LocalityPreset(
                name="Кропивницький",
                patterns=(r"\bкропивницьк(ий|ого|ому|им|ім)\b",),
            ),
        },
    ),
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
            "kyiv_oblast_bila_tserkva": LocalityPreset(
                name="Біла Церква",
                patterns=(
                    r"\bбіл(а|ої|ій|у|ою) церкв(а|и|і|у|ою)\b",
                    r"\bбц\b",
                ),
            ),
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
    "luhansk_oblast": RegionPreset(
        name="Луганська область",
        patterns=(
            r"\bлуганщин(а|и|і|у|ою)\b",
            r"\bлуганськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "luhansk_oblast_luhansk": LocalityPreset(
                name="Луганськ",
                patterns=(r"\bлуганськ(у|ом|і)?\b",),
            ),
        },
    ),
    "lviv_oblast": RegionPreset(
        name="Львівська область",
        patterns=(
            r"\bльвівщин(а|и|і|у|ою)\b",
            r"\bльвівськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "lviv_oblast_lviv": LocalityPreset(
                name="Львів", patterns=(r"\bльв(ів|ова|ову|овом|ові)\b",)
            ),
        },
    ),
    "mykolaiv_oblast": RegionPreset(
        name="Миколаївська область",
        patterns=(
            r"\bмиколаївщин(а|и|і|у|ою)\b",
            r"\bмиколаївськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "mykolaiv_oblast_mykolaiv": LocalityPreset(
                name="Миколаїв",
                patterns=(r"\bмикола(їв|єва|єві|єву|євом)\b",),
            ),
        },
    ),
    "odesa_oblast": RegionPreset(
        name="Одеська область",
        patterns=(
            r"\bодещин(а|и|і|у|ою)\b",
            r"\bодеськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "odesa_oblast_arkadiia": LocalityPreset(
                name="Аркадія", patterns=(r"\bаркаді(я|ї|ю|єю)\b",)
            ),
            "odesa_oblast_bilhorod_dnistrovskyi": LocalityPreset(
                name="Білгород-Дністровський",
                patterns=(r"\bбілгород[ -]дністровськ(ий|ого|ому|им|ім)\b",),
            ),
            "odesa_oblast_chornomorsk": LocalityPreset(
                name="Чорноморськ", patterns=(r"\bчорноморськ(а|у|ом|і)?\b",)
            ),
            "odesa_oblast_karolino_buhaz": LocalityPreset(
                name="Кароліно-Бугаз",
                patterns=(r"\bкароліно[ -]бугаз(у|і|ом|а)?\b",),
            ),
            "odesa_oblast_khadzhybeiskyi_raion": LocalityPreset(
                name="Хаджибейський район",
                patterns=(r"\bхаджибейськ(ий|ого|ому|им|ім) район(у|і|ом)?\b",),
            ),
            "odesa_oblast_odesa": LocalityPreset(
                name="Одеса", patterns=(r"\bодес(а|и|і|у|ою)\b",)
            ),
            "odesa_oblast_odesa_port": LocalityPreset(
                name="Одеський порт",
                patterns=(
                    r"\bодеськ(ий|ого|ому|им|ім) порт(у|і|ом|а)?\b",
                    r"\bодес(а|и|і|у|ою)\s*[ /-]\s*порт(у|і|ом|а)?\b",
                ),
            ),
            "odesa_oblast_ovidiopol": LocalityPreset(
                name="Овідіополь", patterns=(r"\bовідіопол(ь|я|і|ю|ем)\b",)
            ),
            "odesa_oblast_peresyp": LocalityPreset(
                name="Пересип", patterns=(r"\bпересип(у|ом|і)?\b",)
            ),
            "odesa_oblast_zatoka": LocalityPreset(
                name="Затока", patterns=(r"\bзаток(а|и|у|ою|ці)\b",)
            ),
        },
    ),
    "poltava_oblast": RegionPreset(
        name="Полтавська область",
        patterns=(
            r"\bполтавщин(а|и|і|у|ою)\b",
            r"\bполтавськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "poltava_oblast_poltava": LocalityPreset(
                name="Полтава", patterns=(r"\bполтав(а|и|і|у|ою)\b",)
            ),
        },
    ),
    "rivne_oblast": RegionPreset(
        name="Рівненська область",
        patterns=(
            r"\bрівненщин(а|и|і|у|ою)\b",
            r"\bрівненськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "rivne_oblast_rivne": LocalityPreset(
                name="Рівне", patterns=(r"\bрівне\b",)
            ),
        },
    ),
    "sumy_oblast": RegionPreset(
        name="Сумська область",
        patterns=(
            r"\bсумщин(а|и|і|у|ою)\b",
            r"\bсумськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "sumy_oblast_sumy": LocalityPreset(
                name="Суми", patterns=(r"\bсум(и|ах|ами)?\b",)
            ),
        },
    ),
    "ternopil_oblast": RegionPreset(
        name="Тернопільська область",
        patterns=(
            r"\bтернопільщин(а|и|і|у|ою)\b",
            r"\bтернопільськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "ternopil_oblast_ternopil": LocalityPreset(
                name="Тернопіль",
                patterns=(r"\bтерноп(іль|оля|олю|олем|олі)\b",),
            ),
        },
    ),
    "vinnytsia_oblast": RegionPreset(
        name="Вінницька область",
        patterns=(
            r"\bвінниччин(а|и|і|у|ою)\b",
            r"\bвінницьк(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "vinnytsia_oblast_vinnytsia": LocalityPreset(
                name="Вінниця", patterns=(r"\bвінниц(я|і|ю|ею)\b",)
            ),
        },
    ),
    "volyn_oblast": RegionPreset(
        name="Волинська область",
        patterns=(
            r"\bволин(ь|і|ню)\b",
            r"\bволинськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "volyn_oblast_lutsk": LocalityPreset(
                name="Луцьк", patterns=(r"\bлуцьк(а|у|ом|ові)?\b",)
            ),
        },
    ),
    "zakarpattia_oblast": RegionPreset(
        name="Закарпатська область",
        patterns=(r"\bзакарпатськ(а|ої|ій|у|ою) област(ь|і|ю)\b",),
        localities={
            "zakarpattia_oblast_uzhhorod": LocalityPreset(
                name="Ужгород", patterns=(r"\bужгород(а|у|ом|і)?\b",)
            ),
        },
    ),
    "zaporizhzhia_oblast": RegionPreset(
        name="Запорізька область",
        patterns=(r"\bзапорізьк(а|ої|ій|у|ою) област(ь|і|ю)\b",),
        localities={
            "zaporizhzhia_oblast_komyshuvakha": LocalityPreset(
                name="Комишуваха", patterns=(r"\bкомишувах(а|и|і|у|ою)\b",)
            ),
            "zaporizhzhia_oblast_orikhiv": LocalityPreset(
                name="Оріхів", patterns=(r"\bоріх(ів|ова|ову|ові|овом)\b",)
            ),
            "zaporizhzhia_oblast_vilniansk": LocalityPreset(
                name="Вільнянськ", patterns=(r"\bвільнянськ(а|у|і|ом)?\b",)
            ),
            "zaporizhzhia_oblast_zaporizhzhia": LocalityPreset(
                name="Запоріжжя",
                patterns=(
                    r"\bзапоріжж(я|і|ю|ям)\b",
                    r"\bзп\b",
                ),
            ),
        },
    ),
    "zhytomyr_oblast": RegionPreset(
        name="Житомирська область",
        patterns=(
            r"\bжитомирщин(а|и|і|у|ою)\b",
            r"\bжитомирськ(а|ої|ій|у|ою) област(ь|і|ю)\b",
        ),
        localities={
            "zhytomyr_oblast_zhytomyr": LocalityPreset(
                name="Житомир", patterns=(r"\bжитомир(а|у|ом|і)?\b",)
            ),
        },
    ),
}
