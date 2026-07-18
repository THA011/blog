#!/usr/bin/env python3
"""Entry point for building the static blog.

Usage:
    python build.py

Reads config.yaml + content/, renders src/templates/ with the generator in
src/generator/, and writes the finished HTML (plus assets/) to the repo root so
it can be served directly by GitHub Pages or any static host.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.generator.site import build_site, configure_logging  # noqa: E402


def main() -> int:
    configure_logging(ROOT)
    written = build_site(ROOT)
    print(f"\nBuilt {len(written)} files. Serve with: python -m http.server 8000")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
