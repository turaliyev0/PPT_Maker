#!/usr/bin/env python3
"""Extract text AND images from a PDF (HWP export or similar)."""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

import fitz


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if pdf_path is None:
        print("Usage: python scripts/extract_pdf.py <file.pdf>")
        sys.exit(1)
    if not pdf_path.is_absolute():
        pdf_path = root / pdf_path
    stem = pdf_path.stem
    out_dir = root / "templates" / "extracted"
    out_dir.mkdir(parents=True, exist_ok=True)

    full_dir = out_dir / f"{stem}-hwp-full"
    if full_dir.exists():
        shutil.rmtree(full_dir)
    bindata_dir = full_dir / "bindata"
    bindata_dir.mkdir(parents=True)

    text_path = out_dir / f"{stem}-hwp-from-html.txt"
    figures_path = out_dir / f"{stem}-figures.json"

    doc = fitz.open(str(pdf_path))
    text_parts: list[str] = []
    img_counter = 0
    figures: list[dict] = []
    caption_re = re.compile(r"그림\s*(\d+)\.\s*(.+?)(?=\n|$)")

    for page_num in range(doc.page_count):
        page = doc[page_num]
        page_text = page.get_text()
        if page_text.strip():
            text_parts.append(page_text)

        for img_info in page.get_images(full=True):
            xref = img_info[0]
            try:
                base = doc.extract_image(xref)
            except Exception:
                continue
            if not base or not base.get("image"):
                continue
            ext = base.get("ext", "png")
            if ext == "jpeg":
                ext = "jpeg"
            img_counter += 1
            fname = f"BIN{img_counter:04d}.{ext}"
            (bindata_dir / fname).write_bytes(base["image"])

    doc.close()

    text = "\n\n".join(text_parts)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    text_path.write_text(text, encoding="utf-8")

    # Map figure captions (from text order) to extracted images (document order)
    captions = caption_re.findall(text)
    for num_s, cap in captions:
        idx = int(num_s) - 1
        if 0 <= idx < img_counter:
            fname = sorted(bindata_dir.iterdir())[idx].name if bindata_dir.exists() else f"BIN{idx + 1:04d}.png"
            files = sorted(bindata_dir.iterdir())
            if idx < len(files):
                rel = files[idx].relative_to(root).as_posix()
                figures.append(
                    {
                        "num": int(num_s),
                        "caption": cap.strip(),
                        "path": rel,
                    }
                )

    figures_path.write_text(json.dumps(figures, ensure_ascii=False, indent=2), encoding="utf-8")

    bindata_count = len(list(bindata_dir.glob("*"))) if bindata_dir.exists() else 0
    print(f"Wrote {full_dir} ({bindata_count} images)")
    print(f"Wrote {text_path} ({len(text)} chars)")
    print(f"Wrote {figures_path} ({len(figures)} figure mappings)")


if __name__ == "__main__":
    main()
