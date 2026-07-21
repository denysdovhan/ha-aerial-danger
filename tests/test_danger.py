"""Tests for the aerial danger detection library."""

# ruff: noqa: S101

import re

import pytest

from custom_components.aerial_danger.danger import (
    DangerDetector,
    DangerType,
    PatternMatch,
)
from custom_components.aerial_danger.danger.keywords import DRONE_DANGER, IRBM_DANGER

REGION_PATTERNS = [
    r"\bки(ї|є)в(а|у|ом|е|і)?\b",
    r"\bкиївщин(а|и|і|у|ою)?\b",
    r"\bстолиц(і|ю|я)?\b",
    r"(до|на) нас",
    r"наш(у|ої) област(ьі|і)?",
]

NEIGHBORHOOD_PATTERNS = [
    r"\bнив(ки|ками|ок)\b",
    r"\bсвятошин(а|у|ом|і|о)?\b",
    r"\bсвятошин(ський|ського)?\b",
    r"\bантонов",
    r"\bакадем",
    r"берковець",
    r"cирець",
    r"cирця",
    r"\bшулявк(а|и)\b",
    r"галаган",
]

ZIRCON_CASES: list[str] = [
    "🔴Пуск ракети «Циркон»!",
    "🔴 Пуск ракети «Циркон»!",
    "🔴Пуск Циркону!",
    "🔴 Пуск Циркону!",
    "ЦИРКОН",
    "ЦИРКОН Є",
    "ЩЕ ЦИРКОН",
    "І ЩЕ ЦИРКОН",
    "2 ЦИРКОНИ!",
    "Вихід Циркона Курщина!",
    "Циркон з Криму! У наш бік!",
    "Циркон з Курщини! У наш бік!",
    "🔴Циркон з Криму.",
    "🔴 Циркон з Криму.",
    "Циркони заходять в область!",
    "🔴Циркон Київ!",
    "❗️ 1х Циркон на Київ з Курська",
    "❗️ 2х Циркони у напрямку Києва",
    "Загальна ситуація:\nКР Циркон у напрямку Києва.",
    "❗️ Київ 1х Циркон на місто",
    "Циркони над Києвом!!",
    "🚀 Вихід Циркону у бік Києва!",
    "❗️З Курська тоже Циркони до нас!",
    "🚀 Також є циркон. Сумарно до 4 ракет на Київ!",
    "2-3 Циркона на Київ.",
    "Циркони з Криму на Київ!",
    "Циркони з Курщини на Київ!",
    "Бляяяя, Циркон на Київ!!!",
    "❗️ 1х Циркон повз Ніжин на Київ",
    "❗️ Вихід йм. КР Циркон у напрямку Київщини.",
    "Циркон з півдня попередньо.",
    "Циркон з півночі попередньо.",
    "Ще з Курська Циркон!",
    "Ще з Курщини на Циркон!",
]

TARGETED_ZIRCON_CASES: list[tuple[str, str]] = [
    (r"\bхерсон(а|у|ом|і)?\b", "Циркон над Херсоном попередньо!"),
    (r"\bтроя\b", "Троя, два Циркона!"),
    (r"\bбц\b", "БЦ увага по Цирконам."),
    (r"\bбровари\b", "БРОВАРИ ЦИРКОН!"),
    (r"\bбровари\b", "Бровари увага Циркон."),
    (r"\bсумщин(а|і|у|ою)?\b", "Циркон на Сумщині!"),
]

BALLISTIC_CASES: list[str] = [
    "Київ швидкісна!",
    "КИЇВ Є ЦІЛІ!",
    "Київ спуск! Одна за другою!",
    "❗️ Балістика у напрямку Києва",
    "❗️Повторний вихід з Брянська у напрямку Києва",
    "КИЇВ ЦІЛЬ!",
    "🔴🚀 «Кинджал» Київ!",
    "☄Київ Балістика!",
    "КИЇВ ШВИДКІСНА",
    "🚀Швидкісна ціль на Київ!",
    "Ще балістика на Київ!",
    "‼️ Київ — спуск балістики!",
    "🚀 Київ! Балістика!",
    "🚀 Київ! Ще балістика!",
    "🚀 Київ, балістика!",
    "❗️ Кинджал вектор Київ/агломерація",
    "🚀 Київ! Кинджал!",
    "Київ є ЦІЛЬ!",
    "КИЇВ КИНДЖАЛ",
    "🚀 Швидкісна у бік Києва!",
    "‼️Київ — спуск Кинджалу!",
    "Кинджал у бік Києва/Житомира.",
]

IRBM_CASES: list[tuple[str, str]] = [
    (
        IRBM_DANGER[0],
        "‼️Увага! Загроза застосування балістики середньої дальності (БРСД) "
        "по всій території України.\nІмовірний пуск ракети Кедр/Орєшнік "
        "(п/п РС-26).",
    ),
    (
        IRBM_DANGER[0],
        "‼️ Загроза застосування балістики середньої дальності (БРСД) "
        "по всій території України.",
    ),
    (IRBM_DANGER[0], "Загроза БРСД."),
    (IRBM_DANGER[0], "Повторна загроза БРСД."),
    (
        IRBM_DANGER[0],
        "🚨Загроза застосування балістичної ракети середньої дальності (Орєшнік).",
    ),
    (
        IRBM_DANGER[0],
        "❗️Загроза застосування БРСД «Орєшнік» по території України.",
    ),
    (
        IRBM_DANGER[1],
        "пуск Орєшніка",
    ),
    (
        IRBM_DANGER[2],
        "🚀 Є інформація про пуск Орешніка! Протягом 10 хвилин уважно.",
    ),
    (
        IRBM_DANGER[3],
        "🚀 Була інформація про пуск Орєшніка!",
    ),
    (
        IRBM_DANGER[4],
        "❗️Загроза пусків Орєшніка!",
    ),
    (
        IRBM_DANGER[4],
        "🔴❗️Загроза застосування «Орєшніка»!",
    ),
    (
        IRBM_DANGER[4],
        "❗️Загроза нанесення Орешніка!",
    ),
    (
        IRBM_DANGER[4],
        "Upd. Загроза пуски Орєшніка!",
    ),
    (
        IRBM_DANGER[4],
        "загроза орєшніка",
    ),
    (
        IRBM_DANGER[5],
        "тривога по Орєшніку!",
    ),
    (
        IRBM_DANGER[6],
        "🔴По Орєшніку загроза актуальна!",
    ),
    (
        IRBM_DANGER[7],
        "Увага поширення тривоги по всій країні на імовірну активність БРСД "
        "з полігону КапЯр!",
    ),
    (
        IRBM_DANGER[8],
        "❗️Додалась загроза застосування балістики з Капустиного Яру (орєшнік).",
    ),
    (
        IRBM_DANGER[9],
        "❗️ Загроза застосування міжконтинентальних балістичних ракет РС-26 «Рубіж».",
    ),
]

IRBM_POTENTIAL_CASES: list[str] = [
    "Імовірний пуск ракети Кедр/Орєшнік (п/п РС-26).",
    "Попередньо, превентивна загроза БРСД по всій країні!",
    "Попередьно, загроза БРСД.",
    "❗️Також отримали попередження стосовно загрози застосування БРСД "
    "впродовж декількох годин.",
    "попередньо, пуск орєшніка",
    "Можливі тривоги по причині загрози міжконтинентальної балістичної "
    'ракети "Рубіж" (Орешник).',
    "За інформацією, на полігоні «Капустин Яр» відбуваються підготовчі "
    "дії до запуску міжконтинентальної балістичної ракети «Орєшнік».",
    "За інформацією, противник готовий протягом двох годин здійснити "
    "пуск до 2-х ракет «Орєшнік».",
    "рф готує новий запуск БРСД “Орєшнік” з полігону Капустин Яр по "
    "Україні найближчим часом.",
    "Окремо діє попередження про ймовірне застосування БРСД "
    "«Кедр/Орєшнік» по території України.",
    "По всій країні тривогу оголошено превентивно, оскільки надійшла "
    "інформація про можливий пуск БСД «Орєшнік» з полігону «Капустин Яр».",
    "🟡Підвищена загроза застосування балістичної ракети середньої "
    "дальності «Орєшнік» по території України!",
    "Повітряні Сили ЗС України офіційно повідомили про загрозу "
    "застосування БРСД «Орєшнік» по території України протягом доби.",
    "❗️Загроза пусків БРСД «Орєшнік» із полігону «Капустин Яр» зберігається до 19.02.",
]

IRBM_AFTERMATH_CASES: list[str] = [
    "Момент удару «Орєшніком» по Львівщині.",
    "СБУ показала уламки балістичної ракети середньої дальності «Кедр», "
    "якою вчора атакували Львівщину.",
    "Відбій загрози БРСД по території України.",
    "Станом на зараз не володіємо інформацією про загрозу застосування "
    "балістики середньої дальності Кедр (Орєшнік).",
    "З’являються деталі щодо застосування другої балістичної ракети "
    "середньої дальності «Кєдр/Орєшнік» під час минулої атаки.",
    "У ніч на 24 травня ворог застосував 0/1 БРСД «Кєдр/Орєшнік».",
]

CRUISE_CASES: list[str] = [
    "🔴Ракета Київ!",
    "КР Позняки\n КР Теремки\n КР Солом'янка\n КР Нивки",
    "Київ увага КР!!",
    "❗ Київ — група КР на місто",
    "❗️🚀КИЇВ 3-4 ХВЛИНИ ДО КР!",
    "Київ і агломерація бути в укриттях по КР",
    "🚀 Васильків/Київ, йде з півдня!",
    "Київ увага по КР",
    "Київ ще групи КР!",
    "‼️ Київ — наближення крилатих ракет",
    "Київ увага — КР",
    "До 4 КР на Київ/Бориспіль.",
    "🟡🚀Калібри з Житомирщини розвертаються на Київщину, вектор Київ!",
    "🚀 Калібри на Київ!",
    "🚀КР на Київ!",
    "🟡🚀Калібри на Святошинський район!",
    "КАЛІБР КИЇВ!",
    "🔴🚀4х групи крилатих ракет підлітають до Києва!",
    "🟡🚀Ракета на Київ, вектор Академмістечко!",
    "🚀 Група крилатих ракет на Чернігівщині. Курс до нас.",
    "🚀 Крилаті з Житомирщини курсом до нас.",
    "❗️Короче, до 10 штук. Крилаті курсом на нашу область.",
]

DRONE_CASES: list[tuple[str, str]] = [
    (DRONE_DANGER[10], "🛵 У бік Нивок."),
    (DRONE_DANGER[10], "🛵 Нивки, може бути гучно!"),
    (DRONE_DANGER[10], "🛵 Курс на Нивки/Святошино."),
    (DRONE_DANGER[10], "Святошино/Нивки 🛵"),
    (DRONE_DANGER[13], "Нивки над вами БПЛА!"),
    (DRONE_DANGER[18], "❗️ Київ — 1х Академ/Коцюбинське."),
    (
        DRONE_DANGER[18],
        "Київ:\n 1х Нивки/Сирець\n 2х Жуляни\n \n 1х ДВРЗ/Березняки",
    ),
    (DRONE_DANGER[18], "❗️ Київ — 1х Нивки Сирець"),
    (DRONE_DANGER[19], "Київ: \n 2х Куренівка Нивки \n 1х Бортничі"),
    (DRONE_DANGER[19], "❗️ Київ — 1х на Святошин."),
    (DRONE_DANGER[23], "Антонов йде!"),
]

REACTIVE_DRONE_CASES: list[tuple[str, str, str]] = [
    (
        r"\bтроєщин(а|и|і|у|ою)?\b",
        DRONE_DANGER[0],
        "Реактивний Шахед наближається до Києва, вектор Троєщина.",
    ),
    (
        r"\bзаток(а|и|у|ою)?\b",
        DRONE_DANGER[1],
        "❗️ Реактивна ціль у напрямку Затока, Одещина.",
    ),
    (
        r"\bнив(ки|ками|ок)\b",
        DRONE_DANGER[2],
        "🛵 Реактивні БпЛА на Нивки",
    ),
    (
        r"\bдніпропетровщин(а|и|і|у|ою)?\b",
        DRONE_DANGER[2],
        "🛵 Реактивний БпЛА на Дніпропетровщині, курс на північ Кривого Рогу.",
    ),
    (
        r"\bдимер(а|у|ом|і)?\b",
        DRONE_DANGER[2],
        "Київщина:\n1х реактивний БпЛА повз Димер у Вишгородському районі.",
    ),
    (
        r"\bбровар(и|ів|ах)?\b",
        DRONE_DANGER[2],
        "🛵 Реактивний БпЛА курсом на Бровари!",
    ),
    (
        r"\bодеськ(ий|ого|ому) район\b",
        DRONE_DANGER[3],
        "Пара реактивних клоунів в морі курсом на Одеський район.",
    ),
    (
        r"\bбровар(и|ів|ах)?\b",
        DRONE_DANGER[4],
        "Реактивний дрон повз Бровари.",
    ),
    (
        r"\bтро(я|ю)\b",
        DRONE_DANGER[4],
        "1 реактивний дрон летить на Трою.",
    ),
    (
        r"\bоболон(ь|і|ню)\b",
        DRONE_DANGER[4],
        "Реактивний дрон на Оболонь.",
    ),
    (
        r"\bсолом(а|ою|и)?\b",
        DRONE_DANGER[5],
        "Реактивний над Соломою🛵",
    ),
    (
        r"\bвишгород",
        DRONE_DANGER[5],
        "Реактивний на Вишгород",
    ),
    (
        r"\bславутич",
        DRONE_DANGER[5],
        "Реактивний повз Славутич на море",
    ),
    (
        r"\bяготин(а|у|ом|і)?\b",
        DRONE_DANGER[6],
        "Реактивний в бік Яготина з Полтавщини",
    ),
    (
        r"\bбровар(и|ів|ах)?\b",
        DRONE_DANGER[6],
        "🛵Новий реактивний у бік Броварів та Борисполя!",
    ),
    (
        r"\bодес(а|и|у|ою)?\b",
        DRONE_DANGER[7],
        "Одеса наступний реактивний 5хв.",
    ),
    (
        r"\bславутич",
        DRONE_DANGER[7],
        "Славутич реактивний 5500 висота",
    ),
    (
        r"\bлів(ий|ого|ому) берег\b",
        DRONE_DANGER[7],
        "Лівий берег - реактивний йде!",
    ),
    (
        r"\bтро(я|ю)\b",
        DRONE_DANGER[7],
        "🛵 Троя, реактивний",
    ),
    (
        r"\bніжин(а|у|ом|і)?\b",
        DRONE_DANGER[8],
        "2 реактивних на Ніжин йде",
    ),
    (
        r"\bтроєщин(а|и|і|у|ою)?\b",
        DRONE_DANGER[8],
        "4 реактивних на Київ, перший на Троєщину/Оболонь.",
    ),
    (
        r"\bвідрадн(ий|ого|ому|им)?\b",
        DRONE_DANGER[9],
        "❗️ Київ 1х реактив, Відрадний Святошин",
    ),
    (
        r"\bкам[’']янськ(ий|ого|ому)?\b",
        DRONE_DANGER[9],
        "❗️ 1х реактив у Кам'янському районі Дніпропетровської області.",
    ),
]

REACTIVE_DRONE_AFTERMATH_CASES: list[tuple[str, str]] = [
    (
        r"\bдарницьк(ий|ого|ому)?\b",
        "Під час минулої повітряної атаки ворог застосував реактивний дрон "
        "типу “Герань-3”. Характерний звук було чутно в Дарницькому районі.",
    ),
    (
        r"\bнив(ки|ками|ок)\b",
        "Під час минулої атаки реактивний дрон було збито над Нивками.",
    ),
]

GENERIC_CASES: list[str] = [
    "🔴🚀Нивки.",
    "🔴❗️Вектор Київ!",
    "🔴❗️Київ!",
    "🔴🚀 Київ!!",
    "❗️Київ!",
    "🟡Київ!",
    "🚀Нивки!",
    "🔴🚀Святошино!",
    "🔴🚀Святошин!",
    "Далі Нивки.",
    "❗️На Нивки!",
    "БОЯРКА - ВИШНЕВЕ - КИЇВ!!",
    "КИЇВ!",
    "КИЇВ 2 СТІНИ!",
    "Київ зреагувати!!",
    "‼️Київ!",
    "Київ жахне!!",
    "Нивки увага!",
    "Київ/Вишгород увага",
    "🔴🚀 Вектор руху на Київ!",
    "🚀 Вектор на столицю!",
]

MATCH_CASES: list[tuple[DangerType, str]] = [
    *[(DangerType.IRBM, text) for _, text in IRBM_CASES],
    *[(DangerType.BALLISTIC, s) for s in BALLISTIC_CASES],
    *[(DangerType.CRUISE, s) for s in CRUISE_CASES],
    *[(DangerType.DRONE, text) for _, text in DRONE_CASES],
    *[(DangerType.GENERIC, s) for s in GENERIC_CASES],
]


NO_MATCH_CASES: list[str] = [
    "🛵Шахед на Мену.",
    "🛵7 Шахедів з моря на Татарбунари.",
    "🛵Залишився 1 Шахед на півночі Київщині, летить в напрямку Чорнобиля!",
    "🔴🚀Вишгород та Бровари!",
    "🚀Візуалізації напрямку польоту крилатої ракети.",
    "🟡 Дорозвідка по Кинджалах, локаційно чисто.",
    "🔴🚛 Загроза балістики з Воронезької області!",
    "🟡🛵 Шахеди над Києвом, вектор Теремки, Виноградар та Чоколівка!",
    "БпЛА невстановленого типу над Обухівським р-ном Київщини.",
    "💥Удар балістикою по Дніпру.",
    "⚠️ 2х БпЛА сектор Павлоград, дніпропетровської області.",
    "‼️Одеса — спуск балістики!",
    "⚠️ 5х БпЛА на північ від Києва. \n 6х БпЛА у напрямку Вишневе/Білогородка",
    "По Києву били Іскандер-М та Циркони.",
    "Під час нічної атаки по Києву росія випустила дві ракети «Циркон»/«Онікс».",
    "На жаль, цієї ночі над Києвом не вдалося збити жодної ракети «Циркон».",
    "Удар Цирконами по Києву відбувся вночі.",
    "Вночі було зафіксовано пуск ракети «Циркон» по Києву.",
    "Циркон над Херсоном попередньо!",
    "Троя, два Циркона!",
    "БЦ увага по Цирконам.",
    "БРОВАРИ ЦИРКОН!",
]


def test_validate_patterns() -> None:
    """Configured patterns compile independently from the detector."""
    DangerDetector.validate_patterns(REGION_PATTERNS, NEIGHBORHOOD_PATTERNS)

    with pytest.raises(re.error):
        DangerDetector.validate_patterns(["("])


def test_ballistic_only() -> None:
    """Ballistic-specific helper should flag ballistic samples."""
    detector = DangerDetector(REGION_PATTERNS, NEIGHBORHOOD_PATTERNS)
    for text in BALLISTIC_CASES:
        detection = detector.ballistic_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.BALLISTIC, text


def test_irbm_is_nationwide() -> None:
    """IRBM alerts should not require configured area patterns."""
    detector = DangerDetector([], [])
    for danger_pattern, text in IRBM_CASES:
        detection = detector.irbm_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.IRBM, text
        assert detection.matched_area is None, text
        assert detection.area_pattern is None, text
        assert detection.danger_pattern == danger_pattern, text
        assert detector.danger(text).type == DangerType.IRBM, text


def test_irbm_aftermath_does_not_match() -> None:
    """IRBM aftermath and all-clear posts should not raise danger flags."""
    detector = DangerDetector([], [])
    for text in IRBM_AFTERMATH_CASES:
        detection = detector.danger(text)
        assert detection.danger is False, text
        assert detection.type is None, text


def test_irbm_potential_danger_does_not_match() -> None:
    """IRBM forecasts and preparations should not raise danger flags."""
    detector = DangerDetector([], [])
    for text in IRBM_POTENTIAL_CASES:
        detection = detector.danger(text)
        assert detection.danger is False, text
        assert detection.type is None, text


def test_zircon_is_ballistic_and_cruise() -> None:
    """Shared Zircon keywords should match ballistic and cruise detection."""
    detector = DangerDetector([r".*"], [])
    for text in ZIRCON_CASES:
        ballistic = detector.ballistic_danger(text)
        cruise = detector.cruise_missile_danger(text)
        assert ballistic.danger is True, text
        assert ballistic.type == DangerType.BALLISTIC, text
        assert cruise.danger is True, text
        assert cruise.type == DangerType.CRUISE, text
        assert detector.danger(text).type == DangerType.BALLISTIC, text


def test_targeted_zircon_uses_configured_area() -> None:
    """Targeted Zircon alerts should require their configured area."""
    for area, text in TARGETED_ZIRCON_CASES:
        detector = DangerDetector([area], [])
        ballistic = detector.ballistic_danger(text)
        cruise = detector.cruise_missile_danger(text)
        assert ballistic.danger is True, text
        assert ballistic.type == DangerType.BALLISTIC, text
        assert cruise.danger is True, text
        assert cruise.type == DangerType.CRUISE, text


def test_cruise_only() -> None:
    """Cruise-specific helper should flag cruise samples."""
    detector = DangerDetector(REGION_PATTERNS, NEIGHBORHOOD_PATTERNS)
    for text in CRUISE_CASES:
        detection = detector.cruise_missile_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.CRUISE, text


def test_drone_only() -> None:
    """Drone-specific helper should flag drone samples."""
    detector = DangerDetector(REGION_PATTERNS, NEIGHBORHOOD_PATTERNS)
    for danger_template, text in DRONE_CASES:
        detection = detector.drone_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.DRONE, text
        assert detection.area_pattern is not None, text
        assert detection.danger_pattern == danger_template.replace(
            "{area}", detection.area_pattern
        ), text


def test_reactive_drone_danger() -> None:
    """Reactive-drone alerts should match their area-specific phrase."""
    for area_pattern, danger_template, text in REACTIVE_DRONE_CASES:
        detector = DangerDetector([], [area_pattern])

        detection = detector.danger(text)

        assert detection.danger is True, text
        assert detection.type == DangerType.DRONE, text
        assert detection.danger_pattern == danger_template.replace(
            "{area}", area_pattern
        ), text


def test_reactive_drone_aftermath_does_not_match() -> None:
    """Reactive-drone aftermath should not raise danger flags."""
    for area_pattern, text in REACTIVE_DRONE_AFTERMATH_CASES:
        detector = DangerDetector([], [area_pattern])

        detection = detector.danger(text)

        assert detection.danger is False, text
        assert detection.type is None, text


def test_generic_only() -> None:
    """Generic helper should flag generic samples."""
    detector = DangerDetector(REGION_PATTERNS, NEIGHBORHOOD_PATTERNS)
    for text in GENERIC_CASES:
        detection = detector.generic_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.GENERIC, text


def test_matches_expected_types() -> None:
    """All positive samples should be detected with the expected type."""
    detector = DangerDetector(REGION_PATTERNS, NEIGHBORHOOD_PATTERNS)
    for expected_type, text in MATCH_CASES:
        detection = detector.danger(text)
        assert detection.danger is True, text
        assert detection.type == expected_type, text


def test_detection_includes_exact_matches_and_patterns() -> None:
    """A detection should preserve exact text and matching regex patterns."""
    area_pattern = r"\bкиїв\b"
    detector = DangerDetector([area_pattern], [])

    detection = detector.danger("КИЇВ ШВИДКІСНА!")

    assert detection.matched_area == "КИЇВ"
    assert detection.matched_danger == "КИЇВ ШВИДКІСНА"
    assert detection.area_pattern == area_pattern
    assert detection.danger_pattern == rf"{area_pattern} швидкісна"


def test_match_helpers_return_pattern_matches() -> None:
    """Match helpers should return named text and pattern fields."""
    area_pattern = r"\bкиїв\b"
    danger_pattern = rf"{area_pattern} швидкісна"
    message = "КИЇВ ШВИДКІСНА!"
    detector = DangerDetector([area_pattern], [])

    assert detector.find_area(message, [area_pattern]) == PatternMatch(
        text="КИЇВ", pattern=area_pattern
    )
    assert detector.match_first(
        detector.compile_patterns([danger_pattern]), message
    ) == PatternMatch(text="КИЇВ ШВИДКІСНА", pattern=danger_pattern)


def test_non_matches() -> None:
    """Negative samples should not raise danger flags."""
    detector = DangerDetector(REGION_PATTERNS, NEIGHBORHOOD_PATTERNS)
    for text in NO_MATCH_CASES:
        detection = detector.danger(text)
        assert detection.danger is False, text
        assert detection.type is None, text
