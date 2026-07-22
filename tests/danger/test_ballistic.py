"""Tests for ballistic danger detection."""

# ruff: noqa: S101

from custom_components.aerial_danger.danger import DangerDetector, DangerType

from .common import LOCALITY_PATTERNS, REGION_PATTERNS

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


def test_ballistic_only() -> None:
    """Ballistic-specific helper should flag ballistic samples."""
    detector = DangerDetector(REGION_PATTERNS, LOCALITY_PATTERNS)
    for text in BALLISTIC_CASES:
        detection = detector.ballistic_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.BALLISTIC, text
        assert detector.danger(text).type == DangerType.BALLISTIC, text


def test_zircon_is_ballistic() -> None:
    """Shared Zircon keywords should match ballistic detection."""
    detector = DangerDetector([r".*"], [])
    for text in ZIRCON_CASES:
        ballistic = detector.ballistic_danger(text)
        assert ballistic.danger is True, text
        assert ballistic.type == DangerType.BALLISTIC, text
        assert detector.danger(text).type == DangerType.BALLISTIC, text


def test_targeted_zircon_is_ballistic() -> None:
    """Targeted Zircon alerts should match ballistic detection."""
    for area, text in TARGETED_ZIRCON_CASES:
        detector = DangerDetector([area], [])
        ballistic = detector.ballistic_danger(text)
        assert ballistic.danger is True, text
        assert ballistic.type == DangerType.BALLISTIC, text
