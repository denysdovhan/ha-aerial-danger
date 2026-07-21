"""Tests for area pattern presets."""

# ruff: noqa: S101

import re

import pytest

from custom_components.aerial_danger.danger import DangerDetector
from custom_components.aerial_danger.danger.presets import (
    PRESETS,
    neighborhood_ids,
    resolve_neighborhood_patterns,
    resolve_region_patterns,
)


def test_registry_ids_ownership_and_compilation() -> None:
    """Test stable IDs, nested ownership, and valid regexes."""
    assert list(PRESETS) == ["kyiv"]
    assert neighborhood_ids(["kyiv"]) == [
        "kyiv_sviatoshyn",
        "kyiv_akademmistechko",
        "kyiv_antonov",
        "kyiv_nyvky",
        "kyiv_vynohradar",
    ]
    assert neighborhood_ids([]) == []
    region = PRESETS["kyiv"]
    assert region.name == "Kyiv"
    assert [preset.name for preset in region.neighborhoods.values()] == [
        "Sviatoshyn",
        "Akademmistechko",
        "Antonov",
        "Nyvky",
        "Vynohradar",
    ]
    DangerDetector.validate_patterns(
        region.patterns,
        *(preset.patterns for preset in region.neighborhoods.values()),
    )


@pytest.mark.parametrize(
    ("preset_id", "text"),
    [
        ("kyiv_sviatoshyn", "Святошино"),
        ("kyiv_akademmistechko", "Академ"),
        ("kyiv_akademmistechko", "Академмістечком"),
        ("kyiv_antonov", "Антонова"),
        ("kyiv_nyvky", "Нивках"),
        ("kyiv_vynohradar", "Виноградарі"),
    ],
)
def test_researched_neighborhood_variants(preset_id: str, text: str) -> None:
    """Test researched neighborhood wording."""
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
