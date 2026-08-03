"""Tests for area pattern presets."""

# ruff: noqa: S101

import json
import re
from pathlib import Path

import pytest

from custom_components.aerial_danger.danger import DangerDetector
from custom_components.aerial_danger.danger.pattern_utils import (
    locality_ids,
    resolve_locality_patterns,
    resolve_region_patterns,
)
from custom_components.aerial_danger.danger.presets import PRESETS

PRESET_EXAMPLES = {
    "dnipropetrovsk_oblast": ("Дніпропетровщиною", "Дніпропетровській області"),
    "dnipropetrovsk_oblast_dnipro": ("Дніпром",),
    "dnipropetrovsk_oblast_kamianske": ("Кам'янському",),
    "dnipropetrovsk_oblast_kryvyi_rih": ("Кривого Рогу",),
    "dnipropetrovsk_oblast_pavlohrad": ("Павлоградом",),
    "kharkiv_oblast": ("Харківщиною", "Харківській області"),
    "kharkiv_oblast_balakliia": ("Балаклією",),
    "kharkiv_oblast_bohodukhiv": ("Богодуховом",),
    "kharkiv_oblast_derzhprom": ("Держпрому",),
    "kharkiv_oblast_kharkiv": ("Харкові",),
    "kharkiv_oblast_khtz": ("хтз",),
    "kharkiv_oblast_kozacha_lopan": ("Козачою Лопанню",),
    "kharkiv_oblast_kulynychi": ("Кулиничах",),
    "kharkiv_oblast_kupiansk": ("Куп'янськом",),
    "kharkiv_oblast_piatykhatky": ("П'ятихатках",),
    "kharkiv_oblast_saltivka": ("Салтівкою",),
    "kyiv": ("Києва", "Києві", "Києву", "Києвом", "столиця"),
    "kyiv_akademmistechko": ("Академмістечком",),
    "kyiv_darnytsia": ("Дарницький масив",),
    "kyiv_lisovyi_masyv": ("Лісовий",),
    "kyiv_livoberezhnyi_masyv": ("Лівобережний",),
    "kyiv_minskyi_masyv": ("Мінський",),
    "kyiv_sviatoshyn": ("Святошино",),
    "kyiv_troieshchyna": ("Троєщини",),
    "kyiv_vidradnyi": ("Відрадний",),
    "kyiv_voskresenka": ("Воскресенка",),
    "kyiv_oblast": (
        "Київщина",
        "Київщини",
        "Київщині",
        "Київщину",
        "Київщиною",
        "Київської області",
        "Київській області",
        "Київську область",
        "Київською областю",
    ),
    "kyiv_oblast_boryspil": (
        "Борисполя",
        "Борисполю",
        "Борисполем",
        "Борисполі",
        "Борік",
    ),
    "odesa_oblast": ("Одещиною", "Одеською областю"),
    "odesa_oblast_arkadiia": ("Аркадією",),
    "odesa_oblast_bilhorod_dnistrovskyi": ("Білгород Дністровському",),
    "odesa_oblast_chornomorsk": ("Чорноморськом",),
    "odesa_oblast_karolino_buhaz": ("Кароліно Бугазом",),
    "odesa_oblast_khadzhybeiskyi_raion": ("Хаджибейському районі",),
    "odesa_oblast_odesa": ("Одесою",),
    "odesa_oblast_odesa_port": ("Одеському порту", "Одеса / порт"),
    "odesa_oblast_ovidiopol": ("Овідіополем",),
    "odesa_oblast_peresyp": ("Пересипом",),
    "odesa_oblast_zatoka": ("Затокою",),
    "zaporizhzhia_oblast": ("Запорізькою областю",),
    "zaporizhzhia_oblast_komyshuvakha": ("Комишувахою",),
    "zaporizhzhia_oblast_orikhiv": ("Оріховом",),
    "zaporizhzhia_oblast_vilniansk": ("Вільнянськом",),
    "zaporizhzhia_oblast_zaporizhzhia": ("Запоріжжі", "ЗП"),
}


def test_registry_ids_ownership_and_compilation() -> None:
    """Test stable IDs, nested ownership, and valid regexes."""
    assert list(PRESETS) == [
        "dnipropetrovsk_oblast",
        "kharkiv_oblast",
        "kyiv",
        "kyiv_oblast",
        "odesa_oblast",
        "zaporizhzhia_oblast",
    ]
    assert locality_ids([]) == []
    for region_id, region in PRESETS.items():
        assert locality_ids([region_id]) == list(region.localities)
    for region in PRESETS.values():
        assert list(region.localities) == sorted(region.localities)
        DangerDetector.validate_patterns(
            region.patterns,
            *(preset.patterns for preset in region.localities.values()),
        )


@pytest.mark.parametrize("language", ["en", "uk"])
def test_selector_translations_cover_regions(language: str) -> None:
    """Test every region preset has a selector translation in registry order."""
    translations_path = (
        Path(__file__).parents[2]
        / "custom_components"
        / "aerial_danger"
        / "translations"
        / f"{language}.json"
    )
    translations = json.loads(translations_path.read_text())
    options = translations["selector"]["region_presets"]["options"]
    assert list(options) == list(PRESETS)
    if language == "uk":
        assert options == {
            preset_id: preset.name for preset_id, preset in PRESETS.items()
        }


@pytest.mark.parametrize("language", ["en", "uk"])
def test_selector_translations_cover_localities(language: str) -> None:
    """Test every preset has a selector translation in registry order."""
    translations_path = (
        Path(__file__).parents[2]
        / "custom_components"
        / "aerial_danger"
        / "translations"
        / f"{language}.json"
    )
    translations = json.loads(translations_path.read_text())
    options = translations["selector"]["locality_presets"]["options"]
    localities = {
        preset_id: preset
        for region in PRESETS.values()
        for preset_id, preset in region.localities.items()
    }
    assert list(options) == list(localities)
    if language == "uk":
        assert options == {
            preset_id: preset.name for preset_id, preset in localities.items()
        }


def test_preset_examples() -> None:
    """Test preset aliases, inflections, and alternate spellings."""
    patterns_by_id = {}
    for region_id, region in PRESETS.items():
        patterns_by_id[region_id] = region.patterns
        patterns_by_id.update(
            {
                preset_id: preset.patterns
                for preset_id, preset in region.localities.items()
            }
        )

    assert PRESET_EXAMPLES.keys() <= patterns_by_id.keys()
    for preset_id, texts in PRESET_EXAMPLES.items():
        for text in texts:
            assert any(
                re.search(pattern, text, re.IGNORECASE | re.UNICODE)
                for pattern in patterns_by_id[preset_id]
            ), (preset_id, text)


def test_boundaries_and_safe_location_text() -> None:
    """Test preset boundaries and ordinary location text stay safe."""
    regions = resolve_region_patterns([], ["kyiv"])
    localities = resolve_locality_patterns([], ["kyiv"], ["kyiv_akademmistechko"])
    detector = DangerDetector(regions, localities)
    assert not any(re.search(pattern, "Київщина", re.IGNORECASE) for pattern in regions)
    assert not any(
        re.search(pattern, "академія", re.IGNORECASE) for pattern in localities
    )
    assert not detector.danger("Станція метро Академмістечко відкрита").danger


def test_resolve_custom_first_deduplicates_and_ignores_unknown_ids() -> None:
    """Test resolution order, deduplication, and current-definition lookup."""
    kyiv_pattern = PRESETS["kyiv"].patterns[0]
    regions = resolve_region_patterns([kyiv_pattern, "custom"], ["missing", "kyiv"])
    localities = resolve_locality_patterns(
        [], ["missing", "kyiv"], ["kyiv_nyvky", "missing"]
    )
    assert regions == [kyiv_pattern, "custom", PRESETS["kyiv"].patterns[1]]
    assert localities == list(PRESETS["kyiv"].localities["kyiv_nyvky"].patterns)
