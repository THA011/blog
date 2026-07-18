"""Load and validate the site configuration (config.yaml)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Category:
    slug: str
    label: str
    css: str = ""


@dataclass
class SiteConfig:
    """Parsed, validated view of config.yaml."""

    site: dict[str, Any]
    nav: list[dict[str, Any]]
    categories: list[Category]
    services: list[dict[str, Any]]
    process: list[dict[str, Any]]
    home: dict[str, Any]
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def category_map(self) -> dict[str, Category]:
        return {c.slug: c for c in self.categories}

    def category_label(self, slug: str) -> str:
        cat = self.category_map.get(slug)
        if cat is None:
            raise KeyError(f"Unknown category slug: {slug!r}")
        return cat.label

    def category_css(self, slug: str) -> str:
        cat = self.category_map.get(slug)
        return cat.css if cat else ""


REQUIRED_TOP_LEVEL = ("site", "nav", "categories", "services", "process", "home")


def load_config(path: str | Path) -> SiteConfig:
    """Read config.yaml and return a validated :class:`SiteConfig`."""

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    missing = [key for key in REQUIRED_TOP_LEVEL if key not in data]
    if missing:
        raise ValueError(f"config.yaml is missing required keys: {', '.join(missing)}")

    # Fold home config into the site dict so templates can reach it as site.home.
    site = dict(data["site"])
    site["home"] = data["home"]
    site["services"] = data["services"]
    site["process"] = data["process"]

    categories = [Category(**c) for c in data["categories"]]

    return SiteConfig(
        site=site,
        nav=data["nav"],
        categories=categories,
        services=data["services"],
        process=data["process"],
        home=data["home"],
        raw=data,
    )
