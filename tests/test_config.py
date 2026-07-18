"""Tests for the config loader."""

import pytest

from src.generator.config import load_config


def test_loads_required_sections(project_root):
    cfg = load_config(project_root / "config.yaml")
    assert cfg.site["name"] == "Mwatha Maina"
    assert cfg.nav
    assert cfg.categories
    assert cfg.services
    assert cfg.process


def test_category_lookup(project_root):
    cfg = load_config(project_root / "config.yaml")
    assert cfg.category_label("copywriting") == "Copywriting"
    assert cfg.category_css("web") == "web"
    with pytest.raises(KeyError):
        cfg.category_label("nonexistent")


def test_first_service_is_core(project_root):
    cfg = load_config(project_root / "config.yaml")
    assert cfg.services[0]["core"] is True


def test_missing_config_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nope.yaml")


def test_missing_keys_raises(tmp_path):
    (tmp_path / "bad.yaml").write_text("site: {name: x}\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_config(tmp_path / "bad.yaml")
