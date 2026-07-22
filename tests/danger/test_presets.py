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


def test_registry_ids_ownership_and_compilation() -> None:
    """Test stable IDs, nested ownership, and valid regexes."""
    assert list(PRESETS) == ["kyiv", "kyiv_oblast"]
    assert locality_ids([]) == []
    for region_id, region in PRESETS.items():
        assert locality_ids([region_id]) == list(region.localities)
    assert PRESETS["kyiv"].name == "Київ"
    assert PRESETS["kyiv_oblast"].name == "Київська область"
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


@pytest.mark.parametrize(
    ("preset_id", "text"),
    [
        ("kyiv_akademmistechko", "Академмістечком"),
        ("kyiv_darnytsia", "Дарницький масив"),
        ("kyiv_lisovyi_masyv", "Лісовий"),
        ("kyiv_livoberezhnyi_masyv", "Лівобережний"),
        ("kyiv_minskyi_masyv", "Мінський"),
        ("kyiv_sviatoshyn", "Святошино"),
        ("kyiv_troieshchyna", "Троєщини"),
        ("kyiv_vidradnyi", "Відрадний"),
        ("kyiv_voskresenka", "Воскресенка"),
    ],
)
def test_additional_locality_variants(preset_id: str, text: str) -> None:
    """Test additional aliases and spellings."""
    patterns = PRESETS["kyiv"].localities[preset_id].patterns
    assert any(
        re.search(pattern, text, re.IGNORECASE | re.UNICODE) for pattern in patterns
    )


@pytest.mark.parametrize(
    "text", ["Київ", "Києва", "Києві", "Києву", "Києвом", "столиця"]
)
def test_researched_kyiv_variants(text: str) -> None:
    """Test researched Kyiv wording."""
    assert any(
        re.search(pattern, text, re.IGNORECASE | re.UNICODE)
        for pattern in PRESETS["kyiv"].patterns
    )


@pytest.mark.parametrize(
    "text",
    [
        "Київщина",
        "Київщини",
        "Київщині",
        "Київщину",
        "Київщиною",
        "Київська область",
        "Київської області",
        "Київській області",
        "Київську область",
        "Київською областю",
    ],
)
def test_researched_kyiv_oblast_variants(text: str) -> None:
    """Test researched Kyiv Oblast wording."""
    assert any(
        re.search(pattern, text, re.IGNORECASE | re.UNICODE)
        for pattern in PRESETS["kyiv_oblast"].patterns
    )


@pytest.mark.parametrize(
    "text", ["Бориспіль", "Борисполя", "Борисполю", "Борисполем", "Борисполі", "Борік"]
)
def test_boryspil_variants(text: str) -> None:
    """Test Boryspil forms and its alert shorthand."""
    patterns = PRESETS["kyiv_oblast"].localities["kyiv_oblast_boryspil"].patterns
    assert any(
        re.search(pattern, text, re.IGNORECASE | re.UNICODE) for pattern in patterns
    )


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
