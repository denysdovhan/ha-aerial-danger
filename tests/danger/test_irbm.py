"""Tests for intermediate-range ballistic missile danger detection."""

# ruff: noqa: S101

from custom_components.aerial_danger.danger import DangerDetector, DangerType
from custom_components.aerial_danger.danger.keywords import IRBM_DANGER

IRBM_CASES: list[tuple[str, str]] = [
    (
        IRBM_DANGER[0],
        "‼️Увага! Загроза застосування балістики середньої дальності (БРСД) "
        "по всій території України.\nІмовірний пуск ракети Кедр/Орєшнік "
        "(п/п РС-26).",
    ),
    (
        IRBM_DANGER[0],
        "‼️ Загроза застосування балістики середньої дальності (БРСД) "
        "по всій території України.",
    ),
    (IRBM_DANGER[2], "Загроза БРСД."),
    (IRBM_DANGER[2], "Повторна загроза БРСД."),
    (
        IRBM_DANGER[1],
        "🚨Загроза застосування балістичної ракети середньої дальності (Орєшнік).",
    ),
    (
        IRBM_DANGER[2],
        "❗️Загроза застосування БРСД «Орєшнік» по території України.",
    ),
    (IRBM_DANGER[3], "пуск Орєшніка"),
    (
        IRBM_DANGER[4],
        "🚀 Є інформація про пуск Орешніка! Протягом 10 хвилин уважно.",
    ),
    (
        IRBM_DANGER[4],
        "🚀 Є інформація про пуск Орешніка! (Протягом 10 хвилин уважно).",
    ),
    (IRBM_DANGER[5], "🚀 Була інформація про пуск Орєшніка!"),
    (IRBM_DANGER[6], "❗️Загроза пусків Орєшніка!"),
    (IRBM_DANGER[6], "🔴❗️Загроза застосування «Орєшніка»!"),
    (IRBM_DANGER[6], "❗️Загроза нанесення Орешніка!"),
    (IRBM_DANGER[6], "Upd. Загроза пуски Орєшніка!"),
    (IRBM_DANGER[6], "загроза орєшніка"),
    (IRBM_DANGER[7], "тривога по Орєшніку!"),
    (IRBM_DANGER[8], "🔴По Орєшніку загроза актуальна!"),
    (
        IRBM_DANGER[9],
        "Увага поширення тривоги по всій країні на імовірну активність БРСД "
        "з полігону КапЯр!",
    ),
    (
        IRBM_DANGER[10],
        "❗️Додалась загроза застосування балістики з Капустиного Яру (орєшнік).",
    ),
    (
        IRBM_DANGER[11],
        "❗️ Загроза застосування міжконтинентальних балістичних ракет РС-26 «Рубіж».",
    ),
]

IRBM_POTENTIAL_CASES: list[str] = [
    "Імовірний пуск ракети Кедр/Орєшнік (п/п РС-26).",
    "Ймовірно був пуск з Капустиного Яру. Очікуємо.",
    "Попередньо, превентивна загроза БРСД по всій країні!",
    "Попередьно, загроза БРСД.",
    "❗️Також отримали попередження стосовно загрози застосування БРСД "
    "впродовж декількох годин.",
    "попередньо, пуск орєшніка",
    "Можливі тривоги по причині загрози міжконтинентальної балістичної "
    'ракети "Рубіж" (Орешник).',
    "За інформацією, на полігоні «Капустин Яр» відбуваються підготовчі "
    "дії до запуску міжконтинентальної балістичної ракети «Орєшнік».",
    "За інформацією, противник готовий протягом двох годин здійснити "
    "пуск до 2-х ракет «Орєшнік».",
    "рф готує новий запуск БРСД “Орєшнік” з полігону Капустин Яр по "
    "Україні найближчим часом.",
    "Окремо діє попередження про ймовірне застосування БРСД "
    "«Кедр/Орєшнік» по території України.",
    "По всій країні тривогу оголошено превентивно, оскільки надійшла "
    "інформація про можливий пуск БСД «Орєшнік» з полігону «Капустин Яр».",
    "🟡Підвищена загроза застосування балістичної ракети середньої "
    "дальності «Орєшнік» по території України!",
    "Повітряні Сили ЗС України офіційно повідомили про загрозу "
    "застосування БРСД «Орєшнік» по території України протягом доби.",
    "❗️Загроза пусків БРСД «Орєшнік» із полігону «Капустин Яр» зберігається до 19.02.",
]

IRBM_AFTERMATH_CASES: list[str] = [
    "Момент удару «Орєшніком» по Львівщині.",
    "СБУ показала уламки балістичної ракети середньої дальності «Кедр», "
    "якою вчора атакували Львівщину.",
    "Відбій загрози БРСД по території України.",
    "Станом на зараз не володіємо інформацією про загрозу застосування "
    "балістики середньої дальності Кедр (Орєшнік).",
    "З’являються деталі щодо застосування другої балістичної ракети "
    "середньої дальності «Кєдр/Орєшнік» під час минулої атаки.",
    "У ніч на 24 травня ворог застосував 0/1 БРСД «Кєдр/Орєшнік».",
]


def test_irbm_is_nationwide() -> None:
    """IRBM alerts should not require configured area patterns."""
    detector = DangerDetector([], [])
    for danger_pattern, text in IRBM_CASES:
        detection = detector.irbm_danger(text)
        assert detection.danger is True, text
        assert detection.type == DangerType.IRBM, text
        assert detection.matched_area is None, text
        assert detection.area_pattern is None, text
        assert detection.danger_pattern == danger_pattern, text
        assert detector.danger(text).type == DangerType.IRBM, text


def test_irbm_aftermath_does_not_match() -> None:
    """IRBM aftermath and all-clear posts should not raise danger flags."""
    detector = DangerDetector([], [])
    for text in IRBM_AFTERMATH_CASES:
        detection = detector.danger(text)
        assert detection.danger is False, text
        assert detection.type is None, text


def test_irbm_potential_danger_does_not_match() -> None:
    """IRBM forecasts and preparations should not raise danger flags."""
    detector = DangerDetector([], [])
    for text in IRBM_POTENTIAL_CASES:
        detection = detector.danger(text)
        assert detection.danger is False, text
        assert detection.type is None, text
