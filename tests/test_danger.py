"""Tests for the DangerDetector class in the aerial_danger custom component."""

from custom_components.aerial_danger.danger import DangerDetector, DangerType

CITY_PATTERNS = [
    r"\bки(ї|є)в(а|у|ом|е|і)?\b",
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
]


def test_ballistic_only() -> None:
    """Ballistic-specific helper should flag ballistic samples."""
    detector = DangerDetector(CITY_PATTERNS, NEIGHBORHOOD_PATTERNS)
    for text in BALLISTIC_CASES:
        detection = detector.ballistic_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.BALLISTIC, text


def test_cruise_only() -> None:
    """Cruise-specific helper should flag cruise samples."""
    detector = DangerDetector(CITY_PATTERNS, NEIGHBORHOOD_PATTERNS)
    for text in CRUISE_CASES:
        detection = detector.cruise_missile_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.CRUISE, text


def test_drone_only() -> None:
    """Drone-specific helper should flag drone samples."""
    detector = DangerDetector(CITY_PATTERNS, NEIGHBORHOOD_PATTERNS)
    for text in DRONE_CASES:
        detection = detector.drone_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.DRONE, text


def test_generic_only() -> None:
    """Generic helper should flag generic samples."""
    detector = DangerDetector(CITY_PATTERNS, NEIGHBORHOOD_PATTERNS)
    for text in GENERIC_CASES:
        detection = detector.generic_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.GENERIC, text


def test_matches_expected_types() -> None:
    """All positive samples should be detected with the expected type."""
    detector = DangerDetector(CITY_PATTERNS, NEIGHBORHOOD_PATTERNS)
    for expected_type, text in MATCH_CASES:
        detection = detector.danger(text)
        assert detection.danger is True, text
        assert detection.type == expected_type, text


def test_non_matches() -> None:
    """Negative samples should not raise danger flags."""
    detector = DangerDetector(CITY_PATTERNS, NEIGHBORHOOD_PATTERNS)
    for text in NO_MATCH_CASES:
        detection = detector.danger(text)
        assert detection.danger is False, text
        assert detection.type is None, text
