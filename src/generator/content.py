"""Parse Markdown content with YAML frontmatter into Page/Post objects.

Writing is the product here, so writing should be the easy part: every article
is a plain Markdown file with a small YAML header (title, category, date...).
Authors never touch HTML. This module reads those files, checks the header has
what we need, renders the body, and hands back tidy typed objects the templates
can trust.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import markdown
import yaml

from .config import SiteConfig

_FRONTMATTER_FENCE = "---"


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split ``text`` into (metadata dict, markdown body).

    A file may open with a YAML frontmatter block fenced by ``---`` lines.
    If no frontmatter is present, metadata is empty and the whole text is body.
    """

    lines = text.splitlines()
    if not lines or lines[0].strip() != _FRONTMATTER_FENCE:
        return {}, text

    for idx in range(1, len(lines)):
        if lines[idx].strip() == _FRONTMATTER_FENCE:
            meta = yaml.safe_load("\n".join(lines[1:idx])) or {}
            body = "\n".join(lines[idx + 1 :]).lstrip("\n")
            return meta, body

    raise ValueError("Frontmatter opening '---' has no closing '---'")


def render_markdown(body: str) -> str:
    # "extra" gives us tables, fenced code and footnotes; "sane_lists" stops
    # adjacent lists from bleeding into one another. Enough for prose, no more.
    return markdown.markdown(body, extensions=["extra", "sane_lists"])


@dataclass
class Page:
    """A standalone prose page (e.g. About). Simpler than a Post -- no category,
    no date, no callout, just a heading and rendered body."""

    slug: str
    title: str
    body: str  # rendered HTML
    eyebrow: str = ""
    heading: str = ""
    lead: str = ""


@dataclass
class Post:
    """A blog article. Carries both the content and the presentation metadata a
    card/article template needs, so templates stay logic-free."""

    slug: str
    title: str
    category: str
    category_label: str
    category_css: str
    description: str
    read_time: str
    date: str
    body: str  # rendered HTML
    callout_title: str = ""
    callout_text: str = ""
    callout_cta: str = "Start a project"

    @property
    def url(self) -> str:
        # Posts live one directory deep; templates prefix root="../" to match.
        return f"posts/{self.slug}.html"


def load_page(path: str | Path) -> Page:
    path = Path(path)
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    title = meta.get("title", path.stem.replace("-", " ").title())
    return Page(
        slug=path.stem,
        title=title,
        body=render_markdown(body),
        eyebrow=meta.get("eyebrow", ""),
        heading=meta.get("heading", ""),
        lead=meta.get("lead", ""),
    )


def load_post(path: str | Path, config: SiteConfig) -> Post:
    """Load a single post, validating it against the site's categories."""
    path = Path(path)
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))

    # These four earn a post its place on a card; without them it can't render
    # correctly, so refuse the build instead of shipping a broken tile.
    required = ("title", "category", "description", "read_time")
    missing = [k for k in required if k not in meta]
    if missing:
        raise ValueError(f"{path.name} is missing frontmatter keys: {', '.join(missing)}")

    slug = meta.get("slug", path.stem)
    category = meta["category"]
    if category not in config.category_map:
        raise ValueError(
            f"{path.name}: unknown category {category!r} (not in config.yaml categories)"
        )

    return Post(
        slug=slug,
        title=meta["title"],
        category=category,
        category_label=config.category_label(category),
        category_css=config.category_css(category),
        description=meta["description"],
        read_time=meta["read_time"],
        date=str(meta.get("date", "")),
        body=render_markdown(body),
        callout_title=meta.get("callout_title", ""),
        callout_text=meta.get("callout_text", ""),
        callout_cta=meta.get("callout_cta", "Start a project"),
    )


def load_posts(directory: str | Path, config: SiteConfig) -> list[Post]:
    """Load every ``*.md`` post, newest first (by ``date`` then slug)."""

    directory = Path(directory)
    posts = [load_post(p, config) for p in sorted(directory.glob("*.md"))]
    posts.sort(key=lambda p: (p.date, p.slug), reverse=True)
    return posts
