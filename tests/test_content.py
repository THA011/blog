"""Tests for frontmatter parsing and content loading."""

import pytest

from src.generator.config import load_config
from src.generator.content import (
    load_posts,
    parse_frontmatter,
    render_markdown,
)


def test_parse_frontmatter_splits_meta_and_body():
    meta, body = parse_frontmatter("---\ntitle: Hi\ncategory: web\n---\nHello world")
    assert meta == {"title": "Hi", "category": "web"}
    assert body == "Hello world"


def test_parse_frontmatter_without_fence():
    meta, body = parse_frontmatter("no frontmatter here")
    assert meta == {}
    assert body == "no frontmatter here"


def test_parse_frontmatter_unclosed_raises():
    with pytest.raises(ValueError):
        parse_frontmatter("---\ntitle: Hi\nbody with no close")


def test_render_markdown_produces_html():
    html = render_markdown("# Heading\n\nSome **bold** text.")
    assert "<h1>Heading</h1>" in html
    assert "<strong>bold</strong>" in html


def test_load_posts_count_and_order(project_root):
    cfg = load_config(project_root / "config.yaml")
    posts = load_posts(project_root / "content" / "posts", cfg)
    assert len(posts) == 7
    # Sorted newest-first by date.
    dates = [p.date for p in posts]
    assert dates == sorted(dates, reverse=True)


def test_posts_resolve_category_metadata(project_root):
    cfg = load_config(project_root / "config.yaml")
    posts = load_posts(project_root / "content" / "posts", cfg)
    for post in posts:
        assert post.category in cfg.category_map
        assert post.category_label
        assert post.url.startswith("posts/")


def test_bad_category_raises(tmp_path, project_root):
    cfg = load_config(project_root / "config.yaml")
    (tmp_path / "x.md").write_text(
        "---\ntitle: X\ncategory: bogus\ndescription: d\nread_time: 1 min\n---\nBody",
        encoding="utf-8",
    )
    from src.generator.content import load_post

    with pytest.raises(ValueError):
        load_post(tmp_path / "x.md", cfg)
