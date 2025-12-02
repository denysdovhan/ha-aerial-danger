"""
Detection cases derived from plan/cases.md.

Add new samples by extending `MATCH_CASES` or `NO_MATCH_CASES`.
"""
# ruff: noqa: S101

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from custom_components.aerial_danger.lib.danger import DangerDetector, DangerType

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

MATCH_CASES: list[tuple[DangerType, str]] = [
    (DangerType.BALLISTIC, "Київ швидкісна!"),
    (DangerType.BALLISTIC, "КИЇВ Є ЦІЛІ!"),
    (DangerType.BALLISTIC, "Київ спуск! Одна за другою!"),
    (DangerType.BALLISTIC, "❗️ Балістика у напрямку Києва"),
    (DangerType.BALLISTIC, "❗️Повторний вихід з Брянська у напрямку Києва"),
    (DangerType.BALLISTIC, "🔴❗️Київ!"),
    (DangerType.BALLISTIC, "🔴❗️Вектор Київ!"),
    (DangerType.BALLISTIC, "КИЇВ ЦІЛЬ!"),
    (DangerType.BALLISTIC, "🔴🚀 «Кинджал» Київ!"),
    (DangerType.BALLISTIC, "🔴🚀 Вектор руху на Київ!"),
    (DangerType.BALLISTIC, "КИЇВ 2 СТІНИ!"),
    (DangerType.BALLISTIC, "🔴🚀Нивки."),
    (DangerType.BALLISTIC, "☄Київ Балістика!"),
    (DangerType.BALLISTIC, "КИЇВ ШВИДКІСНА"),
    (DangerType.BALLISTIC, "🚀Швидкісна ціль на Київ!"),
    (DangerType.BALLISTIC, "Ще балістика на Київ!"),
    (DangerType.BALLISTIC, "‼️ Київ — спуск балістики!"),
    (DangerType.BALLISTIC, "🚀 Київ! Балістика!"),
    (DangerType.BALLISTIC, "🚀 Київ! Ще балістика!"),
    (DangerType.BALLISTIC, "🚀 Київ, балістика!"),
    (DangerType.BALLISTIC, "❗️ Кинджал вектор Київ/агломерація"),
    (DangerType.BALLISTIC, "🚀 Київ! Кинджал!"),
    (DangerType.BALLISTIC, "Київ є ЦІЛЬ!"),
    (DangerType.BALLISTIC, "🔴🚀 Київ!!"),
    (DangerType.BALLISTIC, "КИЇВ КИНДЖАЛ"),
    (DangerType.BALLISTIC, "🚀 Швидкісна у бік Києва!"),
    (DangerType.BALLISTIC, "‼️Київ — спуск Кинджалу!"),
    (DangerType.CRUISE, "🔴Ракета Київ!"),
    (DangerType.CRUISE, "КР Позняки\n КР Теремки\n КР Солом'янка\n КР Нивки"),
    (DangerType.CRUISE, "Київ увага КР!!"),
    (DangerType.CRUISE, "❗ Київ — група КР на місто"),
    (DangerType.CRUISE, "❗️🚀КИЇВ 3-4 ХВЛИНИ ДО КР!"),
    (DangerType.CRUISE, "Київ і агломерація бути в укриттях по КР"),
    (DangerType.CRUISE, "🚀 Васильків/Київ, йде з півдня!"),
    (DangerType.CRUISE, "Київ увага по КР"),
    (DangerType.CRUISE, "Київ ще групи КР!"),
    (DangerType.CRUISE, "‼️ Київ — наближення крилатих ракет"),
    (DangerType.CRUISE, "Київ увага — КР"),
    (DangerType.CRUISE, "🚀 Вектор на столицю!"),
    (DangerType.CRUISE, "Кинджал у бік Києва/Житомира."),
    (DangerType.CRUISE, "🚀Нивки!"),
    (DangerType.CRUISE, "До 4 КР на Київ/Бориспіль."),
    (
        DangerType.CRUISE,
        "🟡🚀Калібри з Житомирщини розвертаються на Київщину, вектор Київ!",
    ),
    (DangerType.CRUISE, "🚀 Калібри на Київ!"),
    (DangerType.CRUISE, "🚀КР на Київ!"),
    (DangerType.CRUISE, "🟡🚀Калібри на Святошинський район!"),
    (DangerType.CRUISE, "КАЛІБР КИЇВ!"),
    (DangerType.CRUISE, "🔴🚀4х групи крилатих ракет підлітають до Києва!"),
    (DangerType.CRUISE, "🔴🚀Святошино!"),
    (DangerType.CRUISE, "🟡🚀Ракета на Київ, вектор Академмістечко!"),
    (DangerType.CRUISE, "🚀 Група крилатих ракет на Чернігівщині. Курс до нас."),
    (DangerType.CRUISE, "🚀 Крилаті з Житомирщини курсом до нас."),
    (DangerType.CRUISE, "❗️Короче, до 10 штук. Крилаті курсом на нашу область."),
    (DangerType.DRONE, "❗️ Київ — 1х Академ/Коцюбинське."),
    (DangerType.DRONE, "Київ:\n 1х Нивки/Сирець\n 2х Жуляни\n \n 1х ДВРЗ/Березняки"),
    (DangerType.DRONE, "🛵 У бік Нивок."),
    (DangerType.DRONE, "Київ: \n 2х Куренівка Нивки \n 1х Бортничі"),
    (DangerType.DRONE, "❗️ Київ — 1х Нивки Сирець"),
    (DangerType.DRONE, "❗️ Київ — 1х на Святошин."),
    (DangerType.DRONE, "🛵 Нивки, може бути гучно!"),
    (DangerType.DRONE, "Нивки над вами БПЛА!"),
    (DangerType.DRONE, "🛵 Курс на Нивки/Святошино."),
    (DangerType.DRONE, "Антонов йде!"),
    (DangerType.DRONE, "Святошино/Нивки 🛵"),
    (DangerType.GENERIC, "❗️Київ!"),
    (DangerType.GENERIC, "🟡Київ!"),
    (DangerType.GENERIC, "Далі Нивки."),
    (DangerType.GENERIC, "❗️На Нивки!"),
    (DangerType.GENERIC, "БОЯРКА - ВИШНЕВЕ - КИЇВ!!"),
    (DangerType.GENERIC, "КИЇВ!"),
    (DangerType.GENERIC, "Київ зреагувати!!"),
    (DangerType.GENERIC, "‼️Київ!"),
    (DangerType.GENERIC, "Київ жахне!!"),
    (DangerType.GENERIC, "Нивки увага!"),
    (DangerType.GENERIC, "Київ/Вишгород увага"),
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
