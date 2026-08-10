"""Tests for safety messages."""

# ruff: noqa: S101

import pytest

from custom_components.aerial_danger.danger import DangerDetector

from .common import REGION_PATTERNS

SAFETY_CASES: list[str] = [
    (
        "Маємо підготовку до пусків балістики. Планується залучення близько "
        '10 ОТРК "Іскандер" з Брянська по Київщині.'
    ),
    "Планується залучення ОТРК «Іскандер» по Київщині.",
    "По Києву було застосовано балістичні ракети. Атака завершена.",
    "🚀 Ракета на Київ.\n\nРакета припинила своє існування.",
    "☄ Балістика на Київ.\n\nРакети припинили своє існування.",
    "По Києву все, цілей більше немає.",
    "КИЇВ УВАГА!\n\nЦІЛІ ЗНИКЛИ.",
    "КИЇВ УВАГА!\nЦІЛІ ЗНИКЛИ",
    "Все тихо",
    "💥 Одещина вибухи, дорозвідка.",
    "балістика відбій",
    "⚪️ Відбій загрози балістики.",
    "🟢 ВІДБІЙ ТРИВОГИ | Київ10:00",
    "🟡Чисто на цю мить.",
    "Цілей поки немає.",
    "По балістичних цілях — чисто.",
    "По «реактивних » також чисто.",
    "Область візуально чисто",
    "❕ Локаційно область чиста",
    "❕Припинила існування.",
    (
        "Уточнена інформація щодо ракетного удару по Києву: "
        "зафіксовано влучання балістичної ракети."
    ),
    (
        "У ніч на 28 липня противник атакував Київ та Київщину "
        "балістичними і крилатими ракетами та ударними БпЛА. "
        "Збито/подавлено більшість повітряних цілей. "
        "Зафіксовано влучання."
    ),
    (
        "Чисто на околицях, Київ трішки на перекур. "
        "Присутні цілі в області, але не так близько, очікуємо підліт."
    ),
]


@pytest.mark.parametrize(
    "text",
    SAFETY_CASES,
)
def test_safety_does_not_match(text: str) -> None:
    """Explicit clear posts should not raise danger flags."""
    detector = DangerDetector(REGION_PATTERNS, [])

    detection = detector.danger(text)

    assert detection.danger is False, text
    assert detection.type is None, text
    assert detector.is_safe(text) is True, text


@pytest.mark.parametrize(
    "text",
    [
        "Буде відбій згодом.",
        (
            "По ракетам чисто наразі, відбулись масовані пуски реактивних "
            "дронів. Близько 10 реактивних летять на Київщину."
        ),
    ],
)
def test_future_or_partial_clear_is_not_safe(text: str) -> None:
    """Future or weapon-specific clear wording should not veto current danger."""
    detector = DangerDetector(REGION_PATTERNS, [])

    assert detector.is_safe(text) is False, text
