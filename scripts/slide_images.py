#!/usr/bin/env python3
"""Resolve slide images from HWP/PDF bindata."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "templates" / "extracted"

MIN_WIDTH = 480
MIN_HEIGHT = 320


@dataclass
class SlideImageSpec:
    slide_id: str
    alt: str
    bindata: str
    layout: Literal["split", "band", "hero"] = "split"
    content_class: Literal["photo", "diagram", "chart", "screenshot"] = "photo"


@dataclass
class ResolvedImage:
    slide_id: str
    alt: str
    rel_path: str
    abs_path: Path
    width: int
    height: int


def bindata_dir(stem: str) -> Path:
    return EXTRACTED / f"{stem}-hwp-full" / "bindata"


def _rel_from_root(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def html_src(resolved: ResolvedImage) -> str:
    return "../" + resolved.rel_path


def resolve_bindata(stem: str, filename: str) -> Path | None:
    path = bindata_dir(stem) / filename
    if path.exists():
        return path
    bd = bindata_dir(stem)
    if not bd.exists():
        return None
    for p in bd.iterdir():
        if p.name.lower() == filename.lower():
            return p
    return None


def resolve_spec(
    stem: str,
    spec: SlideImageSpec,
    used_bindata: set[str],
) -> ResolvedImage | None:
    bd = resolve_bindata(stem, spec.bindata)
    if not bd or bd.name in used_bindata:
        return None

    try:
        with Image.open(bd) as im:
            w, h = im.size
    except Exception:
        return None

    if w < MIN_WIDTH // 2 or h < MIN_HEIGHT // 2:
        return None

    used_bindata.add(bd.name)
    return ResolvedImage(
        slide_id=spec.slide_id,
        alt=spec.alt,
        rel_path=_rel_from_root(bd),
        abs_path=bd,
        width=w,
        height=h,
    )


def resolve_all(stem: str, specs: list[SlideImageSpec]) -> dict[str, ResolvedImage]:
    used_bindata: set[str] = set()
    resolved: dict[str, ResolvedImage] = {}
    for spec in specs:
        img = resolve_spec(stem, spec, used_bindata)
        if img:
            resolved[spec.slide_id] = img
    return resolved


SCIEN_IMAGE_SPECS: list[SlideImageSpec] = [
    SlideImageSpec("background", "건설업 디지털 전환", "BIN0006.jpeg"),
    SlideImageSpec("platform", "디지털 트윈 아키텍처", "BIN0001.jpeg", content_class="diagram"),
    SlideImageSpec("method", "Two-Track 학습", "BIN0018.jpeg", content_class="diagram"),
    SlideImageSpec("org_partners", "Point Cloud 지형", "BIN0023.jpeg"),
]
