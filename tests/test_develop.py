"""Check development launcher imports without starting Home Assistant."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def test_develop_keeps_library_and_integration_imports_separate(tmp_path: Path) -> None:
    """The launcher must not shadow the published aerial_danger package."""
    root = Path(__file__).resolve().parents[1]
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    shutil.copy2(root / "scripts/develop", scripts / "develop")
    (tmp_path / "config").mkdir()
    (tmp_path / "custom_components").symlink_to(root / "custom_components")
    subprocess.run(
        [
            "/bin/bash",
            "-c",
            """
            uv() {
                "$TEST_PYTHON" -c '
from aerial_danger import DangerDetector
import custom_components.aerial_danger
'
            }
            export -f uv
            bash scripts/develop
            """,
        ],
        cwd=tmp_path,
        env={**os.environ, "PYTHONPATH": "", "TEST_PYTHON": sys.executable},
        check=True,
        capture_output=True,
        text=True,
    )
