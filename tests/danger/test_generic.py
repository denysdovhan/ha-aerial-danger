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


def test_generic_only() -> None:
    """Generic helper should flag generic samples."""
    detector = DangerDetector(REGION_PATTERNS, LOCALITY_PATTERNS)
    for text in GENERIC_CASES:
        detection = detector.generic_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.GENERIC, text
        assert detector.danger(text).type == DangerType.GENERIC, text
