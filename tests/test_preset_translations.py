"""Tests for Home Assistant preset translations."""

# ruff: noqa: S101

import json
from pathlib import Path

import pytest
from aerial_danger.location_presets import LOCATION_PRESETS


@pytest.mark.parametrize("language", ["en", "uk"])
def test_selector_translations_cover_regions(language: str) -> None:
    """Test every region preset has a selector translation in registry order."""
    translations_path = (
        Path(__file__).parents[1]
        / "custom_components"
        / "aerial_danger"
        / "translations"
        / f"{language}.json"
    )
    translations = json.loads(translations_path.read_text())
    options = translations["selector"]["region_presets"]["options"]
    assert list(options) == list(LOCATION_PRESETS)
    assert all(isinstance(label, str) and label for label in options.values())


@pytest.mark.parametrize("language", ["en", "uk"])
def test_selector_translations_cover_localities(language: str) -> None:
    """Test every preset has a selector translation in registry order."""
    translations_path = (
        Path(__file__).parents[1]
        / "custom_components"
        / "aerial_danger"
        / "translations"
        / f"{language}.json"
    )
    translations = json.loads(translations_path.read_text())
    options = translations["selector"]["locality_presets"]["options"]
    localities = {
        preset_id: preset
        for region in LOCATION_PRESETS.values()
        for preset_id, preset in region.localities.items()
    }
    assert list(options) == list(localities)
    assert all(isinstance(label, str) and label for label in options.values())
