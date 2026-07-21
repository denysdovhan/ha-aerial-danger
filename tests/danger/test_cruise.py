"""Tests for cruise missile danger detection."""

# ruff: noqa: S101

from custom_components.aerial_danger.danger import DangerDetector, DangerType

from .common import NEIGHBORHOOD_PATTERNS, REGION_PATTERNS
from .test_ballistic import TARGETED_ZIRCON_CASES, ZIRCON_CASES

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


def test_cruise_only() -> None:
    """Cruise-specific helper should flag cruise samples."""
    detector = DangerDetector(REGION_PATTERNS, NEIGHBORHOOD_PATTERNS)
    for text in CRUISE_CASES:
        detection = detector.cruise_missile_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.CRUISE, text
        assert detector.danger(text).type == DangerType.CRUISE, text


def test_zircon_is_cruise() -> None:
    """Shared Zircon keywords should match cruise detection."""
    detector = DangerDetector([r".*"], [])
    for text in ZIRCON_CASES:
        detection = detector.cruise_missile_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.CRUISE, text


def test_targeted_zircon_is_cruise() -> None:
    """Targeted Zircon alerts should match cruise detection."""
    for area, text in TARGETED_ZIRCON_CASES:
        detector = DangerDetector([area], [])
        detection = detector.cruise_missile_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.CRUISE, text
