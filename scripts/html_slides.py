#!/usr/bin/env python3
"""Scaffold slide_plan entries as HTML drafts (1280×720).

Not final deck output — the agent should redesign slides with larger type,
varied layouts, and no duplicate HWP images. This script helps extract
content and reasonable defaults only.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

from parse_hwp import (
    EXTRACTED,
    HwpData,
    INTL_EVIDENCE_FIGURES,
    ORG_PHOTO_FIGURE,
    PRIOR_RD_FIGURE,
    SlidePlan,
)

ROOT = Path(__file__).resolve().parents[1]

BASE_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1280px; height: 720px;
  font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
  background: #fff; color: #2D2D2D;
  padding: 36px 44px; overflow: hidden;
}
body.cover, body.closing {
  background: #1F4E79; color: #fff;
  display: flex; flex-direction: column; justify-content: center;
}
body.cover.has-hero { position: relative; }
body.cover.has-hero .hero-bg {
  position: absolute; inset: 0; opacity: 0.18; object-fit: cover; width: 100%; height: 100%;
}
body.cover.has-hero .cover-inner { position: relative; z-index: 1; }
.section { font-size: 15px; color: #6b7280; margin-bottom: 10px; }
.action-title {
  font-size: 32px; font-weight: 800; color: #1F4E79;
  margin-bottom: 20px; line-height: 1.3;
}
body.cover .action-title, body.closing .action-title { display: none; }
.cover h1 { font-size: 42px; font-weight: 800; margin-bottom: 16px; line-height: 1.25; }
.cover .meta, .closing .meta { font-size: 18px; color: #A0BBDD; line-height: 1.6; }
.closing h1 { font-size: 48px; text-align: center; margin-bottom: 20px; }
.closing .meta { text-align: center; }
ul { padding-left: 1.25em; font-size: 17px; line-height: 1.5; }
li { margin-bottom: 8px; }
.content { max-height: 560px; overflow: hidden; }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
th { background: #E8EFF5; color: #1F4E79; text-align: left; padding: 8px 10px; font-weight: 700; }
td { padding: 8px 10px; border-bottom: 1px solid #E8E8E8; vertical-align: top; }
.two-col { display: flex; gap: 18px; align-items: flex-start; }
.two-col .col { flex: 1; min-width: 0; }
.photo { width: 220px; flex-shrink: 0; }
.photo img { width: 100%; max-height: 280px; object-fit: cover; border-radius: 4px; }
.photo-lg { width: 280px; flex-shrink: 0; }
.photo-lg img { width: 100%; max-height: 340px; object-fit: cover; border-radius: 4px; }
.placeholder {
  width: 100%; height: 200px; background: #F5F5F5; border: 1px dashed #CCC;
  display: flex; align-items: center; justify-content: center;
  color: #777; font-size: 12px; border-radius: 4px;
}
.panels { display: flex; gap: 14px; }
.panel { flex: 1; }
.panel img { width: 100%; max-height: 500px; object-fit: contain; }
.visual-split { display: flex; gap: 18px; align-items: flex-start; }
.visual-split .visual { flex: 0 0 46%; }
.visual-split .visual img { width: 100%; max-height: 500px; object-fit: contain; border-radius: 4px; }
.visual-split .text { flex: 1; min-width: 0; }
.visual-dual .visual-row { display: flex; gap: 12px; margin-bottom: 12px; }
.visual-dual .visual-row .panel img { max-height: 260px; }
.bar-chart .bar-row { display: flex; align-items: center; margin: 8px 0; font-size: 15px; }
.bar-chart .bar-label { width: 32%; padding-right: 8px; line-height: 1.2; }
.bar-chart .bar-track { flex: 1; height: 20px; background: #E8EFF5; border-radius: 4px; overflow: hidden; }
.bar-chart .bar-fill { height: 100%; background: linear-gradient(90deg, #1F4E79, #3A7AB8); border-radius: 4px; }
.bar-chart .bar-val { width: 14%; text-align: right; font-size: 14px; color: #555; padding-left: 6px; }
.timeline { display: flex; gap: 10px; }
.timeline .year {
  flex: 1; background: #E8EFF5; border-radius: 8px; padding: 12px;
  font-size: 14px; line-height: 1.4; border-top: 4px solid #1F4E79;
}
.timeline .year strong { display: block; color: #1F4E79; margin-bottom: 6px; font-size: 16px; }
.budget-stack { margin-top: 8px; }
.budget-stack .yr { margin-bottom: 12px; }
.budget-stack .yr-label { font-size: 15px; font-weight: 700; color: #1F4E79; margin-bottom: 4px; }
.budget-stack .yr-bar { display: flex; height: 26px; border-radius: 4px; overflow: hidden; font-size: 13px; color: #fff; }
.budget-stack .gov { background: #1F4E79; display: flex; align-items: center; padding: 0 6px; }
.budget-stack .priv { background: #7BA7D7; display: flex; align-items: center; padding: 0 6px; }
.patent-cards { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.patent-card {
  flex: 1 1 45%; background: #F5F8FB; border-left: 4px solid #1F4E79;
  padding: 10px 12px; font-size: 14px; line-height: 1.35;
}
.patent-card .status { color: #1F4E79; font-weight: 700; font-size: 13px; }
.toc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 24px; font-size: 16px; }
.toc-grid .item { padding: 5px 0; border-bottom: 1px solid #EEE; }
.toc-with-thumb { display: flex; gap: 20px; }
.toc-with-thumb .thumb { flex: 0 0 38%; }
.toc-with-thumb .thumb img { width: 100%; max-height: 480px; object-fit: contain; }
.subhead { font-size: 16px; font-weight: 700; margin: 12px 0 6px; color: #2D2D2D; }
.pi { font-size: 20px; font-weight: 700; color: #1F4E79; margin-bottom: 10px; }
"""

def _claim_figures(used: set[int], nums: list[int]) -> None:
    used.update(n for n in nums if n is not None)

# Caption keyword routing (visual-design.md)
KIND_FIGURE_KEYWORDS: dict[str, list[str]] = {
    "background": ["차별", "배경", "필요", "로드맵", "개념"],
    "goals": ["로드맵", "목표", "냉각", "AI", "구성"],
    "method": ["구성", "설계", "알고리즘", "모듈", "아키텍처", "열교환", "순환"],
    "org_intro": ["설비", "인프라", "인증", "장비", "시설", "자격"],
    "commercialization": ["사업화", "로드맵", "제품화", "패키지"],
    "commercialization_strategy": ["시장", "로봇", "제품화", "성장"],
    "impact": ["기대효과", "효과", "절감"],
    "roles": ["추진체계", "체계도", "체계"],
    "schedule": ["추진체계", "체계도", "일정", "체계"],
    "intl_base": ["협력", "수상", "ranking", "전경"],
    "toc": ["추진체계", "체계도", "로드맵"],
}

ORG_EXECUTION_KEYWORDS: dict[str, list[str]] = {
    "㈜경안써머텍": ["열교환", "액침", "모듈", "유체", "쉘", "설계"],
    "인하대학교": ["CFD", "디지털", "트윈", "해석", "열"],
    "한국화학융합시험연구원": ["시험", "검증", "완료", "열성능"],
    "중경우전대학교": ["용접", "로봇", "자동화", "원주"],
}

INTL_FIGURE_KEYWORDS = ["전경", "협력", "계약", "ranking", "국제"]


def _esc(text: str) -> str:
    return html.escape(str(text or ""), quote=True)


def _load_figure_captions(stem: str = "input") -> dict[int, str]:
    path = EXTRACTED / f"{stem}-figures.json"
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {int(f["num"]): f.get("caption", "") for f in raw if f.get("num")}


def _org_from_header(data: HwpData, header: str):
    for org in data.orgs:
        if org.name in header:
            return org
    return None


def _history_bullets(history: list[str]) -> list[str]:
    return [h.lstrip("•· ").strip() for h in history if h.strip()]


def _execution_bullets(org) -> list[str]:
    lines: list[str] = []
    for title, bullets in org.execution:
        if bullets:
            for b in bullets:
                if b.strip():
                    lines.append(b.strip())
        elif title.strip() and title != org.name:
            lines.append(title.strip())
    return lines


def _first_execution_bullet(org) -> str:
    for _title, bullets in org.execution:
        for b in bullets:
            if b.strip():
                return b.strip()
        if _title.strip() and _title != org.name:
            return _title.strip()
    return ""


def _flatten_background(items: list[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        if item.startswith("  "):
            if out:
                out[-1] = f"{out[-1]} — {item.strip()}"
            else:
                out.append(item.strip())
        else:
            out.append(item.strip())
    return [x for x in out if x]


def _bullets_html(items: list[str], limit: int = 4) -> str:
    items = [i for i in items if i and str(i).strip()][:limit]
    if not items:
        return ""
    return "<ul>" + "".join(f"<li>{_esc(i)}</li>" for i in items) + "</ul>"


def _table_html(headers: list[str], rows: list[tuple], col_widths: list[str] | None = None) -> str:
    if not rows:
        return ""
    cw = col_widths or []
    head = "<tr>" + "".join(
        f'<th style="{f"width:{cw[i]}" if i < len(cw) else ""}">{_esc(h)}</th>' for i, h in enumerate(headers)
    ) + "</tr>"
    body = ""
    for row in rows:
        body += "<tr>" + "".join(f"<td>{_esc(c)}</td>" for c in row) + "</tr>"
    return f"<table><thead>{head}</thead><tbody>{body}</tbody></table>"


def os_relpath(target: Path, start: Path) -> str:
    import os

    return os.path.relpath(target, start)


def _fig_src(figures: dict, num: int | None, slides_dir: Path) -> str | None:
    if num is None:
        return None
    rel = figures.get(num) or figures.get(str(num))
    if not rel:
        return None
    p = (ROOT / rel).resolve()
    if not p.exists():
        return None
    return Path(os_relpath(p, slides_dir)).as_posix()


def _img_tag(figures: dict, num: int, slides_dir: Path, alt: str) -> str:
    src = _fig_src(figures, num, slides_dir)
    if src:
        return f'<img src="{_esc(src)}" alt="{_esc(alt)}">'
    return ""


def _img_or_placeholder(figures: dict, num: int | None, slides_dir: Path, caption: str, css_class: str = "photo") -> str:
    src = _fig_src(figures, num, slides_dir)
    if src:
        return f'<div class="{css_class}"><img src="{_esc(src)}" alt="{_esc(caption)}"></div>'
    return f'<div class="{css_class}"><div class="placeholder">{_esc(caption)}</div></div>'


def _match_figures(
    kind: str,
    captions: dict[int, str],
    figures: dict,
    org_name: str | None = None,
    limit: int = 2,
    exclude: set[int] | None = None,
) -> list[int]:
    exclude = exclude or set()
    keywords = list(KIND_FIGURE_KEYWORDS.get(kind, []))
    if kind == "execution" and org_name:
        keywords = ORG_EXECUTION_KEYWORDS.get(org_name, keywords)
    if kind == "intl_evidence":
        keywords = INTL_FIGURE_KEYWORDS + [str(n) for n in INTL_EVIDENCE_FIGURES]

    matched: list[int] = []
    for num, cap in sorted(captions.items()):
        if num in exclude or num not in figures:
            continue
        cap_l = cap.lower()
        if any(kw.lower() in cap_l or kw in cap for kw in keywords):
            matched.append(num)
        if len(matched) >= limit:
            break

    if not matched and kind == "intl_evidence":
        for n in INTL_EVIDENCE_FIGURES:
            if n in figures and n not in exclude:
                matched.append(n)
    return matched[:limit]


def _visual_split(fig_nums: list[int], text_html: str, figures: dict, slides_dir: Path, alt: str = "HWP 그림") -> str:
    imgs = "".join(
        f'<div class="visual">{_img_tag(figures, n, slides_dir, alt)}</div>'
        for n in fig_nums[:1]
        if _fig_src(figures, n, slides_dir)
    )
    if not imgs:
        return text_html
    return f'<div class="visual-split">{imgs}<div class="text">{text_html}</div></div>'


def _visual_dual(fig_nums: list[int], bottom_html: str, figures: dict, slides_dir: Path, alt: str = "HWP 그림") -> str:
    panels = "".join(
        f'<div class="panel">{_img_tag(figures, n, slides_dir, alt)}</div>'
        for n in fig_nums[:2]
        if _fig_src(figures, n, slides_dir)
    )
    if not panels:
        return bottom_html
    return f'<div class="visual-dual"><div class="visual-row">{panels}</div>{bottom_html}</div>'


def _parse_numeric(val: str) -> float:
    m = re.search(r"[\d,]+(?:\.\d+)?", str(val).replace(",", ""))
    return float(m.group().replace(",", "")) if m else 0.0


def _bar_chart_html(rows: list[tuple], label_idx: int = 0, value_idx: int = 2) -> str:
    if not rows:
        return ""
    values = [_parse_numeric(r[value_idx]) for r in rows if len(r) > value_idx]
    max_v = max(values) if values else 1.0
    if max_v <= 0:
        max_v = 1.0
    bars = []
    for row in rows[:6]:
        if len(row) <= value_idx:
            continue
        label = row[label_idx]
        val = _parse_numeric(row[value_idx])
        pct = min(100, int((val / max_v) * 100)) if val else 5
        bars.append(
            f'<div class="bar-row"><div class="bar-label">{_esc(label)}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>'
            f'<div class="bar-val">{_esc(row[value_idx])}</div></div>'
        )
    return f'<div class="bar-chart">{"".join(bars)}</div>'


def _timeline_html(rows: list[tuple]) -> str:
    if not rows:
        return ""
    blocks = []
    for year, content in rows[:4]:
        short = content[:120] + ("…" if len(content) > 120 else "")
        blocks.append(f'<div class="year"><strong>{_esc(year)}</strong>{_esc(short)}</div>')
    return f'<div class="timeline">{"".join(blocks)}</div>'


def _budget_stack_html(rows: list[tuple]) -> str:
    if not rows:
        return ""
    totals = [_parse_numeric(r[3]) for r in rows if len(r) > 3]
    max_t = max(totals) if totals else 1.0
    parts = []
    for row in rows:
        if len(row) < 4:
            continue
        gov = _parse_numeric(row[1])
        priv = _parse_numeric(row[3]) - gov if _parse_numeric(row[3]) > gov else _parse_numeric(row[2]) if len(row) > 2 else 0
        total = gov + priv if (gov + priv) > 0 else _parse_numeric(row[3])
        scale = (total / max_t * 100) if max_t else 50
        gov_pct = (gov / total * scale) if total else scale / 2
        priv_pct = scale - gov_pct
        parts.append(
            f'<div class="yr"><div class="yr-label">{_esc(row[0])}</div>'
            f'<div class="yr-bar" style="width:{scale}%">'
            f'<div class="gov" style="width:{gov_pct}%">{_esc(row[1])}</div>'
            f'<div class="priv" style="width:{priv_pct}%">{_esc(row[2] if len(row) > 2 else "")}</div>'
            f"</div></div>"
        )
    return f'<div class="budget-stack">{"".join(parts)}</div>'


def _patent_cards_html(patents) -> str:
    if not patents:
        return '<p style="font-size:11px;color:#777">해당 없음 (HWP 기재)</p>'
    cards = []
    for p in patents[:4]:
        cards.append(
            f'<div class="patent-card"><div class="status">{_esc(p.status)} · {_esc(p.country)}</div>'
            f"{_esc(p.name)}</div>"
        )
    return f'<div class="patent-cards">{"".join(cards)}</div>'


def _header_block(sp: SlidePlan) -> str:
    if sp.kind in ("cover", "closing"):
        return ""
    return f'<div class="section">{_esc(sp.num)} · {_esc(sp.header)}</div><div class="action-title">{_esc(sp.action_title)}</div>'


def _wrap(body_class: str, inner: str) -> str:
    cls = f' class="{body_class}"' if body_class else ""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>{BASE_CSS}</style>
</head>
<body{cls}>
{inner}
</body>
</html>
"""


def render_slide(
    sp: SlidePlan,
    data: HwpData,
    rest: list[SlidePlan],
    slides_dir: Path,
    captions: dict[int, str],
    used_figures: set[int],
) -> str:
    kind = sp.kind
    reserved = set(ORG_PHOTO_FIGURE.values()) | set(PRIOR_RD_FIGURE.values()) | used_figures

    if kind == "cover":
        lead = data.orgs[0].name if data.orgs else "주관기관"
        hero_nums = _match_figures("goals", captions, data.figures, limit=1, exclude=reserved)
        hero = ""
        body_cls = "cover"
        if hero_nums:
            _claim_figures(used_figures, hero_nums[:1])
            body_cls = "cover has-hero"
        inner = f"""
{('<img class="hero-bg" src="' + _esc(_fig_src(data.figures, hero_nums[0], slides_dir) or '') + '" alt="">') if hero_nums and _fig_src(data.figures, hero_nums[0], slides_dir) else ''}
<div class="cover-inner">
<h1>{_esc(data.title)}</h1>
<div class="meta">{_esc(data.subtitle)}<br>주관: {_esc(lead)}<br>{_esc(data.date)}</div>
</div>
"""
        return _wrap(body_cls, inner)

    if kind == "closing":
        inner = f"""
<h1>감사합니다</h1>
<div class="meta">{_esc(data.title)}<br>{_esc(data.subtitle)}</div>
"""
        return _wrap("closing", inner)

    header = _header_block(sp)
    body = ""
    org = _org_from_header(data, sp.header)

    if kind == "toc":
        items = [f"{s.num}. {s.header}" for s in rest if s.kind not in ("cover", "toc", "closing")]
        grid = '<div class="toc-grid">' + "".join(f'<div class="item">{_esc(it)}</div>' for it in items[:16]) + "</div>"
        thumb_nums = _match_figures("toc", captions, data.figures, limit=1, exclude=reserved)
        _claim_figures(used_figures, thumb_nums)
        if thumb_nums and _fig_src(data.figures, thumb_nums[0], slides_dir):
            thumb = f'<div class="thumb">{_img_tag(data.figures, thumb_nums[0], slides_dir, "추진체계")}</div>'
            body = f'<div class="toc-with-thumb">{thumb}<div class="col">{grid}</div></div>'
        else:
            body = grid

    elif kind == "org_intro":
        if org or data.orgs:
            o = org or data.orgs[0]
            pi = o.pi + (f" ({o.team})" if o.team else "")
            text = f'<div class="pi">{_esc(pi)}</div>' + _bullets_html(_history_bullets(o.history), 4)
            figs = _match_figures("org_intro", captions, data.figures, limit=2, exclude=reserved)
            _claim_figures(used_figures, figs)
            body = _visual_dual(figs, text, data.figures, slides_dir, "기관 인프라")

    elif kind == "background":
        text = _bullets_html(_flatten_background(data.background), 4)
        figs = _match_figures("background", captions, data.figures, limit=1, exclude=reserved)
        _claim_figures(used_figures, figs)
        body = _visual_split(figs, text, data.figures, slides_dir, "개발 배경")

    elif kind == "goals":
        text = _bullets_html(data.goals or [sp.action_title], 4)
        figs = _match_figures("goals", captions, data.figures, limit=1, exclude=reserved)
        _claim_figures(used_figures, figs)
        body = _visual_split(figs, text, data.figures, slides_dir, "개발 목표")

    elif kind == "performance":
        rows = [(r[0], r[1], r[2], r[3]) for r in data.performance]
        chart = _bar_chart_html(rows)
        mini = _table_html(["항목", "목표치"], [(r[0], r[2]) for r in rows[:4]], ["55%", "45%"])
        body = f'<div class="two-col"><div class="col">{chart}</div><div class="col">{mini}</div></div>'

    elif kind == "method":
        rows = [(t[0], t[1], t[2]) for t in data.method_techs]
        tbl = _table_html(["핵심기술", "개발내용", "담당"], rows[:4], ["22%", "58%", "20%"])
        figs = _match_figures("method", captions, data.figures, limit=2, exclude=reserved)
        _claim_figures(used_figures, figs)
        body = _visual_dual(figs, tbl, data.figures, slides_dir, "개발 방법")

    elif kind == "capability":
        if org:
            pi = org.pi + (f" ({org.team})" if org.team else "")
            pi_num = ORG_PHOTO_FIGURE.get(org.name)
            _claim_figures(used_figures, [pi_num] if pi_num else [])
            photo = _img_or_placeholder(data.figures, pi_num, slides_dir, "책임자 사진", "photo-lg")
            hist = _bullets_html(_history_bullets(org.history), 4)
            pat = '<div class="subhead">지식재산권</div>' + _patent_cards_html(org.patents)
            body = f'<div class="two-col">{photo}<div class="col"><div class="pi">{_esc(pi)}</div><div class="subhead">주요 이력</div>{hist}{pat}</div></div>'

    elif kind == "intl_evidence":
        nums = _match_figures("intl_evidence", captions, data.figures, limit=3, exclude=set())
        if not nums:
            nums = [n for n in INTL_EVIDENCE_FIGURES if n in data.figures and n not in used_figures][:2]
        _claim_figures(used_figures, nums)
        panels = "".join(
            f'<div class="panel">{_img_tag(data.figures, n, slides_dir, "협력 증빙")}</div>'
            for n in nums
            if _fig_src(data.figures, n, slides_dir)
        )
        body = f'<div class="panels">{panels}</div>' if panels else '<div class="placeholder">협력 증빙 이미지</div>'

    elif kind == "execution":
        text = _bullets_html(_execution_bullets(org) if org else [], 4)
        figs = _match_figures("execution", captions, data.figures, org_name=org.name if org else None, limit=1, exclude=reserved)
        _claim_figures(used_figures, figs)
        body = _visual_split(figs, text, data.figures, slides_dir, "수행 내용")

    elif kind == "prior_rd":
        if org:
            prior_num = PRIOR_RD_FIGURE.get(org.name)
            extra: list[int] = []
            if prior_num and prior_num not in used_figures:
                _claim_figures(used_figures, [prior_num])
            elif prior_num:
                prior_num = None
            img = _img_or_placeholder(data.figures, prior_num, slides_dir, "선행연구", "visual")
            tbl = _table_html(["선행연구", "활용계획"], org.prior_rd[:4], ["45%", "55%"])
            if prior_num and _fig_src(data.figures, prior_num, slides_dir):
                body = f'<div class="visual-split">{img}<div class="text">{tbl}</div></div>'
            else:
                extra = _match_figures("prior_rd", captions, data.figures, limit=1, exclude=reserved)
                _claim_figures(used_figures, extra)
                if extra:
                    body = _visual_split(extra, tbl, data.figures, slides_dir, "선행연구")
                else:
                    body = f'<div class="two-col">{img}<div class="col">{tbl}</div></div>'

    elif kind == "yearly":
        if org:
            body = _timeline_html(org.yearly)
            if len(org.yearly) > 4:
                body += _table_html(["연차", "추진내용"], org.yearly[4:6], ["14%", "86%"])

    elif kind == "roles":
        rows = []
        for o in data.orgs:
            role_text = _first_execution_bullet(o) or (o.history[0] if o.history else "")
            rows.append((o.name, o.role, role_text))
        tbl = _table_html(["기관", "역할", "담당 내용"], rows, ["28%", "12%", "60%"])
        figs = _match_figures("roles", captions, data.figures, limit=1, exclude=reserved)
        _claim_figures(used_figures, figs)
        body = _visual_split(figs, tbl, data.figures, slides_dir, "추진체계")

    elif kind == "schedule":
        tbl = _table_html(["연차", "단계별 목표"], data.phase_goals, ["14%", "86%"])
        figs = _match_figures("schedule", captions, data.figures, limit=1, exclude=reserved)
        _claim_figures(used_figures, figs)
        body = _visual_split(figs, tbl, data.figures, slides_dir, "세부 일정")

    elif kind == "budget":
        if data.budget_years:
            stack = _budget_stack_html(data.budget_years)
            summary = f'<p style="font-size:15px;font-weight:700;margin-bottom:10px">총 {_esc(data.budget_total or "")}</p>' if data.budget_total else ""
            mini = _table_html(["연차", "정부", "민간", "합계"], data.budget_years, ["14%", "28%", "28%", "30%"])
            body = summary + stack + mini
        elif data.budget_total:
            body = f'<p style="font-size:16px;font-weight:700">{_esc(data.budget_total)}</p>'

    elif kind == "commercialization":
        text = _bullets_html(data.commercialization or [sp.action_title], 4)
        figs = _match_figures("commercialization", captions, data.figures, limit=2, exclude=reserved)
        _claim_figures(used_figures, figs)
        body = _visual_dual(figs, text, data.figures, slides_dir, "사업화")

    elif kind == "commercialization_strategy":
        text = _bullets_html(data.commercialization_strategy or [sp.action_title], 4)
        figs = _match_figures("commercialization_strategy", captions, data.figures, limit=1, exclude=reserved)
        _claim_figures(used_figures, figs)
        body = _visual_split(figs, text, data.figures, slides_dir, "사업화 전략")

    elif kind == "impact":
        text = _bullets_html(data.impact or [sp.action_title], 4)
        figs = _match_figures("impact", captions, data.figures, limit=1, exclude=reserved)
        _claim_figures(used_figures, figs)
        body = _visual_split(figs, text, data.figures, slides_dir, "기대효과")

    elif kind == "intl_base":
        parts = []
        figs = _match_figures("intl_base", captions, data.figures, limit=1, exclude=reserved)
        _claim_figures(used_figures, figs)
        if data.intl_stats:
            parts.append(_table_html(["항목", "실적"], data.intl_stats, ["35%", "65%"]))
        if data.intl_bullets:
            parts.append(_bullets_html(data.intl_bullets, 4))
        text = "".join(parts)
        body = _visual_split(figs, text, data.figures, slides_dir, "국제협력") if figs else text

    elif kind == "appendix_profile":
        if org:
            pi_num = ORG_PHOTO_FIGURE.get(org.name)
            # PI photo may repeat on capability + appendix only
            photo = _img_or_placeholder(data.figures, pi_num, slides_dir, "책임자 사진", "photo-lg")
            body = f'<div class="two-col">{photo}<div class="col"><div class="pi">{_esc(org.pi)}</div>{_bullets_html(_history_bullets(org.history), 6)}</div></div>'

    return _wrap("", f'{header}<div class="content">{body}</div>')


def _slug(sp: SlidePlan) -> str:
    s = re.sub(r"[^\w\-]+", "-", sp.header, flags=re.UNICODE).strip("-")[:40]
    return f"{sp.num}-{sp.kind}" + (f"-{s}" if s else "")


def build_all(data: HwpData, slides_dir: Path, stem: str = "input") -> list[Path]:
    slides_dir.mkdir(parents=True, exist_ok=True)
    captions = _load_figure_captions(stem)
    plan = [s for s in data.slide_plan if s.include]
    written: list[Path] = []
    used_figures: set[int] = set()
    for i, sp in enumerate(plan):
        out = slides_dir / f"{_slug(sp)}.html"
        out.write_text(
            render_slide(sp, data, plan[i + 1 :], slides_dir, captions, used_figures),
            encoding="utf-8",
        )
        written.append(out)

    index_lines = [
        "<!DOCTYPE html><html lang='ko'><head><meta charset='UTF-8'>",
        "<title>Slide preview</title>",
        "<style>body{font-family:sans-serif;padding:24px} a{display:block;margin:6px 0}</style>",
        "</head><body><h1>Slides</h1>",
    ]
    for p in written:
        index_lines.append(f'<a href="{_esc(p.name)}" target="_blank">{_esc(p.name)}</a>')
    index_lines.append("</body></html>")
    (slides_dir / "index.html").write_text("\n".join(index_lines), encoding="utf-8")
    return written
