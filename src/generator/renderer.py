"""Thin wrapper around the Jinja2 environment used to render pages.

One place owns the templating config so every page is built the same way -- most
importantly with autoescaping on, so any text coming from Markdown or config
can't accidentally inject HTML.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape


class Renderer:
    """Loads templates from ``templates_dir`` and renders them with a context."""

    def __init__(self, templates_dir: str | Path) -> None:
        self.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
            # trim/lstrip keep the generated HTML clean despite readable,
            # heavily-indented template source -- no stray blank lines.
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template: str, **context: Any) -> str:
        return self.env.get_template(template).render(**context)
