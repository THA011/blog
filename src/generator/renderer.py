"""Thin wrapper around the Jinja2 environment used to render pages."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape


class Renderer:
    def __init__(self, templates_dir: str | Path) -> None:
        self.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template: str, **context: Any) -> str:
        return self.env.get_template(template).render(**context)
