"""Tests for generated location selector translations."""

# ruff: noqa: S101

import json
import runpy
from pathlib import Path


def test_sync_preserves_ui_text_and_checks_without_writing(tmp_path: Path) -> None:
    """Generate both languages, preserve UI text, and detect stale output."""
    main = runpy.run_path(
        str(Path(__file__).parents[1] / "scripts/sync_location_names")
    )["main"]
    directory = tmp_path / "custom_components/aerial_danger/translations"
    directory.mkdir(parents=True)
    original = json.dumps(
        {
            "config": {"title": "Keep this text"},
            "selector": {
                "other": {"options": {"keep": "Keep"}},
                "region_presets": {"options": {"obsolete": "Old region"}},
                "locality_presets": {"options": {"obsolete": "Old place"}},
            },
        }
    )
    for language in ("en", "uk"):
        (directory / f"{language}.json").write_text(original)

    assert main(tmp_path, check=True) == 1
    assert all(path.read_text() == original for path in directory.glob("*.json"))
    assert main(tmp_path) == 0
    for language, expected_name in (("en", "Nyvky"), ("uk", "Нивки")):
        data = json.loads((directory / f"{language}.json").read_text())
        assert data["config"] == {"title": "Keep this text"}
        assert data["selector"]["other"] == {"options": {"keep": "Keep"}}
        assert (
            data["selector"]["locality_presets"]["options"]["kyiv_nyvky"]
            == expected_name
        )
        assert "obsolete" not in data["selector"]["locality_presets"]["options"]
        assert "obsolete" not in data["selector"]["region_presets"]["options"]
    assert main(tmp_path, check=True) == 0
    before = {path: path.stat().st_mtime_ns for path in directory.glob("*.json")}
    assert main(tmp_path) == 0
    assert {path: path.stat().st_mtime_ns for path in before} == before
