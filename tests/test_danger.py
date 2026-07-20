"""Tests for the aerial danger detection library."""

# ruff: noqa: S101

import re

import pytest

from custom_components.aerial_danger.danger import (
    DangerDetector,
    DangerType,
    PatternMatch,
)

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

DRONE_CASES: list[str] = [
    "❗️ Київ — 1х Академ/Коцюбинське.",
    "Київ:\n 1х Нивки/Сирець\n 2х Жуляни\n \n 1х ДВРЗ/Березняки",
    "🛵 У бік Нивок.",
    "Київ: \n 2х Куренівка Нивки \n 1х Бортничі",
    "❗️ Київ — 1х Нивки Сирець",
    "❗️ Київ — 1х на Святошин.",
    "🛵 Нивки, може бути гучно!",
    "Нивки над вами БПЛА!",
    "🛵 Курс на Нивки/Святошино.",
    "Антонов йде!",
    "Святошино/Нивки 🛵",
]

REACTIVE_DRONE_CASES: list[tuple[str, str, str]] = [
    (
        r"\bвідрадн(ий|ого|ому|им)?\b",
        r"\bреактив\b.{0,32}{area}",
        "❗️ Київ 1х реактив, Відрадний Святошин",
    ),
    (
        r"\bнив(ки|ками|ок)\b",
        r"\bреактивн(і бпла на|ий бпла (на|повз|курсом на)) {area}",
        "🛵 Реактивні БпЛА на Нивки",
    ),
    (
        r"\bсолом(а|ою|и)?\b",
        r"\bреактивний\b (на|над|повз) {area}",
        "Реактивний над Соломою🛵",
    ),
    (
        r"\bтроєщин(а|и|і|у|ою)?\b",
        r"\bреактивний шахед\b.{0,48}\bвектор {area}",
        "Реактивний Шахед наближається до Києва, вектор Троєщина.",
    ),
    (
        r"\bкам[’']янськ(ий|ого|ому)?\b",
        r"\bреактив\b.{0,32}{area}",
        "❗️ 1х реактив у Кам'янському районі Дніпропетровської області.",
    ),
    (
        r"\bзаток(а|и|у|ою)?\b",
        r"\bреактивна ціль\b у напрямку {area}",
        "❗️ Реактивна ціль у напрямку Затока, Одещина.",
    ),
    (
        r"\bодес(а|и|у|ою)?\b",
        r"{area}\W+(наступний реактивний\b|реактивний( йде\b| \d+\b|[!.]*$))",
        "Одеса наступний реактивний 5хв.",
    ),
    (
        r"\bдніпропетровщин(а|и|і|у|ою)?\b",
        r"\bреактивн(і бпла на|ий бпла (на|повз|курсом на)) {area}",
        "🛵 Реактивний БпЛА на Дніпропетровщині, курс на північ Кривого Рогу.",
    ),
    (
        r"\bдимер(а|у|ом|і)?\b",
        r"\bреактивн(і бпла на|ий бпла (на|повз|курсом на)) {area}",
        "Київщина:\n1х реактивний БпЛА повз Димер у Вишгородському районі.",
    ),
    (
        r"\bбровар(и|ів|ах)?\b",
        r"\bреактивн(і бпла на|ий бпла (на|повз|курсом на)) {area}",
        "🛵 Реактивний БпЛА курсом на Бровари!",
    ),
    (
        r"\bодеськ(ий|ого|ому) район\b",
        r"\bреактивних клоунів\b.{0,24}\bкурсом на {area}",
        "Пара реактивних клоунів в морі курсом на Одеський район.",
    ),
    (
        r"\bяготин(а|у|ом|і)?\b",
        r"\bреактивний\b (у|в) бік {area}",
        "Реактивний в бік Яготина з Полтавщини",
    ),
    (
        r"\bбровар(и|ів|ах)?\b",
        r"\bреактивний\b (у|в) бік {area}",
        "🛵Новий реактивний у бік Броварів та Борисполя!",
    ),
    (
        r"\bвишгород",
        r"\bреактивний\b (на|над|повз) {area}",
        "Реактивний на Вишгород",
    ),
    (
        r"\bславутич",
        r"\bреактивний\b (на|над|повз) {area}",
        "Реактивний повз Славутич на море",
    ),
    (
        r"\bславутич",
        r"{area}\W+(наступний реактивний\b|реактивний( йде\b| \d+\b|[!.]*$))",
        "Славутич реактивний 5500 висота",
    ),
    (
        r"\bбровар(и|ів|ах)?\b",
        r"\bреактивний дрон\b (на|повз|летить на) {area}",
        "Реактивний дрон повз Бровари.",
    ),
    (
        r"\bтро(я|ю)\b",
        r"\bреактивний дрон\b (на|повз|летить на) {area}",
        "1 реактивний дрон летить на Трою.",
    ),
    (
        r"\bоболон(ь|і|ню)\b",
        r"\bреактивний дрон\b (на|повз|летить на) {area}",
        "Реактивний дрон на Оболонь.",
    ),
    (
        r"\bлів(ий|ого|ому) берег\b",
        r"{area}\W+(наступний реактивний\b|реактивний( йде\b| \d+\b|[!.]*$))",
        "Лівий берег - реактивний йде!",
    ),
    (
        r"\bтро(я|ю)\b",
        r"{area}\W+(наступний реактивний\b|реактивний( йде\b| \d+\b|[!.]*$))",
        "🛵 Троя, реактивний",
    ),
    (
        r"\bніжин(а|у|ом|і)?\b",
        r"\bреактивних\b( на|.{0,32}\bперший на) {area}",
        "2 реактивних на Ніжин йде",
    ),
    (
        r"\bтроєщин(а|и|і|у|ою)?\b",
        r"\bреактивних\b( на|.{0,32}\bперший на) {area}",
        "4 реактивних на Київ, перший на Троєщину/Оболонь.",
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
    *[(DangerType.BALLISTIC, s) for s in BALLISTIC_CASES],
    *[(DangerType.CRUISE, s) for s in CRUISE_CASES],
    *[(DangerType.DRONE, s) for s in DRONE_CASES],
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
    for text in DRONE_CASES:
        detection = detector.drone_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.DRONE, text


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
