"""Tests for multiple launch rocket system danger detection."""

# ruff: noqa: S101

from custom_components.aerial_danger.danger import DangerDetector, DangerType

from .common import LOCALITY_PATTERNS, REGION_PATTERNS

MLRS_CASES: list[str] = [
    "🔴❗️ РСЗВ на Харків!",
    "Суми обстріл РСЗВ.",
    "Запоріжжя РСЗВ!",
    "Західні околиці Харкова почули вибух. Працює РСЗВ.",
    "❗️ Ведеться обстріл Шосткинського району Сумщини з РСЗВ.",
    "❗️ Уточнення: виходи РСЗВ у напрямку Запоріжжя.",
    "РСЗВ працює по передмістю Запоріжжя",
    "РСЗВ працює по району Очакова.\nБПЛА мандрує у Південне.",
    "Саме зараз відбувається обстріл з РСЗВ «Град» Миропілля на Сумщині.",
    "Купʼянськ на Харківщині під атакою ворожою РСЗВ.",
    (
        "❗️🚛 Харків під атакою ворожою РСЗВ!\n"
        "🟡❗️ Загроза повторного удару актуальна до відбою повітряної тривоги."
    ),
    "🚀 Працює ворожа РСЗВ по ЛБЗ на Сумщині в сектор н.п. Варачине.",
]

MLRS_NO_MATCH_CASES: list[str] = [
    "По Сумах було завдано удару РСЗВ.",
    "Харків: це було РСЗВ.",
    "РСЗВ на Суми, поки чисто.",
    "Підсумуємо: Харківщина зазнала удару РСЗВ.",
    "Пояснюємо, чим РСЗВ небезпечна для Харкова.",
]

MLRS_REGION_CASES: list[str] = [
    "⚠ Увага!\nОбстріл РСЗВ прикордонних населених пунктів на Харківщині.",
    "⚠ Чернігівщина під обстрілом РСЗВ з півночі.",
    "❗️ Повторні виходи РСЗВ на Миколаївщину.",
    "На Сумщині працює РСЗВ, не панікуєм.",
    "Обстріл з РСЗВ прикордоння Харківщини, корегує ворожий БПЛА.",
    "сумщина\nРСЗВ по прикордонню",
]


def test_mlrs_danger() -> None:
    """Live MLRS alerts should map to the MLRS danger type."""
    detector = DangerDetector(REGION_PATTERNS, LOCALITY_PATTERNS)
    for text in MLRS_CASES:
        detection = detector.mlrs_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.MLRS, text
        assert detector.danger(text).type == DangerType.MLRS, text


def test_mlrs_non_actionable_does_not_match() -> None:
    """Retrospective and analysis MLRS posts should stay neutral."""
    detector = DangerDetector(REGION_PATTERNS, LOCALITY_PATTERNS)
    for text in MLRS_NO_MATCH_CASES:
        detection = detector.danger(text)
        assert detection.danger is False, text
        assert detection.type is None, text
        assert detector.is_safe(text) is False, text


def test_mlrs_requires_configured_locality() -> None:
    """Region patterns should not activate the MLRS danger type."""
    detector = DangerDetector([r"\bхарків\b", *REGION_PATTERNS], [])

    detection = detector.danger("РСЗВ на Харків!")

    assert detection.type is not DangerType.MLRS

    for text in MLRS_REGION_CASES:
        detection = detector.mlrs_danger(text)
        assert detection.danger is False, text
        assert detection.type is None, text
