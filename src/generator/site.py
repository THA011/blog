"""Orchestrate a full build: config + content -> rendered static site.

This is the conductor. config.py and content.py do the reading, renderer.py does
the templating; here we wire them together in the right order and write the
finished pages out. Output lands at the repo root on purpose so GitHub Pages can
serve it with zero configuration.
"""

from __future__ import annotations

import logging
import shutil
from datetime import date
from pathlib import Path

from .config import SiteConfig, load_config
from .content import Page, Post, load_page, load_posts
from .renderer import Renderer

logger = logging.getLogger("blog.build")


class SiteBuilder:
    """Builds the static site from source into the output directory."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.src = self.root / "src"
        self.content = self.root / "content"
        self.output = self.root  # generated HTML sits at repo root for GitHub Pages
        self.renderer = Renderer(self.src / "templates")
        self.config: SiteConfig | None = None
        self.written: list[Path] = []

    # -- helpers ---------------------------------------------------------

    def _write(self, relpath: str, html: str) -> None:
        dest = self.output / relpath
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        self.written.append(dest)
        logger.info("wrote %s (%d bytes)", relpath, len(html))

    def _base_context(self, active: str, root_prefix: str) -> dict:
        # Everything every template needs, in one place. ``active`` highlights
        # the current nav link; ``root`` is "" at the root and "../" for posts
        # so links and asset paths resolve from either depth.
        assert self.config is not None
        return {
            "site": self.config.site,
            "nav": self.config.nav,
            "categories": self.config.categories,
            "active": active,
            "root": root_prefix,
            "year": date.today().year,
        }

    # -- build steps -----------------------------------------------------

    def copy_assets(self) -> None:
        # Ship src/assets verbatim to /assets. Wipe first so deleted or renamed
        # files never linger in the output from a previous build.
        src_assets = self.src / "assets"
        dest_assets = self.output / "assets"
        if dest_assets.exists():
            shutil.rmtree(dest_assets)
        shutil.copytree(src_assets, dest_assets)
        logger.info("copied assets -> %s", dest_assets.relative_to(self.root))

    def build_posts(self, posts: list[Post]) -> None:
        for post in posts:
            html = self.renderer.render(
                "post.html",
                post=post,
                page_title=f"{post.title} — {self.config.site['name']}",
                page_description=post.description,
                **self._base_context(active="blog", root_prefix="../"),
            )
            self._write(post.url, html)

    def build_blog(self, posts: list[Post]) -> None:
        html = self.renderer.render(
            "blog.html",
            posts=posts,
            page_title=f"Blog — {self.config.site['name']}",
            page_description=f"Marketing, copywriting, web and design articles by {self.config.site['name']}.",
            **self._base_context(active="blog", root_prefix=""),
        )
        self._write("blog.html", html)

    def build_home(self, posts: list[Post]) -> None:
        # Feature the exact posts named in config, in that order -- editorial
        # choice beats "newest three". Unknown slugs are skipped, not fatal.
        by_slug = {p.slug: p for p in posts}
        featured = [by_slug[s] for s in self.config.home.get("featured", []) if s in by_slug]
        html = self.renderer.render(
            "home.html",
            featured_posts=featured,
            page_title=f"{self.config.site['name']} — {self.config.site['tagline']}",
            **self._base_context(active="home", root_prefix=""),
        )
        self._write("index.html", html)

    def build_simple(self, template: str, out: str, active: str, title: str) -> None:
        html = self.renderer.render(
            template,
            page_title=f"{title} — {self.config.site['name']}",
            **self._base_context(active=active, root_prefix=""),
        )
        self._write(out, html)

    def build_page(self, page: Page, out: str, active: str) -> None:
        html = self.renderer.render(
            "page.html",
            page=page,
            page_title=f"{page.title} — {self.config.site['name']}",
            **self._base_context(active=active, root_prefix=""),
        )
        self._write(out, html)

    # -- entry point -----------------------------------------------------

    def build(self) -> list[Path]:
        # Load config first: if it's invalid we stop here, before writing a
        # single file, so a bad edit can't leave a half-updated site on disk.
        self.written = []
        self.config = load_config(self.root / "config.yaml")
        logger.info("loaded config for %s", self.config.site["name"])

        posts = load_posts(self.content / "posts", self.config)
        logger.info("loaded %d posts", len(posts))

        self.copy_assets()
        self.build_home(posts)
        self.build_blog(posts)
        self.build_posts(posts)
        self.build_simple("services.html", "services.html", "services", "Services")
        self.build_simple("contact.html", "contact.html", "contact", "Contact")

        about = load_page(self.content / "pages" / "about.md")
        self.build_page(about, "about.html", "about")

        logger.info("build complete: %d files", len(self.written))
        return self.written


def configure_logging(root: str | Path) -> None:
    logs = Path(root) / "logs"
    logs.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(logs / "build.log", encoding="utf-8"),
        ],
    )


def build_site(root: str | Path) -> list[Path]:
    return SiteBuilder(root).build()
