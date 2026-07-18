"""Shared pytest fixtures."""

import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def project_root() -> Path:
    return ROOT


@pytest.fixture
def built_site(tmp_path: Path) -> Path:
    """Copy source into an isolated dir and build the site there.

    Keeps tests from mutating the real repo output.
    """
    for item in ("config.yaml", "src", "content"):
        source = ROOT / item
        dest = tmp_path / item
        if source.is_dir():
            shutil.copytree(source, dest)
        else:
            shutil.copy2(source, dest)

    from src.generator.site import build_site

    build_site(tmp_path)
    return tmp_path
