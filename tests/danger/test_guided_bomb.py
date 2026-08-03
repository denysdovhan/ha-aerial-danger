"""Tests for guided bomb danger detection."""

# ruff: noqa: S101

import pytest

from custom_components.aerial_danger.danger import DangerDetector, DangerType

from .common import LOCALITY_PATTERNS, REGION_PATTERNS

GUIDED_BOMB_CASES: list[str] = [
    "🟡💣 Вокзал!",
    "🟡💣 КАБ на Харків, вектор Стара Салтівка!",
    "🟡💣 КАБ повз Кароліно-Бугаз на Овідіополь!",
    "🟡💣 Пуск КАБ на Запоріжжя!",
    "🟡💣 КАБи на Дніпропетровщині, вектор Кривий Ріг!",
    "🚀 КАБи ➡️ на Донеччину (Слов'янськ)!",
    "Суми увага КАБ!",
    "КАБи на Запоріжжя!",
    "💣 Пуск КАБу у напрямку Херсон/Кринки.",
    "🚀 Пуски КАБ на Запоріжжя, Харківщину та Донеччину",
    "💣 КАБ у напрямку Харків.",
    "Суми повтор КАБи!",
    "Миколаїв увага, рух Каба в район",
    "На Козачу Лопань КАБ поки йде.",
    "КАБ йде в сектор Станіслав - Миколаїв - Очаків.",
    "КАБ східні околиці Семенівки.",
    "💣 Пуск КАБ в районі т.о. Скадовська, вектор Очаків.",
    "🟡💣 Наближення КАБ до Очакова, невдовзі буде гучно!",
    "2х КАБ на Харків, вектор Держпром!",
    "2х КАБ та Молнія на Суми!",
    "Ще й КАБ на Шостку",
]

GUIDED_BOMB_NO_MATCH_CASES: list[str] = [
    "Ймовірно знову КАБи в бік Одещини будуть кидати. Набрали висоту.",
    "Су-34 високо, імовірно на пуски КАБ в бік Сум.",
    "Су-34 може йти на пуски КАБ в бік Харкова.",
    (
        "Настали ті дні, коли КАБ теоретично вже може долітати до Київщини. "
        "Поки без столиці."
    ),
    "Ворогом нанесений по Сумах удар 6 КАБами. Є постраждалі.",
    "Аналітика: дальність КАБ до Харкова.",
]

GUIDED_BOMB_REGION_CASES: list[str] = [
    "🟡💣 КАБи на Дніпропетровщині!",
    "🚀 Пуски КАБ на Харківщину",
    "🚀 КАБи ➡️ на Харківщину зі сходу!",
    "🚀 Пуски КАБ ➡️ на схід Дніпропетровщини!",
    "Фіксується лише БпЛА на Дніпропетровщині та КАБ на Харківщину",
    (
        "🚀 Пуски керованих авіаційних бомб ворожою тактичною авіацією "
        "на Дніпропетровщину (Синельниківський р-н)."
    ),
    (
        "🚀 Повторні пуски керованих авіаційних бомб ворожою тактичною "
        "авіацією на Запорізьку область."
    ),
]

GUIDED_BOMB_SAFETY_CASES: list[str] = [
    "2х КАБ припинили своє існування на Сумщині.",
]


def test_guided_bomb_danger() -> None:
    """Live guided bomb alerts should map to the guided bomb danger type."""
    detector = DangerDetector(REGION_PATTERNS, LOCALITY_PATTERNS)
    for text in GUIDED_BOMB_CASES:
        detection = detector.guided_bomb_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.GUIDED_BOMB, text
        assert detector.danger(text).type == DangerType.GUIDED_BOMB, text


@pytest.mark.parametrize(
    "term",
    ["Керована авіабомба", "керовані авіабомби"],
)
def test_requested_guided_bomb_terms(term: str) -> None:
    """Requested compact guided bomb terms should remain supported."""
    detector = DangerDetector([], [r"\bхарків\b"])

    detection = detector.guided_bomb_danger(f"{term} на Харків.")

    assert detection.danger is True
    assert detection.type == DangerType.GUIDED_BOMB


def test_guided_bomb_non_actionable_does_not_match() -> None:
    """Forecast, analysis, and aftermath posts should stay neutral."""
    detector = DangerDetector(REGION_PATTERNS, LOCALITY_PATTERNS)
    for text in GUIDED_BOMB_NO_MATCH_CASES:
        detection = detector.danger(text)
        assert detection.danger is False, text
        assert detection.type is None, text
        assert detector.is_safe(text) is False, text


def test_guided_bomb_safety_does_not_match() -> None:
    """Explicitly resolved guided bomb posts should clear danger."""
    detector = DangerDetector(REGION_PATTERNS, LOCALITY_PATTERNS)
    for text in GUIDED_BOMB_SAFETY_CASES:
        detection = detector.danger(text)
        assert detection.danger is False, text
        assert detection.type is None, text
        assert detector.is_safe(text) is True, text


def test_guided_bomb_requires_configured_locality() -> None:
    """Region patterns should not activate the guided bomb danger type."""
    detector = DangerDetector([r"\bхарків\b", *REGION_PATTERNS], [])

    detection = detector.danger("КАБ на Харків!")

    assert detection.type is not DangerType.GUIDED_BOMB

    for text in GUIDED_BOMB_REGION_CASES:
        detection = detector.guided_bomb_danger(text)
        assert detection.danger is False, text
        assert detection.type is None, text
