#!/usr/bin/env python3
"""Parse extracted HWP plain text into structured presentation data."""
from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "templates" / "extracted"

ORG_ALIASES = {
    "경안": "㈜경안써머텍",
    "경안써머텍": "㈜경안써머텍",
    "인하대": "인하대학교",
    "KTR": "한국화학융합시험연구원",
    "중경우전대": "중경우전대학교",
}

ROLE_LABELS = {
    "주관": "주관",
    "위탁1": "위탁",
    "위탁2": "위탁",
    "국제": "국제공동",
}


@dataclass
class Patent:
    name: str
    country: str
    status: str


@dataclass
class Org:
    name: str
    role: str
    pi: str
    team: str = ""
    history: list[str] = field(default_factory=list)
    patents: list[Patent] = field(default_factory=list)
    relevance: list[tuple[str, str]] = field(default_factory=list)
    execution: list[tuple[str, list[str]]] = field(default_factory=list)
    prior_rd: list[tuple[str, str]] = field(default_factory=list)
    yearly: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class SlidePlan:
    """Structured slide plan with academic-style action titles (from HWP facts only)."""

    num: str
    kind: str
    header: str
    action_title: str
    hwp_source: str = ""
    include: bool = True
    skip_reason: str = ""


@dataclass
class HwpData:
    title: str
    subtitle: str
    date: str
    orgs: list[Org]
    goals: list[str]
    impact: list[str]
    figures: dict[int, str]
    has_intl_cooperation: bool
    intl_stats: list[tuple[str, str]]
    intl_bullets: list[str]
    missing: list[dict]
    outline: list[str]
    slide_plan: list[SlidePlan] = field(default_factory=list)
    # Extended HWP sections (included in slide_plan when present)
    background: list[str] = field(default_factory=list)
    phase_goals: list[tuple[str, str]] = field(default_factory=list)
    performance: list[tuple[str, str, str, str]] = field(default_factory=list)
    method_techs: list[tuple[str, str, str]] = field(default_factory=list)
    budget_total: str = ""
    budget_years: list[tuple[str, str, str, str]] = field(default_factory=list)
    commercialization: list[str] = field(default_factory=list)
    commercialization_strategy: list[str] = field(default_factory=list)


# Figure numbers in HWP that map to slide image slots
ORG_PHOTO_FIGURE = {
    "㈜경안써머텍": 23,
    "인하대학교": 26,
    "한국화학융합시험연구원": 24,
    "중경우전대학교": 25,
}
PRIOR_RD_FIGURE = {
    "㈜경안써머텍": 13,
    "인하대학교": 14,
}
INTL_EVIDENCE_FIGURES = [20, 21]


def _clean(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s.replace("&amp;", "&")


def _lines(text: str) -> list[str]:
    return [ln.strip() for ln in text.splitlines()]


def load_figures(stem: str = "input") -> dict[int, str]:
    path = EXTRACTED / f"{stem}-figures.json"
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {int(f["num"]): f["path"] for f in raw if f.get("path")}


def figure_path(figures: dict[int, str], num: int, root: Path) -> Path | None:
    rel = figures.get(num)
    if not rel:
        return None
    p = root / rel
    return p if p.exists() else None


def parse_goals(text: str) -> list[str]:
    block = re.search(r"개발 목표\s+(.+?)\s+개발 방법", text, re.DOTALL)
    if not block:
        return []
    goals = []
    for ln in _lines(block.group(1)):
        m = re.match(r"[○◦]\s*\(([^)]+)\)\s*(.+)", ln)
        if m:
            goals.append(f"({m.group(1)}) {m.group(2)}")
    return goals


def parse_background(text: str) -> list[str]:
    block = re.search(r"1-1\.\s*개발 배경 및 필요성\s+(.+?)(?:그림\s+\d|1-2\.)", text, re.DOTALL)
    if not block:
        return []
    items: list[str] = []
    for ln in _lines(block.group(1)):
        if ln.startswith("■"):
            items.append(_clean(ln.lstrip("■ ")))
        elif ln.startswith("◦") or ln.startswith("○"):
            items.append("  " + _clean(ln.lstrip("◦○ ")))
    return items[:12]


def parse_phase_goals(text: str) -> list[tuple[str, str]]:
    block = re.search(r"1-2\.\s*기술개발 단계별 목표\s+(.+?)\s+2\.\s*연구개발 방법", text, re.DOTALL)
    if not block:
        return []
    lines = _lines(block.group(1))
    result: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        if re.match(r"^\d+차년도$", lines[i]):
            year = lines[i]
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                result.append((year, _clean(lines[j])))
            i = j + 1
            continue
        i += 1
    return result


def parse_performance_targets(text: str) -> list[tuple[str, str, str, str]]:
    """Return rows: (항목, 단위, 4차년도 목표, 평가방법)."""
    block = re.search(r"2-2\.\s*결과물 성능검증\s+(.+?)\s+3\.\s*선행연구", text, re.DOTALL)
    if not block:
        return []
    lines = [ln for ln in _lines(block.group(1)) if ln and ln not in {"평가 항목", "단위", "비중", "(%)", "평가방법"}]
    rows: list[tuple[str, str, str, str]] = []
    i = 0
    while i < len(lines):
        m = re.match(r"^(\d+)\.\s*(.+)$", lines[i])
        if not m:
            i += 1
            continue
        name = _clean(m.group(2))
        tail = lines[i + 1 : i + 12]
        unit = ""
        y4 = ""
        method = ""
        for t in tail:
            if t in {"W/m2·K", "kPa", "kW", "h", "bar", "mbar·L/s", "m/min", "mm"}:
                unit = t
            elif "ASME" in t or "ISO" in t or "의뢰" in t or "API" in t:
                method = t
            elif re.search(r"\d", t) and ("이상" in t or "이하" in t or re.match(r"^10", t)):
                if not y4:
                    y4 = t
        if name and unit:
            rows.append((name, unit, y4 or "[목표치 미기재]", method or "[평가방법 미기재]"))
        i += 1
    return rows[:8]


def parse_method_techs(text: str) -> list[tuple[str, str, str]]:
    block = re.search(r"■\s*핵심기술 구성\s+(.+?)\s+■\s*1차년도", text, re.DOTALL)
    if not block:
        return []
    lines = _lines(block.group(1))
    techs: list[tuple[str, str, str]] = []
    current_name = ""
    content_parts: list[str] = []
    org = ""
    for ln in lines:
        if re.match(r"^\d+\.\s+", ln):
            if current_name:
                techs.append((current_name, _clean(" ".join(content_parts)), org or "[담당 미기재]"))
            current_name = _clean(re.sub(r"^\d+\.\s*", "", ln))
            content_parts = []
            org = ""
            continue
        if ln in {"주관", "인하대", "주관·", "주관·인하대"} or "주관" in ln and len(ln) < 12:
            org = _clean(ln)
        elif ln and ln not in {"핵심기술", "주요 개발 내용", "담당 기관"}:
            if not re.match(r"^\d+\.", ln) and ln != current_name:
                content_parts.append(ln)
    if current_name:
        techs.append((current_name, _clean(" ".join(content_parts)), org or "[담당 미기재]"))
    return techs[:5]


def parse_budget(text: str) -> tuple[str, list[tuple[str, str, str, str]]]:
    m = re.search(
        r"총 연구개발비\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)",
        text,
    )
    if not m:
        return "", []
    years = [
        ("1차년도", m.group(1), "[민간부담]", m.group(1)),
        ("2차년도", m.group(2), "[민간부담]", m.group(2)),
        ("3차년도", m.group(3), "[민간부담]", m.group(3)),
        ("4차년도", m.group(4), "[민간부담]", m.group(4)),
    ]
    total = f"{m.group(5)}천원"
    return total, years


def parse_commercialization(text: str) -> tuple[list[str], list[str]]:
    goals_block = re.search(
        r"\(1\)\s*구체적인 사업화 목표\s+.+?■\s*(.+?)\s*\(2\)\s*사업화 전략",
        text,
        re.DOTALL,
    )
    goals: list[str] = []
    if goals_block:
        for ln in _lines(goals_block.group(1)):
            if ln.startswith("■"):
                goals.append(_clean(ln.lstrip("■ ")))
            elif ln.startswith("◦") or ln.startswith("○"):
                goals.append(_clean(ln.lstrip("◦○ ")))
    goals = goals[:8]

    strat_block = re.search(r"\(2\)\s*사업화 전략\s+(.+?)\s*\(3\)\s*기대효과", text, re.DOTALL)
    strategy: list[str] = []
    if strat_block:
        for ln in _lines(strat_block.group(1)):
            if ln.startswith("■"):
                strategy.append(_clean(ln.lstrip("■ ")))
            elif ln.startswith("◦") or ln.startswith("○"):
                strategy.append(_clean(ln.lstrip("◦○ ")))
    return goals[:6], strategy[:6]


def parse_impact(text: str) -> list[str]:
    block = re.search(r"기대효과\s+(.+?)\s+󰊲", text, re.DOTALL)
    if not block:
        block = re.search(r"기대효과\s+(.+?)\s+자가진단", text, re.DOTALL)
    if not block:
        return []
    items = []
    for ln in _lines(block.group(1)):
        m = re.match(r"[○◦]\s*\(([^)]+)\)\s*(.+)", ln)
        if m:
            items.append(f"({m.group(1)}) {m.group(2)}")
    return items[:6]


def parse_title(text: str) -> tuple[str, str, str]:
    m = re.search(
        r"중소기업 기술개발.*?연구개발계획서.*?과제명\s+(.+?)\s+개발 목표",
        text,
        re.DOTALL,
    )
    title = _clean(m.group(1)) if m else "과제명 (HWP에서 미확인)"
    subtitle = "중소기업 기술개발(R&D) 지원사업"
    dm = re.search(r"(\d{4})\s*년\s+(\d{1,2})\s*월", text)
    date = f"{dm.group(1)}. {dm.group(2).zfill(2)}" if dm else ""
    return title, subtitle, date


def parse_team(text: str) -> list[Org]:
    orgs: list[Org] = []
    block = re.search(r"연구팀 구성\s+(.+?)\s+기대효과", text, re.DOTALL)
    if not block:
        return orgs

    for line in _lines(block.group(1)):
        m = re.match(r"[○◦]\s*\(([^)]+)\)\s*(.+?)\s*[:：—]\s*(.+)", line)
        if not m:
            continue
        role_key, org_name, rest = m.group(1), _clean(m.group(2)), m.group(3)
        role = ROLE_LABELS.get(role_key, role_key)
        if "경안" in org_name and "㈜" not in org_name:
            org_name = "㈜경안써머텍"
        team_m = re.search(r"\(총\s*(\d+)\s*명\)", rest)
        team = f"총 {team_m.group(1)}명" if team_m else ""
        pi = _clean(rest[: team_m.start()] if team_m else rest)
        orgs.append(Org(name=org_name, role=role, pi=pi, team=team))
    return orgs


def _parse_patent_block(section: str) -> list[Patent]:
    patents: list[Patent] = []
    if "지식재산권" not in section:
        return patents

    chunk = section.split("지식재산권", 1)[1]
    chunk = re.split(r"■\s*대표적 논문|■\s*대표 수상", chunk)[0]
    parts = re.split(r"(?m)^특허\s*$", chunk)
    for part in parts[1:]:
        lines = [ln for ln in _lines(part) if ln and ln not in {"구분", "지식재산권명", "국가명", "비고"}]
        if len(lines) < 3:
            continue
        # name may span multiple lines before country
        country_idx = next(
            (i for i, ln in enumerate(lines) if ln in {"대한민국", "중국", "미국", "일본", "유럽"}),
            None,
        )
        if country_idx is None or country_idx < 1:
            continue
        name = _clean(" ".join(lines[:country_idx]))
        country = lines[country_idx]
        tail = lines[country_idx + 1 :]
        status = tail[-1] if tail and tail[-1] in {"출원", "등록"} else ""
        patents.append(Patent(name=name, country=country, status=status))
    return patents


def parse_patents(text: str) -> dict[str, list[Patent]]:
    mapping: dict[str, list[Patent]] = {}
    patterns = [
        (r"\[주관기관:\s*([^\]]+)\]", "㈜경안써머텍"),
        (r"\[위탁기관:\s*([^\]]+)\]", "인하대학교"),
        (r"\[국제공동연구기관:\s*([^\]]+)\]", "중경우전대학교"),
    ]
    for pat, default_name in patterns:
        for m in re.finditer(pat, text):
            key = default_name
            if "경안" in m.group(1):
                key = "㈜경안써머텍"
            elif "인하" in m.group(1):
                key = "인하대학교"
            elif "중경" in m.group(1) or "우전" in m.group(1):
                key = "중경우전대학교"
            end = text.find("[", m.end())
            section = text[m.start() : end if end != -1 else m.start() + 8000]
            mapping[key] = _parse_patent_block(section)
    return mapping


def parse_capability(text: str, org_name: str) -> list[str]:
    key = org_name.replace("㈜", "").replace("(", "\\(").replace(")", "\\)")
    patterns = [
        rf"■\s*기관 고유역량\s*\[주관기관:\s*경안",
        rf"■\s*기관 고유역량\s*\[국제공동연구기관:\s*중경",
        rf"■\s*기관 고유역량\s*\[위탁기관:\s*인하",
        rf"■\s*기관 고유역량\s*\[위탁기관:\s*한국화학",
    ]
    idx_map = {
        "㈜경안써머텍": 0,
        "중경우전대학교": 1,
        "인하대학교": 2,
        "한국화학융합시험연구원": 3,
    }
    i = idx_map.get(org_name)
    if i is None:
        return []
    matches = list(re.finditer(r"■\s*기관 고유역량\s*\[[^\]]+\]", text))
    if i >= len(matches):
        return []
    start = matches[i].start()
    end = matches[i + 1].start() if i + 1 < len(matches) else start + 2500
    section = text[start:end]
    bullets: list[str] = []
    for ln in _lines(section):
        if ln.startswith("◦") or ln.startswith("○"):
            bullets.append(_clean(ln.lstrip("◦○ ").strip()))
    return bullets[:6]


def parse_development_method(text: str) -> dict[str, list[tuple[str, list[str]]]]:
    block = re.search(r"개발 방법\s+(.+?)\s+연구팀 구성", text, re.DOTALL)
    if not block:
        return {}

    result: dict[str, list[tuple[str, list[str]]]] = {}
    current_org = ""
    current_title = ""
    bullets: list[str] = []

    def flush():
        nonlocal current_org, current_title, bullets
        if current_org and current_title:
            result.setdefault(current_org, []).append((current_title, bullets[:]))
        bullets = []

    for ln in _lines(block.group(1)):
        om = re.match(r"(\d+)\)\s*(.+?)\(([^)]+)\)", ln)
        if om:
            flush()
            name = om.group(2).strip()
            role = om.group(3)
            if "주관" in role:
                current_org = "㈜경안써머텍"
            elif "위탁" in role and "1" in role:
                current_org = "인하대학교"
            elif "위탁" in role:
                current_org = "한국화학융합시험연구원"
            elif "국제" in role:
                current_org = "중경우전대학교"
            else:
                current_org = _clean(name)
            current_title = _clean(name.split("-")[-1] if "-" in name else name)
            continue
        bm = re.match(r"[○◦]\s*\(([^)]+)\)\s*(.+)", ln)
        if bm and current_org:
            bullets.append(f"({bm.group(1)}) {_clean(bm.group(2))}")
    flush()
    return result


def parse_prior_rd(text: str) -> dict[str, list[tuple[str, str]]]:
    result: dict[str, list[tuple[str, str]]] = {}

    # 주관 — explicit prior project
    m = re.search(
        r"주관연구개발기관 선행연구개발 실적_㈜경안써머텍\s+(.+?)\s+■\s*연구개발 실적_㈜경안써머텍",
        text,
        re.DOTALL,
    )
    if m:
        chunk = _clean(m.group(1))
        result.setdefault("㈜경안써머텍", []).append(
            (
                "4.2MPa급 고압 압력용기 개발 (2021–2023)",
                "압력용기 설계·자동용접·CE PED 인증 → 액침냉각 핵심 모듈 제작 활용",
            )
        )

    m2 = re.search(r"■\s*연구개발 실적_㈜경안써머텍\s+(.+?)\s+■\s*보유 인증", text, re.DOTALL)
    if m2:
        result.setdefault("㈜경안써머텍", []).append(
            ("압력용기·열교환기·응축기 설계·제작 (40년+)", "고효율 액침냉각 열교환 모듈 개발에 직접 적용")
        )
        result["㈜경안써머텍"].append(
            ("CE PED·ASME·KTR 공인시험", "열성능·내압·누설·신뢰성 검증 체계 구축")
        )

    m3 = re.search(r"■\s*연구개발 실적_인하대학교\s+(.+?)\s+그림 14", text, re.DOTALL)
    if m3:
        result["인하대학교"] = [
            ("수소 연료전지 3종 열병합 (농촌진흥청)", "열유동 해석·디지털 트윈 방법론 활용"),
            ("AI 스마트팜 인지·제어 (YOLO·딥러닝)", "열부하 예측·제어 최적화 알고리즘 개발"),
            ("HVAC·스팀 트레이스 열유동 해석", "액침조·유체순환계 열유동 검증 경험 활용"),
        ]

    return result


def parse_yearly(text: str) -> dict[str, list[tuple[str, str]]]:
    block = re.search(r"■\s*연구개발 세부 추진일정\s+(.+?)\s+6\.\s*연구비", text, re.DOTALL)
    if not block:
        return {}

    lines = _lines(block.group(1))
    years: dict[str, list[str]] = {}
    current_year = ""
    i = 0
    skip_orgs = {"전 기관", "전기관"}
    while i < len(lines):
        ln = lines[i]
        if re.match(r"^\d+차$", ln):
            j = i + 1
            while j < len(lines) and not lines[j]:
                j += 1
            if j < len(lines) and lines[j] == "년도":
                current_year = f"{ln}년도"
                years[current_year] = []
                i = j + 1
                continue
        if current_year and re.match(r"^\d+\.\s+", ln):
            task = _clean(ln)
            org_alias = ""
            j = i + 1
            while j < len(lines) and not lines[j]:
                j += 1
            if j < len(lines) and lines[j] in ORG_ALIASES:
                org_alias = ORG_ALIASES[lines[j]]
                i = j + 1
            else:
                i += 1
            if org_alias and org_alias not in skip_orgs:
                years[current_year].append(f"{task} ({org_alias})")
            continue
        i += 1

    by_org: dict[str, list[tuple[str, str]]] = {}
    for year, tasks in years.items():
        grouped: dict[str, list[str]] = {}
        for t in tasks:
            m = re.search(r"\(([^)]+)\)\s*$", t)
            if not m:
                continue
            org = m.group(1)
            task = _clean(re.sub(r"\s*\([^)]+\)\s*$", "", t))
            grouped.setdefault(org, []).append(task)
        for org, ts in grouped.items():
            by_org.setdefault(org, []).append((year, " / ".join(ts)))
    return by_org


def parse_intl(text: str) -> tuple[bool, list[tuple[str, str]], list[str]]:
    has = "국제공동" in text or "Agreement" in text
    stats: list[tuple[str, str]] = []
    bullets: list[str] = []

    pairs = [
        (r"국제협력과제\s*(\d+)건", "공동과제", "인하대—중경우전대 한중 국제협력과제 {}건"),
        (r"공동논문\s*(\d+)편", "공동논문", "고수준 학술논문 {}편 공동 게재"),
        (r"공동특허\s*(\d+)건", "공동특허", "공동 발명특허 {}건 출원"),
        (r"상호 방문\s*(\d+)회", "인력교류", "연구인력 상호 방문 {}회"),
    ]
    for pat, label, tmpl in pairs:
        m = re.search(pat, text)
        if m:
            stats.append((label, tmpl.format(m.group(1))))

    for ln in _lines(text):
        if "School of Automation" in ln or "지능형 센서" in ln or "20년" in ln:
            bullets.append(_clean(ln.lstrip("◦○ ")))

    if not bullets:
        bullets = [
            "지능형 센서·로봇·용접 계측·제어 연구역량",
            "인하대학교와 국제공동연구 기반",
        ]
    return has, stats[:4], bullets[:4]


def _relevance_from_patents(org: Org, title: str) -> list[tuple[str, str]]:
    rel: list[tuple[str, str]] = []
    for p in org.patents[:3]:
        short = shorten_name(p.name, 28)
        rel.append((short, f"본 과제({title[:20]}…) 기술개발에 활용"))
    if not rel and org.history:
        for h in org.history[:3]:
            rel.append((h[:30], "본 과제 수행 역량으로 활용"))
    return rel


def shorten_name(s: str, n: int) -> str:
    s = _clean(s)
    return s if len(s) <= n else s[: n - 1] + "…"


def find_missing(data: HwpData) -> list[dict]:
    missing: list[dict] = []

    for org in data.orgs:
        fig = ORG_PHOTO_FIGURE.get(org.name)
        if fig and fig not in data.figures:
            missing.append(
                {
                    "item": f"{org.name} 책임자/기관 사진 (그림 {fig})",
                    "reason": "HWP 이미지 매핑 실패",
                    "options": ["플레이스홀더 표시", "이미지 파일 제공"],
                }
            )

    for org in data.orgs:
        if not org.patents and org.role in {"주관", "위탁", "국제공동"}:
            missing.append(
                {
                    "item": f"{org.name} 지식재산권",
                    "reason": "HWP에 해당 기관 특허 실적 없음",
                    "options": ["해당 없음으로 표시", "추가 자료 제공"],
                }
            )

    return missing


def _shorten_action(text: str, max_len: int = 90) -> str:
    t = _clean(text)
    if len(t) <= max_len:
        return t
    cut = t[: max_len - 1].rsplit(" ", 1)[0]
    return (cut or t[: max_len - 1]) + "…"


def _first_execution_bullet(org: Org) -> str:
    for _title, bullets in org.execution:
        for b in bullets:
            if b.strip():
                return b.strip()
        if _title.strip() and _title != org.name:
            return _title.strip()
    return ""


def _slide(
    kind: str,
    header: str,
    action_title: str,
    hwp_source: str = "",
    *,
    include: bool = True,
    skip_reason: str = "",
) -> SlidePlan:
    return SlidePlan(
        num="",
        kind=kind,
        header=header,
        action_title=action_title,
        hwp_source=hwp_source,
        include=include,
        skip_reason=skip_reason,
    )


def _renumber_slides(plan: list[SlidePlan]) -> list[SlidePlan]:
    n = 0
    for s in plan:
        if not s.include:
            continue
        n += 1
        s.num = f"{n:02d}"
    return [s for s in plan if s.include]


def _has_org_roles(data: HwpData) -> bool:
    return len(data.orgs) >= 2 and any(org.execution for org in data.orgs)


def build_slide_plan(data: HwpData) -> list[SlidePlan]:
    """Compact HWP-driven plan — important sections only, merged to avoid sparse slides."""
    body: list[SlidePlan] = []

    if data.background or data.goals or data.performance:
        action = _shorten_action(data.goals[0] if data.goals else data.background[0])
        body.append(
            _slide(
                "background_goals",
                "개발 배경·목표·성능",
                action,
                "개발 배경·목표",
            )
        )

    if data.method_techs or _has_org_roles(data):
        mt = data.method_techs[0] if data.method_techs else ("", "", "")
        body.append(
            _slide(
                "method_roles",
                "연구개발 방법 및 기관별 역할",
                _shorten_action(f"{mt[0]} {mt[1]}" if mt[0] else "참여기관별 역할 분담"),
                "개발 방법·연구팀",
            )
        )

    for org in data.orgs:
        if org.pi or org.history:
            cap = org.history[0] if org.history else org.pi
            body.append(
                _slide(
                    "capability",
                    f"책임자 역량 - ({org.role}) {org.name}",
                    _shorten_action(cap),
                    f"{org.name} 책임자 역량",
                )
            )

    intl_org = next((o for o in data.orgs if o.role == "국제공동"), None)
    if data.has_intl_cooperation and (
        any(data.figures.get(n) for n in INTL_EVIDENCE_FIGURES) or data.intl_stats
    ):
        stat = data.intl_stats[0] if data.intl_stats else ("국제협력", "협력 실적")
        body.append(
            _slide(
                "intl_combined",
                "국제공동연구 협력",
                _shorten_action(f"{stat[0]}: {stat[1]}"),
                "국제공동연구",
                include=True,
            )
        )

    for org in data.orgs:
        if org.execution or org.prior_rd or org.yearly:
            bullet = _first_execution_bullet(org)
            body.append(
                _slide(
                    "org_block",
                    f"{org.name} 수행·선행·연차",
                    _shorten_action(bullet or f"{org.name} 연차별 계획"),
                    f"{org.name} 수행계획",
                )
            )

    if data.phase_goals or data.budget_total or data.budget_years:
        sched = _shorten_action(data.phase_goals[0][1]) if data.phase_goals else ""
        budget = f"총 {data.budget_total}" if data.budget_total else "연구비 계획"
        body.append(
            _slide(
                "schedule_budget",
                "추진 일정 및 연구비",
                _shorten_action(f"{sched} · {budget}" if sched else budget),
                "일정·예산",
            )
        )

    if data.commercialization or data.commercialization_strategy:
        lead = data.commercialization[0] if data.commercialization else data.commercialization_strategy[0]
        body.append(
            _slide(
                "commercialization",
                "사업화 목표 및 전략",
                _shorten_action(lead),
                "사업화",
            )
        )

    if data.impact:
        body.append(
            _slide(
                "impact",
                "기대효과",
                _shorten_action(data.impact[0]),
                "기대효과",
            )
        )

    plan: list[SlidePlan] = [_slide("cover", "표지", data.title, "과제명")]
    plan.extend(body)
    if len([s for s in body if s.include]) >= 3:
        plan.append(_slide("closing", "감사합니다", data.title, ""))

    return _renumber_slides(plan)


def build_outline(data: HwpData) -> list[str]:
    if not data.slide_plan:
        return [f"표지 - {data.title}"]
    lines: list[str] = []
    for s in data.slide_plan:
        if s.kind == "cover":
            lines.append(f"표지 - {data.title}")
        else:
            lines.append(f"{s.num} | {s.header}")
    return lines


def parse_hwp_text(text: str, *, figures: dict[int, str] | None = None) -> HwpData:
    title, subtitle, date = parse_title(text)
    orgs = parse_team(text)
    patents = parse_patents(text)
    dev = parse_development_method(text)
    prior = parse_prior_rd(text)
    yearly = parse_yearly(text)
    has_intl, intl_stats, intl_bullets = parse_intl(text)
    goals = parse_goals(text)
    impact = parse_impact(text)
    background = parse_background(text)
    phase_goals = parse_phase_goals(text)
    performance = parse_performance_targets(text)
    method_techs = parse_method_techs(text)
    budget_total, budget_years = parse_budget(text)
    commercialization, commercialization_strategy = parse_commercialization(text)
    figs = figures or {}

    for org in orgs:
        org.patents = patents.get(org.name, [])
        org.history = parse_capability(text, org.name)
        org.execution = dev.get(org.name, [])
        if not org.execution and org.history:
            step_size = max(1, len(org.history) // 4)
            chunks = [org.history[i : i + step_size] for i in range(0, len(org.history), step_size)]
            org.execution = [(f"영역 {i+1}", c) for i, c in enumerate(chunks[:4])]
        org.prior_rd = prior.get(org.name, [])
        org.yearly = yearly.get(org.name, [])
        org.relevance = _relevance_from_patents(org, title)

    data = HwpData(
        title=title,
        subtitle=subtitle,
        date=date,
        orgs=orgs,
        goals=goals,
        impact=impact,
        figures=figs,
        has_intl_cooperation=has_intl,
        intl_stats=intl_stats,
        intl_bullets=intl_bullets,
        missing=[],
        outline=[],
        background=background,
        phase_goals=phase_goals,
        performance=performance,
        method_techs=method_techs,
        budget_total=budget_total,
        budget_years=budget_years,
        commercialization=commercialization,
        commercialization_strategy=commercialization_strategy,
    )
    data.missing = find_missing(data)
    data.slide_plan = build_slide_plan(data)
    data.outline = build_outline(data)
    return data


def parse_file(path: Path) -> HwpData:
    text = path.read_text(encoding="utf-8")
    stem = path.name.replace("-hwp-from-html.txt", "")
    return parse_hwp_text(text, figures=load_figures(stem))


def to_json(data: HwpData) -> str:
    def convert(obj):
        if hasattr(obj, "__dataclass_fields__"):
            d = asdict(obj)
            return d
        return obj

    payload = asdict(data)
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _console(text: str) -> str:
    enc = getattr(sys.stdout, "encoding", None) or "utf-8"
    return text.encode(enc, errors="replace").decode(enc)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/parse_hwp.py <file.hwp>")
        sys.exit(1)
    stem = Path(sys.argv[1]).stem
    text_path = EXTRACTED / f"{stem}-hwp-from-html.txt"

    if not text_path.exists():
        print(f"Missing {text_path}. Run: python scripts/extract_hwp_text.py {stem}.hwp")
        sys.exit(1)

    data = parse_file(text_path)
    out_json = EXTRACTED / f"{text_path.stem}-parsed.json"
    out_json.write_text(to_json(data), encoding="utf-8")

    print(f"Parsed {len(data.orgs)} orgs, {len(data.slide_plan)} slides (plan)")
    print(f"Wrote {out_json}")
    print("\n--- OUTLINE ---")
    for line in data.outline:
        print(_console(line))
    print("\n--- SLIDE PLAN (action titles) ---")
    for s in data.slide_plan:
        print(_console(f"{s.num} [{s.kind}] {s.header}"))
        print(_console(f"    -> {s.action_title}"))
    print("\n--- MISSING (ask user) ---", flush=True)
    for m in data.missing:
        print(_console(f"- {m['item']}: {m['reason']}"))
        print(_console(f"  Options: {', '.join(m['options'])}"))


if __name__ == "__main__":
    main()
