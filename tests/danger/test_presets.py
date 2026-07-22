"""Tests for area pattern presets."""

# ruff: noqa: S101

import json
import re
from pathlib import Path

import pytest

from custom_components.aerial_danger.danger import DangerDetector
from custom_components.aerial_danger.danger.pattern_utils import (
    neighborhood_ids,
    resolve_neighborhood_patterns,
    resolve_region_patterns,
)
from custom_components.aerial_danger.danger.presets import PRESETS


def test_registry_ids_ownership_and_compilation() -> None:
    """Test stable IDs, nested ownership, and valid regexes."""
    assert list(PRESETS) == ["kyiv"]
    assert neighborhood_ids([]) == []
    region = PRESETS["kyiv"]
    assert neighborhood_ids(["kyiv"]) == list(region.neighborhoods)
    assert region.name == "Київ"
    assert list(region.neighborhoods) == sorted(region.neighborhoods)
    DangerDetector.validate_patterns(
        region.patterns,
        *(preset.patterns for preset in region.neighborhoods.values()),
    )


@pytest.mark.parametrize("language", ["en", "uk"])
def test_selector_translations_cover_neighborhoods(language: str) -> None:
    """Test every preset has a selector translation in registry order."""
    translations_path = (
        Path(__file__).parents[2]
        / "custom_components"
        / "aerial_danger"
        / "translations"
        / f"{language}.json"
    )
    translations = json.loads(translations_path.read_text())
    options = translations["selector"]["neighborhood_presets"]["options"]
    neighborhoods = PRESETS["kyiv"].neighborhoods
    assert list(options) == list(neighborhoods)
    if language == "uk":
        assert options == {
            preset_id: preset.name for preset_id, preset in neighborhoods.items()
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
def test_additional_neighborhood_variants(preset_id: str, text: str) -> None:
    """Test additional aliases and spellings."""
    patterns = PRESETS["kyiv"].neighborhoods[preset_id].patterns
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


def test_boundaries_and_safe_location_text() -> None:
    """Test preset boundaries and ordinary location text stay safe."""
    regions = resolve_region_patterns([], ["kyiv"])
    neighborhoods = resolve_neighborhood_patterns(
        [], ["kyiv"], ["kyiv_akademmistechko"]
    )
    detector = DangerDetector(regions, neighborhoods)
    assert not any(re.search(pattern, "Київщина", re.IGNORECASE) for pattern in regions)
    assert not any(
        re.search(pattern, "академія", re.IGNORECASE) for pattern in neighborhoods
    )
    assert not detector.danger("Станція метро Академмістечко відкрита").danger


def test_resolve_custom_first_deduplicates_and_ignores_unknown_ids() -> None:
    """Test resolution order, deduplication, and current-definition lookup."""
    kyiv_pattern = PRESETS["kyiv"].patterns[0]
    regions = resolve_region_patterns([kyiv_pattern, "custom"], ["missing", "kyiv"])
    neighborhoods = resolve_neighborhood_patterns(
        [], ["missing", "kyiv"], ["kyiv_nyvky", "missing"]
    )
    assert regions == [kyiv_pattern, "custom", PRESETS["kyiv"].patterns[1]]
    assert neighborhoods == list(PRESETS["kyiv"].neighborhoods["kyiv_nyvky"].patterns)
