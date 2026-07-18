"""Load and validate the site configuration (``config.yaml``).

config.yaml is the single source of truth for the whole site: change a service,
rename the brand or add a category there and every page follows. This module's
job is small but important -- turn that YAML into typed objects and fail loudly,
with a helpful message, the moment something is missing. A broken config should
never produce a half-built site.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Category:
    """A blog category.

    ``slug`` is the internal id (matched against each post's frontmatter),
    ``label`` is what readers see, and ``css`` picks the coloured tag style in
    styles.css (empty means the default brand colour).
    """

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
        """Slug -> Category, for O(1) lookups while rendering posts."""
        return {c.slug: c for c in self.categories}

    def category_label(self, slug: str) -> str:
        # A missing label means a post references a category that doesn't exist.
        # That's an authoring mistake, so raise rather than silently guess.
        cat = self.category_map.get(slug)
        if cat is None:
            raise KeyError(f"Unknown category slug: {slug!r}")
        return cat.label

    def category_css(self, slug: str) -> str:
        # CSS class is cosmetic, so an unknown slug just falls back to default.
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

    # Fold home/services/process into the site dict so every template can reach
    # them as site.home etc. without us threading them through each render call.
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
