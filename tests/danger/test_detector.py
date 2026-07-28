"""Tests for common danger detector behavior."""

# ruff: noqa: S101

import re

import pytest

from custom_components.aerial_danger.danger import (
    DangerDetector,
    PatternMatch,
)

from .common import LOCALITY_PATTERNS, REGION_PATTERNS

NO_MATCH_CASES: list[str] = [
    "🛵Шахед на Мену.",
    "🛵7 Шахедів з моря на Татарбунари.",
    "🛵Залишився 1 Шахед на півночі Київщині, летить в напрямку Чорнобиля!",
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
]


def test_validate_patterns() -> None:
    """Configured patterns compile independently from the detector."""
    DangerDetector.validate_patterns(REGION_PATTERNS, LOCALITY_PATTERNS)

    with pytest.raises(re.error):
        DangerDetector.validate_patterns(["("])


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
    detector = DangerDetector(REGION_PATTERNS, LOCALITY_PATTERNS)
    for text in NO_MATCH_CASES:
        detection = detector.danger(text)
        assert detection.danger is False, text
        assert detection.type is None, text
