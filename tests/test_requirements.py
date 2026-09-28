"""Check the library pin used by Home Assistant and development tooling."""

# ruff: noqa: S101

import json
import tomllib
from pathlib import Path


def test_library_requirement_matches_project() -> None:
    """Dependency updates must include the Home Assistant manifest."""
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text())
    manifest = json.loads(
        (root / "custom_components/aerial_danger/manifest.json").read_text()
    )
    requirement = next(
        item
        for item in project["project"]["dependencies"]
        if item.startswith("aerial-danger==")
    )
    assert requirement in manifest["requirements"], (
        "Run uv run python scripts/sync_library"
    )
