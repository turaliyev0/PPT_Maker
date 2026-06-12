#!/usr/bin/env python3
"""Build draft slides/*.html from parsed HWP slide_plan.

Scaffold only — the agent should redesign slides with creative layouts and
readable typography before converting to PPTX. Prefer writing to slides/_draft/.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from html_slides import build_all
from parse_hwp import parse_file


def main() -> None:
    slides_dir = ROOT / "slides"
    stem: str | None = None
    args = sys.argv[1:]
    for arg in args:
        p = Path(arg)
        if p.suffix.lower() == ".hwp":
            stem = p.stem
        elif p.is_dir() or not p.suffix:
            slides_dir = p if p.is_absolute() else ROOT / p

    if stem is None:
        print("Usage: python scripts/build_html_from_plan.py <file.hwp> [slides-dir]")
        sys.exit(1)

    text_path = ROOT / "templates" / "extracted" / f"{stem}-hwp-from-html.txt"
    if not text_path.exists():
        print(f"Missing {text_path}. Run: python scripts/extract_hwp_text.py {stem}.hwp")
        sys.exit(1)

    data = parse_file(text_path)
    files = build_all(data, slides_dir, stem=stem)
    print(f"Wrote {len(files)} HTML slides → {slides_dir}")
    print(f"Preview: {slides_dir / 'index.html'}")


if __name__ == "__main__":
    main()
