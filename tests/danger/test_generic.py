"""Tests for generic danger detection."""

# ruff: noqa: S101

from custom_components.aerial_danger.danger import DangerDetector, DangerType

from .common import LOCALITY_PATTERNS, REGION_PATTERNS

GENERIC_CASES: list[str] = [
    "🔴🚀Нивки.",
    "🔴❗️Вектор Київ!",
    "🔴❗️Київ!",
    "🔴🚀 Київ!!",
    "❗️Київ!",
    "🟡Київ!",
    "🚀Нивки!",
    "Далі Нивки.",
    "❗️На Нивки!",
    "БОЯРКА - ВИШНЕВЕ - КИЇВ!!",
    "КИЇВ",
    "КИЇВ!",
    "КИЇВ 2 СТІНИ!",
    "КИЇВ Є ЦІЛІ!",
    "КИЇВ ЦІЛЬ!",
    "Київ є ЦІЛЬ!",
    "КИЇВ УВАГА!",
    "Київ зреагувати!!",
    "‼️Київ!",
    "Київ жахне!!",
    "Київ/Вишгород увага",
    "🔴🚀 Вектор руху на Київ!",
    "🚀 Вектор на столицю!",
    "ЦІЛЬ КИЇВЩИНА!",
    "Київ в укриття!",
    "Нивки зреагувати!",
    "Київ ваш вектор!",
    "Далі на Київ йде 2 цілі!!",
    "Петропавлівська на Академ/Святошин!",
    "Нивки!!!",
    "Нивки підліт",
    "Святошинський - увага !",
    "КИЇВ 2 ЦІЛІ!",
    "Курс - Київ!",
    "Нивки - Антонов!",
    "Київщина увага ще ЦІЛЬ!",
    "Київ повторно!",
    "Курсом на Київ!",
    "ЦІЛЬ КИЇВ",
    "КИЇВ ДВІ СТІНИ",
    "2 цілі на Київ",
    "КИЇВ УВАГА!!!!!",
    "КИЇВ ХВИЛИНА!!",
    "Київ ще групові, увага!",
    "🚀 Академмістечко",
    "🔴Київ!",
    "НИВКИ УВАГА!!!!!!!!",
    "🚀 Знову ціль на Київ!",
    "🚀Київ в укриття",
    "Київ !!!",
    "КИЇВ СХОВАЛИСЬ В ДВІ СТІНИ",
    "🔴🚀Нивки!",
    "🔴🚀 Святошин!",
    "🚀 Святошино/Нивки!",
    "Пролітає Галагани та Файна таун.",
    "Галагани на Святошин, Антонов. Нивки готовність!",
    "Хвилина до заходу в Київ!",
    "🔴🚀Вишгород/Оболонь!",
    "Бровари підліт. Ви його не почуєте. Від вікон.",
]

REGION_ONLY_INCOMING_WEAPON_CASES: list[tuple[str, str]] = [
    (r"\bки(ї|є)в(а|у|ом|е|і)?\b", "🟡💣 Київ!"),
    (r"\bхарків(а|у|ом|і)?\b", "🔴❗️ РСЗВ на Харків!"),
    (
        r"\bдніпропетровщин(а|и|і|у|ою)?\b",
        "🟡💣 КАБи на Дніпропетровщині, вектор Кривий Ріг!",
    ),
    (
        r"\bхарків(а|у|ом|і)?\b",
        "🟡💣 КАБ на Харків, вектор Стара Салтівка!",
    ),
]

GENERIC_WHOLE_MESSAGE_CASES: list[str] = [
    "КИЇВ!",
    "НИВКИ!",
    "❗️На Нивки!",
    "🔴❗️Вектор Київ!",
    "Курсом на Київ!",
]


def test_generic_only() -> None:
    """Generic helper should flag generic samples."""
    detector = DangerDetector(REGION_PATTERNS, LOCALITY_PATTERNS)
    for text in GENERIC_CASES:
        detection = detector.generic_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.GENERIC, text
        assert detector.danger(text).type == DangerType.GENERIC, text


def test_weapon_messages_do_not_fall_through_to_generic() -> None:
    """Typed messages with only a region match should stay neutral."""
    for region_pattern, text in REGION_ONLY_INCOMING_WEAPON_CASES:
        detector = DangerDetector([region_pattern], [])

        detection = detector.danger(text)

        assert detection.danger is False, text
        assert detection.type is None, text


def test_terse_generic_matches_complete_message() -> None:
    """Terse generic warnings should preserve the complete matched text."""
    detector = DangerDetector(REGION_PATTERNS, LOCALITY_PATTERNS)
    for text in GENERIC_WHOLE_MESSAGE_CASES:
        detection = detector.generic_danger(text)

        assert detection.danger is True, text
        assert detection.type == DangerType.GENERIC, text
        assert detection.matched_danger == text, text
