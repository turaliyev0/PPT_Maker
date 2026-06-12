#!/usr/bin/env python3
"""Extract text AND images from an HWP file."""
from __future__ import annotations

import logging
import re
import shutil
import sys
import warnings
from contextlib import closing
from pathlib import Path

from hwp5.hwp5html import HTMLTransform
from hwp5.xmlmodel import Hwp5File


def strip_html(html: str) -> str:
    html = re.sub(r"(?i)<br\s*/?>", "\n", html)
    html = re.sub(r"(?i)</p>", "\n", html)
    html = re.sub(r"(?i)</tr>", "\n", html)
    html = re.sub(r"(?i)</td>", " ", html)
    text = re.sub(r"<[^>]+>", "", html)
    text = text.replace("&#13;", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    hwp_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if hwp_path is None:
        print("Usage: python scripts/extract_hwp_text.py <file.hwp>")
        sys.exit(1)
    if not hwp_path.is_absolute():
        hwp_path = root / hwp_path
    stem = hwp_path.stem
    out_dir = root / "templates" / "extracted"
    out_dir.mkdir(parents=True, exist_ok=True)

    full_dir = out_dir / f"{stem}-hwp-full"
    if full_dir.exists():
        shutil.rmtree(full_dir)
    full_dir.mkdir(parents=True)

    text_path = out_dir / f"{stem}-hwp-from-html.txt"
    figures_path = out_dir / f"{stem}-figures.json"

    warnings.filterwarnings("ignore")
    logging.disable(logging.CRITICAL)

    with closing(Hwp5File(str(hwp_path))) as hwp5file:
        HTMLTransform().transform_hwp5_to_dir(hwp5file, str(full_dir))

    html_path = full_dir / "index.xhtml"
    html = html_path.read_text(encoding="utf-8", errors="replace")
    text = strip_html(html)
    text_path.write_text(text, encoding="utf-8")

    # Map figure captions (from text) to bindata image paths (from HTML order)
    import json

    img_srcs = re.findall(r'<img[^>]+src="([^"]+)"', html)
    captions = re.findall(r"그림\s*(\d+)\.\s*(.+?)(?=\n)", text)
    figures = []
    for num_s, cap in captions:
        idx = int(num_s) - 1
        if 0 <= idx < len(img_srcs):
            rel = img_srcs[idx].replace("/", "\\")
            img_path = full_dir / rel
            if img_path.exists():
                figures.append(
                    {
                        "num": int(num_s),
                        "caption": cap.strip(),
                        "path": str(img_path.relative_to(root)).replace("\\", "/"),
                    }
                )

    figures_path.write_text(json.dumps(figures, ensure_ascii=False, indent=2), encoding="utf-8")

    bindata_count = len(list((full_dir / "bindata").glob("*"))) if (full_dir / "bindata").exists() else 0
    print(f"Wrote {full_dir} (html + {bindata_count} images)")
    print(f"Wrote {text_path} ({len(text)} chars)")
    print(f"Wrote {figures_path} ({len(figures)} figure mappings)")


if __name__ == "__main__":
    main()
