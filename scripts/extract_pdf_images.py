#!/usr/bin/env python3
"""Extract embedded images from a PDF into a dedicated folder."""
from __future__ import annotations

import io
import sys
from pathlib import Path

import fitz
import numpy as np
from PIL import Image


def is_decorative_junk(data: bytes) -> bool:
    """Skip thin lines, bullet icons, and flat placeholder shapes."""
    try:
        with Image.open(io.BytesIO(data)) as im:
            im = im.convert("RGB")
            w, h = im.size
            ar = w / h if h else 999
            area = w * h
            size = len(data)
            arr = np.array(im)
            std = float(arr.std())
            flat = arr.reshape(-1, 3)
            if len(flat) > 50000:
                flat = flat[:: max(1, len(flat) // 50000)]
            uniq = len({tuple(p) for p in flat})
    except Exception:
        return False

    if min(w, h) < 24:
        return True
    if ar > 8 or ar < 0.125:
        return True
    if area < 4000:
        return True
    if std < 15 and uniq < 100:
        return True
    if size < 2500 and area < 120000:
        return True
    if uniq < 50 and std < 45 and area > 10000:
        return True
    return False


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    keep_all = "--keep-all" in sys.argv

    pdf_path = Path(args[0]) if args else None
    if pdf_path is None:
        print("Usage: python scripts/extract_pdf_images.py <file.pdf> [output_dir] [--keep-all]")
        sys.exit(1)
    if not pdf_path.is_absolute():
        pdf_path = root / pdf_path

    if len(args) > 1:
        out_dir = Path(args[1])
        if not out_dir.is_absolute():
            out_dir = root / out_dir
    else:
        out_dir = root / f"{pdf_path.stem}-images"

    out_dir.mkdir(parents=True, exist_ok=True)
    removed_dir = out_dir / "_removed"

    doc = fitz.open(str(pdf_path))
    page_count = doc.page_count
    seen_xrefs: set[int] = set()
    saved = 0
    skipped = 0

    for page_num in range(page_count):
        page = doc[page_num]
        page_imgs = 0
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            if xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)
            try:
                base = doc.extract_image(xref)
            except Exception:
                continue
            if not base or not base.get("image"):
                continue
            ext = base.get("ext", "png")
            if ext == "jpg":
                ext = "jpeg"
            raw = base["image"]
            page_imgs += 1
            seq = saved + skipped + 1
            fname = f"page{page_num + 1:03d}_img{page_imgs:02d}_{seq:04d}.{ext}"

            if not keep_all and is_decorative_junk(raw):
                skipped += 1
                removed_dir.mkdir(exist_ok=True)
                (removed_dir / fname).write_bytes(raw)
                continue

            saved += 1
            (out_dir / fname).write_bytes(raw)

    doc.close()

    print(f"PDF: {pdf_path.name} ({page_count} pages)")
    print(f"Saved {saved} images to {out_dir}")
    if skipped:
        print(f"Skipped {skipped} decorative images -> {removed_dir}")


if __name__ == "__main__":
    main()
