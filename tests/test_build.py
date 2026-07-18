"""End-to-end build tests: output files, counts, and link integrity."""

import re
from pathlib import Path

EXPECTED_PAGES = [
    "index.html",
    "blog.html",
    "services.html",
    "about.html",
    "contact.html",
    "assets/css/styles.css",
    "assets/js/main.js",
]

LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')


def test_all_pages_written(built_site: Path):
    for rel in EXPECTED_PAGES:
        assert (built_site / rel).exists(), f"missing {rel}"
    assert len(list((built_site / "posts").glob("*.html"))) == 7


def test_blog_lists_all_seven_posts(built_site: Path):
    html = (built_site / "blog.html").read_text(encoding="utf-8")
    assert html.count('class="card post-card"') == 7


def test_blog_category_counts(built_site: Path):
    html = (built_site / "blog.html").read_text(encoding="utf-8")
    assert html.count('data-category="copywriting"') == 2
    assert html.count('data-category="academic"') == 2
    assert html.count('data-category="web"') == 1
    assert html.count('data-category="graphic"') == 1
    assert html.count('data-category="freelancing"') == 1


def test_home_features_three_posts(built_site: Path):
    html = (built_site / "index.html").read_text(encoding="utf-8")
    assert html.count('class="card post-card"') == 3


def test_services_marks_core_service(built_site: Path):
    html = (built_site / "services.html").read_text(encoding="utf-8")
    assert "Core service" in html


def test_contact_form_present(built_site: Path):
    html = (built_site / "contact.html").read_text(encoding="utf-8")
    assert 'id="contact-form"' in html


def test_no_broken_local_links(built_site: Path):
    html_files = list(built_site.glob("*.html")) + list((built_site / "posts").glob("*.html"))
    broken = []
    for f in html_files:
        for link in LINK_RE.findall(f.read_text(encoding="utf-8")):
            if link.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            target = (f.parent / link).resolve()
            if not target.exists():
                broken.append(f"{f.name} -> {link}")
    assert not broken, f"broken links: {broken}"
