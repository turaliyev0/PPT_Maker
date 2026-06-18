#!/usr/bin/env python3
"""Rich editorial slide generator — full-bleed splits, visual timelines, verified diagrams."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON = ROOT / "templates" / "extracted" / "input-hwp-from-html-parsed.json"
OUT = ROOT / "slides"
IMG = "../templates/extracted/input-hwp-full/bindata"

BASE = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1280px; height: 720px; overflow: hidden;
  font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
  background: #ffffff; color: #16181d;
}
.kicker { font-size: 13px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #6b7280; }
.accent { color: #1F4E79; }
.body { font-size: 16px; line-height: 1.55; color: #2c2f36; list-style: none; }
.body li { margin-bottom: 8px; padding-left: 1.15em; text-indent: -1.15em; }
.body li::before { content: "○ "; color: #2E75B6; font-weight: 700; }
.tbl { width: 100%; border-collapse: collapse; font-size: 14px; }
.tbl th { text-align: left; font-weight: 700; color: #1F4E79; border-bottom: 2px solid #1F4E79; padding: 9px 10px; }
.tbl td { border-bottom: 1px solid #e3e6ea; padding: 8px 10px; vertical-align: top; }
"""


def e(s: str) -> str:
    return html.escape(str(s or ""), quote=True)


def page(title: str, body: str, css: str = "") -> str:
    return (
        f'<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n'
        f"<title>{e(title)}</title>\n<style>\n{BASE}{css}\n</style>\n</head>\n"
        f"<body>{body}\n</body>\n</html>\n"
    )


def patents_table(org: dict, limit: int = 4) -> str:
    if not org.get("patents"):
        return '<p style="font-size:15px;color:#6b7280;font-style:italic">지식재산권: 해당 없음 (HWP 기재)</p>'
    rows = "".join(
        f"<tr><td>{e(p['name'][:50])}{'…' if len(p['name']) > 50 else ''}</td>"
        f"<td>{e(p['status'])}</td></tr>"
        for p in org["patents"][:limit]
    )
    return (
        f'<table class="tbl"><thead><tr><th>특허·출원</th><th style="width:13%">구분</th></tr></thead>'
        f"<tbody>{rows}</tbody></table>"
    )


def org_block_data(org: dict) -> tuple[str, str, str]:
    exec_items = org["execution"][0][1] if org.get("execution") else []
    exec_ul = "".join(f"<li>{e(x)}</li>" for x in exec_items)
    prior_rows = "".join(
        f"<tr><td>{e(r[0][:40])}{'…' if len(r[0]) > 40 else ''}</td>"
        f"<td>{e(r[1][:52])}{'…' if len(r[1]) > 52 else ''}</td></tr>"
        for r in (org.get("prior_rd") or [])[:3]
    ) or '<tr><td colspan="2">해당 없음</td></tr>'
    year_rows = "".join(
        f'<tr><td style="white-space:nowrap;font-weight:700;color:#1F4E79">{e(y[0])}</td>'
        f"<td>{e(y[1])}</td></tr>"
        for y in (org.get("yearly") or [])[:4]
    )
    return exec_ul, prior_rows, year_rows


# ── 01 Cover ─────────────────────────────────────────────────────────────────
def slide_cover(d: dict) -> str:
    chips = ["배경·목표", "연구방법", "책임자 역량", "국제협력", "수행계획", "사업화"]
    chip_html = "".join(f'<span class="chip">{e(c)}</span>' for c in chips)
    css = """
body { display: grid; grid-template-columns: 1.05fr 0.95fr; }
.left {
  background: linear-gradient(155deg, #0f2d4a 0%, #1F4E79 45%, #2E75B6 100%);
  padding: 56px 52px 56px 72px; display: flex; flex-direction: column; justify-content: center;
  position: relative; overflow: hidden;
}
.left::after {
  content: ''; position: absolute; right: -80px; top: -80px; width: 320px; height: 320px;
  border-radius: 50%; background: rgba(255,255,255,.06);
}
.left .kicker { color: #8ec5f0; margin-bottom: 20px; }
.left h1 { font-size: 40px; font-weight: 800; color: #fff; line-height: 1.32; margin-bottom: 28px; position: relative; z-index: 1; }
.meta { font-size: 17px; color: #c5dff5; line-height: 2.1; margin-bottom: 32px; position: relative; z-index: 1; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; position: relative; z-index: 1; }
.chip {
  font-size: 13px; font-weight: 600; color: #d4e8f8; padding: 6px 14px;
  border: 1px solid rgba(255,255,255,.35); border-radius: 20px;
}
.right {
  background: linear-gradient(180deg, #0a1f33 0%, #122a42 100%);
  display: flex; align-items: center; justify-content: center; padding: 28px 32px;
}
.right img { width: 100%; max-height: 620px; object-fit: contain; filter: drop-shadow(0 12px 32px rgba(0,0,0,.35)); }
"""
    body = f"""
<div class="left">
  <div class="kicker">{e(d['subtitle'])}</div>
  <h1>{e(d['title'])}</h1>
  <div class="meta">주관: ㈜경안써머텍<br>참여: 인하대학교 · KTR · 중경우전대학교<br>{e(d['date'])}</div>
  <div class="chips">{chip_html}</div>
</div>
<div class="right">
  <img src="{IMG}/BIN002C.png" alt="통합 시스템 패키지">
</div>
"""
    return page(d["title"], body, css)


# ── 02 Background + goals — diagram hero + goal pills + perf strip ─────────────
def slide_background_goals(d: dict) -> str:
    bg = [x.strip() for x in d["background"] if x and not x.startswith("  ")][:3]
    goals = "".join(
        f'<div class="goal"><span class="gn">{i}</span><p>{e(g)}</p></div>'
        for i, g in enumerate(d["goals"][:5], 1)
    )
    perf = "".join(
        f'<div class="pm"><div class="pv">{e(r[2])}</div><div class="pl">{e(r[0])}</div>'
        f'<div class="pu">{e(r[3] if len(r) > 3 else r[1])}</div></div>'
        for r in d["performance"][:4]
        if r[0] and not r[0].startswith(".") and not r[0][0].isdigit()
    )
    css = """
.wrap { display: grid; grid-template-rows: auto 1fr auto; height: 720px; }
.top { padding: 40px 64px 16px; display: grid; grid-template-columns: 1fr 1fr; gap: 32px; align-items: end; }
.top h1 { font-size: 34px; font-weight: 800; line-height: 1.25; }
.top h1 em { color: #1F4E79; font-style: normal; }
.bg-list { font-size: 15px; line-height: 1.5; color: #475569; }
.bg-list li { margin-bottom: 5px; list-style: none; padding-left: 1em; text-indent: -1em; }
.bg-list li::before { content: "— "; color: #2E75B6; }
.mid { display: grid; grid-template-columns: 1fr 580px; min-height: 0; }
.goals { padding: 0 64px; display: flex; flex-direction: column; gap: 10px; justify-content: center; }
.goal { display: flex; gap: 14px; align-items: flex-start; }
.goal .gn {
  flex-shrink: 0; width: 28px; height: 28px; background: #1F4E79; color: #fff;
  font-size: 14px; font-weight: 800; border-radius: 50%; display: flex; align-items: center; justify-content: center;
}
.goal p { font-size: 15px; line-height: 1.45; }
.hero { background: linear-gradient(135deg, #f0f6fc 0%, #e8f0f8 100%); display: flex; align-items: center; justify-content: center; padding: 20px; }
.hero img { width: 100%; max-height: 340px; object-fit: contain; }
.bottom { padding: 16px 64px 36px; border-top: 3px solid #1F4E79; }
.perf-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.pm { text-align: center; }
.pv { font-size: 32px; font-weight: 800; color: #1F4E79; line-height: 1; }
.pl { font-size: 14px; font-weight: 700; color: #2c2f36; margin-top: 6px; }
.pu { font-size: 12px; color: #6b7280; margin-top: 2px; }
.lbl { font-size: 13px; font-weight: 700; color: #6b7280; letter-spacing: .1em; margin-bottom: 10px; }
"""
    body = f"""
<div class="wrap">
  <div class="top">
    <div>
      <div class="kicker">개발 배경 · 목표 · 성능</div>
      <h1>AI기반 열관리 + <em>고효율 액침냉각</em><br>통합 솔루션</h1>
    </div>
    <ul class="bg-list">{''.join(f'<li>{e(x)}</li>' for x in bg)}</ul>
  </div>
  <div class="mid">
    <div class="goals">{goals}</div>
    <div class="hero"><img src="{IMG}/BIN0003.png" alt="기술개발 로드맵"></div>
  </div>
  <div class="bottom">
    <div class="lbl">성능 목표</div>
    <div class="perf-row">{perf}</div>
  </div>
</div>
"""
    return page("개발 배경·목표·성능", body, css)


# ── 03 Method — full-height diagram split ────────────────────────────────────
def slide_method_roles(d: dict) -> str:
    tech_rows = "".join(
        f"<tr><td><strong>{e(t[0])}</strong></td><td>{e(t[2])}</td>"
        f"<td>{e(t[1][:70])}{'…' if len(t[1]) > 70 else ''}</td></tr>"
        for t in d["method_techs"]
    )
    role_rows = "".join(
        f"<tr><td><strong>{e(o['name'])}</strong></td><td>{e(o['role'])}</td>"
        f"<td>{e(o['execution'][0][1][0] if o.get('execution') else '')}</td></tr>"
        for o in d["orgs"]
    )
    css = """
.wrap { display: grid; grid-template-columns: 520px 1fr; height: 720px; }
.visual {
  background: linear-gradient(180deg, #0f2d4a 0%, #1a3d5c 100%);
  display: flex; flex-direction: column; justify-content: center; padding: 36px 28px;
}
.visual .tag { font-size: 12px; font-weight: 700; color: #8ec5f0; letter-spacing: .12em; margin-bottom: 12px; }
.visual h2 { font-size: 22px; font-weight: 800; color: #fff; line-height: 1.35; margin-bottom: 20px; }
.visual img { width: 100%; max-height: 480px; object-fit: contain; }
.content { padding: 40px 48px 40px 36px; display: flex; flex-direction: column; gap: 18px; }
.content h1 { font-size: 26px; font-weight: 800; color: #1F4E79; }
.block .sub { font-size: 15px; font-weight: 700; color: #2E75B6; margin-bottom: 8px; }
"""
    body = f"""
<div class="wrap">
  <div class="visual">
    <div class="tag">SYSTEM ARCHITECTURE</div>
    <h2>액침냉각 시스템<br>1·2차 냉각루프 통합</h2>
    <img src="{IMG}/BIN0004.png" alt="액침냉각 시스템 구성">
  </div>
  <div class="content">
    <div class="kicker">연구개발 방법</div>
    <h1>핵심기술 및 기관별 역할</h1>
    <div class="block">
      <div class="sub">핵심기술</div>
      <table class="tbl"><thead><tr><th style="width:24%">기술</th><th style="width:12%">담당</th><th>내용</th></tr></thead>
      <tbody>{tech_rows}</tbody></table>
    </div>
    <div class="block">
      <div class="sub">기관별 역할</div>
      <table class="tbl"><thead><tr><th>기관</th><th style="width:14%">구분</th><th>수행</th></tr></thead>
      <tbody>{role_rows}</tbody></table>
    </div>
  </div>
</div>
"""
    return page("연구개발 방법 및 기관별 역할", body, css)


# ── 04 Capability 경안 — 3-col PI + certs ───────────────────────────────────
def slide_capability_kyung(org: dict, title: str) -> str:
    css = """
.wrap { display: grid; grid-template-columns: 220px 1fr 250px; height: 720px; padding: 36px 48px 32px; gap: 24px; }
.col-pi { display: flex; flex-direction: column; gap: 10px; }
.col-pi img.portrait { width: 73px; height: auto; border-radius: 6px; border: 1px solid #dde2ea; }
.pi-name { font-size: 17px; font-weight: 800; color: #1F4E79; line-height: 1.35; }
.pi-meta { font-size: 13px; color: #6b7280; line-height: 1.5; }
.chip { font-size: 12px; background: #eef4fb; border-radius: 6px; padding: 8px 10px; text-align: center; }
.chip b { display: block; font-size: 18px; color: #1F4E79; }
.col-main { display: flex; flex-direction: column; min-height: 0; }
.col-main h1 { font-size: 22px; font-weight: 800; color: #16181d; margin: 6px 0 12px; line-height: 1.35; }
.stats { display: flex; gap: 10px; margin-bottom: 12px; flex-shrink: 0; }
.stats span { flex: 1; font-size: 13px; color: #475569; padding: 8px 0; border-top: 2px solid #1F4E79; }
.stats b { color: #1F4E79; }
.sec { font-size: 14px; font-weight: 700; color: #1F4E79; margin-bottom: 6px; }
.certs { border-top: 1px solid #dde2ea; padding-top: 10px; margin-top: auto; flex-shrink: 0; }
.certs p { font-size: 10px; font-weight: 700; letter-spacing: .12em; color: #2E75B6; margin-bottom: 6px; }
.cert-row { display: flex; gap: 8px; }
.cert-row img { flex: 1; width: 100%; height: 120px; object-fit: contain; border: 1px solid #dde2ea; border-radius: 4px; background: #fff; }
.col-pat { display: flex; flex-direction: column; min-height: 0; }
"""
    body = f"""
<div class="wrap">
  <div class="col-pi">
    <div class="kicker">주관</div>
    <img class="portrait" src="{IMG}/BIN0020.bmp" alt="엄상수 총괄책임">
    <div class="pi-name">엄상수<br><span style="font-size:13px;font-weight:600">총괄책임</span></div>
    <div class="pi-meta">경안써머텍 대표<br>석사/전자공학</div>
    <div class="chip"><b>12</b>총 인원</div>
    <div class="chip"><b>40+</b>년 제작 경험</div>
    <div class="chip"><b>5</b>특허 출원</div>
    <img src="{IMG}/BIN0017.bmp" alt="산업자원부 장관상 표창" style="width:100%;height:auto;margin-top:6px;border:1px solid #c8d9ec;border-radius:4px">
  </div>
  <div class="col-main">
    <div class="kicker">책임자 역량</div>
    <h1>데이터센터 액침냉각 시스템 설계·제작</h1>
    <div class="stats">
      <span><b>CE PED</b> · ASME U/UM</span>
      <span><b>IoT</b> 스마트 제어</span>
      <span><b>다품종</b> 용접 자동화</span>
    </div>
    <div class="sec">주요 역량</div>
    <ul class="body" style="font-size:15px">{''.join(f'<li>{e(h)}</li>' for h in org['history'][:6])}</ul>
    <div style="flex:1;background:#f0f5fb;border-radius:10px;padding:12px;display:flex;align-items:center;justify-content:center;margin:10px 0;min-height:0">
      <img src="{IMG}/BIN0008.png" alt="AI 통합 냉각 제어" style="width:100%;height:auto;max-height:180px;object-fit:contain">
    </div>
    <div class="certs">
      <p>보유 국제 인증서 (원본)</p>
      <div class="cert-row">
        <img src="{IMG}/BIN001D.bmp" alt="ASME CE PED UL 인증">
      </div>
    </div>
  </div>
  <div class="col-pat">
    <div class="sec">지식재산권</div>
    {patents_table(org, 5)}
  </div>
</div>
"""
    return page(title, body, css)


# ── 05 Capability 인하대 — split + award doc ─────────────────────────────────
def slide_capability_inha(org: dict, title: str) -> str:
    css = """
.wrap { display: grid; grid-template-columns: 220px 1fr 480px; height: 720px; padding: 36px 48px; gap: 24px; }
.col-pi img { width: 71px; height: auto; border-radius: 6px; border: 1px solid #dde2ea; }
.pi-name { font-size: 17px; font-weight: 800; color: #1F4E79; margin: 8px 0 4px; line-height: 1.35; }
.pi-meta { font-size: 13px; color: #6b7280; line-height: 1.5; margin-bottom: 10px; }
.chip { font-size: 12px; background: #eef4fb; border-radius: 6px; padding: 8px; text-align: center; margin-bottom: 8px; }
.chip b { display: block; font-size: 18px; color: #1F4E79; }
.col-main h1 { font-size: 21px; font-weight: 800; margin: 6px 0 14px; line-height: 1.35; }
.tl { display: flex; gap: 10px; margin-bottom: 8px; }
.tl .dot { width: 8px; height: 8px; background: #2E75B6; border-radius: 50%; margin-top: 7px; flex-shrink: 0; }
.tl p { font-size: 15px; line-height: 1.45; }
.visual { display: flex; flex-direction: column; gap: 10px; }
.panel { background: #f0f5fb; border-radius: 10px; padding: 14px; flex: 1; display: flex; align-items: center; justify-content: center; min-height: 0; }
.panel img { width: 100%; height: auto; object-fit: contain; }
.award img { width: 100%; height: auto; border: 1px solid #c8d9ec; border-radius: 4px; }
.award p { font-size: 10px; color: #9ca3af; text-align: center; margin-top: 4px; }
"""
    items = "".join(
        f'<div class="tl"><div class="dot"></div><p>{e(h)}</p></div>'
        for h in org["history"][:5]
    )
    body = f"""
<div class="wrap">
  <div class="col-pi">
    <div class="kicker">위탁</div>
    <img src="{IMG}/BIN0021.bmp" alt="이철희 교수">
    <div class="pi-name">이철희 교수<br><span style="font-size:13px;font-weight:600">위탁총괄</span></div>
    <div class="pi-meta">인하대 기계공학과<br>박사/기계공학</div>
    <div class="chip"><b>5</b>총 인원</div>
    <div class="chip"><b>CFD</b>·디지털트윈</div>
  </div>
  <div class="col-main">
    <div class="kicker">책임자 역량</div>
    <h1>열·유동 해석(CFD/FEM) 기반 구조 최적화</h1>
    {items}
    <div style="margin-top:14px">{patents_table(org, 3)}</div>
  </div>
  <div class="visual">
    <div class="panel"><img src="{IMG}/BIN0007.png" alt="유체순환 운전조건 최적화"></div>
    <div class="award">
      <img src="{IMG}/BIN001A.bmp" alt="이철희 교수 수상이력">
      <p>수상·연구 실적 (HWP 원본)</p>
    </div>
  </div>
</div>
"""
    return page(title, body, css)


# ── 06 Capability KTR — test matrix visual ───────────────────────────────────
def slide_capability_ktr(org: dict, title: str) -> str:
    tests = [
        ("열성능", "Q, 열전달계수"),
        ("내압·누설", "헬륨 리크, 압력강하"),
        ("구조 안전", "장기 신뢰성"),
        ("인증 대응", "공인시험성적서"),
    ]
    grid = "".join(
        f'<div class="cell"><div class="icon">{e(t[0][0])}</div><b>{e(t[0])}</b><p>{e(t[1])}</p></div>'
        for t in tests
    )
    css = """
.wrap { padding: 44px 64px; height: 720px; display: flex; flex-direction: column; }
.head { margin-bottom: 24px; }
.head h1 { font-size: 30px; font-weight: 800; color: #1F4E79; margin-top: 6px; }
.pi { font-size: 17px; color: #475569; margin-top: 6px; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
.cell {
  background: linear-gradient(145deg, #E8F4FC, #f4f9fd); border-radius: 12px;
  padding: 20px 16px; text-align: center;
}
.cell .icon {
  width: 44px; height: 44px; background: #1F4E79; color: #fff; font-size: 20px; font-weight: 800;
  border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;
}
.cell b { display: block; font-size: 16px; color: #1F4E79; margin-bottom: 4px; }
.cell p { font-size: 13px; color: #6b7280; }
.lower { flex: 1; display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 32px; }
"""
    body = f"""
<div class="wrap">
  <div class="head">
    <div class="kicker">책임자 역량 · 위탁</div>
    <h1>한국화학융합시험연구원</h1>
    <div class="pi">{e(org['pi'])}</div>
  </div>
  <div class="grid">{grid}</div>
  <div class="lower">
    <div><div style="font-size:15px;font-weight:700;color:#1F4E79;margin-bottom:10px">시험·검증 역량</div>
      <ul class="body">{''.join(f'<li>{e(h)}</li>' for h in org['history'][:5])}</ul></div>
    <div style="background:#f8fafc;border-radius:12px;padding:24px;display:flex;align-items:center">
      <p style="font-size:16px;line-height:1.6;color:#1F4E79;font-weight:600">
        열성능·내압·누설·구조 안전성 시험 및<br>공인시험성적서 확보 지원<br><br>
        <span style="font-size:14px;font-weight:400;color:#6b7280;font-style:italic">지식재산권: 해당 없음 (HWP 기재)</span>
      </p>
    </div>
  </div>
</div>
"""
    return page(title, body, css)


# ── 07 Capability 중경우전 — welding robot + award ───────────────────────────
def slide_capability_jung(org: dict, title: str) -> str:
    skills = ["비전-레이저 용접선 추적", "로봇 자동용접", "다중 패스 용접", "결함 저감", "압력용기 정밀 용접"]
    tags = "".join(f'<span class="tag">{e(s)}</span>' for s in skills)
    css = """
.wrap { display: grid; grid-template-columns: 1fr 420px; height: 720px; }
.content { padding: 40px 36px 40px 64px; display: flex; flex-direction: column; }
.content h1 { font-size: 22px; font-weight: 800; color: #1F4E79; margin: 8px 0 14px; line-height: 1.35; }
.pi { font-size: 15px; color: #475569; margin-bottom: 14px; line-height: 1.5; }
.tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }
.tag { font-size: 13px; font-weight: 600; color: #1F4E79; background: #E8F4FC; padding: 6px 14px; border-radius: 20px; }
.visual { background: #0f2d4a; display: flex; flex-direction: column; padding: 28px 24px; gap: 14px; }
.visual .panel { flex: 1; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,.04); border-radius: 10px; padding: 12px; min-height: 0; }
.visual .panel img { width: 100%; height: auto; max-height: 280px; object-fit: contain; }
.award img { width: 100%; height: auto; border: 1px solid rgba(255,255,255,.2); border-radius: 4px; }
.award p { font-size: 10px; color: #8ec5f0; text-align: center; margin-top: 4px; }
"""
    body = f"""
<div class="wrap">
  <div class="content">
    <div class="kicker">책임자 역량 · 국제공동</div>
    <h1>비전-레이저 기반 용접선 추적 및 로봇 자동용접</h1>
    <div class="pi">{e(org['pi'])}</div>
    <div class="tags">{tags}</div>
    <ul class="body" style="font-size:15px">{''.join(f'<li>{e(h)}</li>' for h in org['history'][:5])}</ul>
    <div style="margin-top:auto">{patents_table(org, 4)}</div>
  </div>
  <div class="visual">
    <div class="panel"><img src="{IMG}/BIN0006.bmp" alt="원주형 용접 로봇"></div>
    <div class="award">
      <img src="{IMG}/BIN0025.png" alt="Rui Li 교수 수상 실적">
      <p>重庆市科学技术奖 一等奖 · Rui Li</p>
    </div>
  </div>
</div>
"""
    return page(title, body, css)


# ── 08 Intl — stat hero + timeline ───────────────────────────────────────────
def slide_intl_combined(d: dict) -> str:
    stats = ""
    colors = ["#1F4E79", "#2E75B6", "#3d8cc4", "#5a9fd4"]
    for i, (label, val) in enumerate(d["intl_stats"]):
        m = re.search(r"(\d+)", val)
        num = m.group(1) if m else "—"
        unit = "건" if "건" in val else "편" if "편" in val else "회" if "회" in val else ""
        stats += (
            f'<div class="sc" style="border-top:4px solid {colors[i]}">'
            f'<div class="num">{e(num)}<span>{unit}</span></div>'
            f'<div class="lbl">{e(label)}</div><div class="desc">{e(val)}</div></div>'
        )
    bullets = "".join(f'<li>{e(b)}</li>' for b in d["intl_bullets"])
    css = """
.wrap { padding: 40px 64px; height: 720px; display: flex; flex-direction: column; }
.head h1 { font-size: 34px; font-weight: 800; margin-top: 8px; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 24px 0; }
.sc { background: #f8fafc; border-radius: 10px; padding: 20px 16px; }
.num { font-size: 52px; font-weight: 800; color: #1F4E79; line-height: 1; }
.num span { font-size: 22px; }
.lbl { font-size: 16px; font-weight: 700; color: #2E75B6; margin-top: 8px; }
.desc { font-size: 13px; color: #6b7280; margin-top: 4px; line-height: 1.4; }
.lower { flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: start; }
.timeline { border-left: 3px solid #1F4E79; padding-left: 24px; }
.tl-item { margin-bottom: 16px; position: relative; }
.tl-item::before {
  content: ''; position: absolute; left: -30px; top: 6px; width: 12px; height: 12px;
  background: #2E75B6; border-radius: 50%; border: 2px solid #fff; box-shadow: 0 0 0 2px #1F4E79;
}
.tl-item b { font-size: 14px; color: #1F4E79; display: block; margin-bottom: 4px; }
.tl-item p { font-size: 15px; line-height: 1.5; }
"""
    timeline_items = [
        ("20년+", "인하대—중경우전대 지능형 센서·로봇 분야 국제협력"),
        ("4건", "한중 국제협력 공동과제 수행"),
        ("18편", "고수준 학술논문 공동 게재"),
        ("6건", "공동 발명특허 출원"),
    ]
    tl = "".join(
        f'<div class="tl-item"><b>{e(t[0])}</b><p>{e(t[1])}</p></div>' for t in timeline_items
    )
    body = f"""
<div class="wrap">
  <div class="head">
    <div class="kicker">국제공동연구</div>
    <h1>인하대 — 중경우전대 <em style="color:#1F4E79;font-style:normal">한중 협력</em></h1>
  </div>
  <div class="stats">{stats}</div>
  <div class="lower">
    <ul class="body">{bullets}</ul>
    <div>
      <div class="timeline">{tl}</div>
      <div style="margin-top:16px;background:#f4f7fb;border-radius:8px;padding:10px">
        <img src="{IMG}/BIN001F.bmp" alt="국제공동연구계약서" style="width:100%;height:auto;max-height:140px;object-fit:contain">
        <p style="font-size:10px;color:#9ca3af;text-align:center;margin-top:4px">국제공동연구 계약서 (HWP 원본)</p>
      </div>
    </div>
  </div>
</div>
"""
    return page("국제공동연구 협력", body, css)


# ── Org blocks ───────────────────────────────────────────────────────────────
def slide_org_kyung(org: dict, img: str) -> str:
    exec_ul, prior_rows, year_rows = org_block_data(org)
    years = org.get("yearly") or []
    timeline = "".join(
        f'<div class="yr"><b>{e(y[0])}</b><p>{e(y[1][:55])}{"…" if len(y[1])>55 else ""}</p></div>'
        for y in years[:4]
    )
    css = """
.wrap { display: grid; grid-template-rows: 1fr auto; height: 720px; }
.main { display: grid; grid-template-columns: 440px 1fr; min-height: 0; }
.visual { background: #0f2d4a; display: flex; align-items: center; justify-content: center; padding: 20px; }
.visual img { width: 100%; max-height: 480px; object-fit: contain; }
.content { padding: 36px 48px 24px 32px; overflow: hidden; }
.title { font-size: 26px; font-weight: 800; color: #1F4E79; margin-bottom: 14px; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 12px; }
.timeline { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0;
  background: linear-gradient(90deg, #1F4E79, #2E75B6); padding: 20px 48px; }
.yr { color: #fff; padding: 0 12px; border-right: 1px solid rgba(255,255,255,.25); }
.yr:last-child { border-right: none; }
.yr b { display: block; font-size: 15px; margin-bottom: 6px; opacity: .85; }
.yr p { font-size: 13px; line-height: 1.4; opacity: .95; }
.sec { font-size: 14px; font-weight: 700; color: #1F4E79; margin-bottom: 6px; }
"""
    body = f"""
<div class="wrap">
  <div class="main">
    <div class="visual"><img src="{IMG}/{img}" alt="열교환 모듈"></div>
    <div class="content">
      <div class="kicker">주관 · 수행·선행·연차</div>
      <div class="title">{e(org['name'])}</div>
      <div class="sec">수행 내용</div>
      <ul class="body" style="font-size:15px">{exec_ul}</ul>
      <div class="grid2">
        <div><div class="sec">선행연구</div>
          <table class="tbl" style="font-size:12px"><thead><tr><th>연구</th><th>활용</th></tr></thead><tbody>{prior_rows}</tbody></table></div>
        <div><div class="sec">연차별</div>
          <table class="tbl" style="font-size:12px"><thead><tr><th>연차</th><th>내용</th></tr></thead><tbody>{year_rows}</tbody></table></div>
      </div>
    </div>
  </div>
  <div class="timeline">{timeline}</div>
</div>
"""
    return page(f"{org['name']} 수행·선행·연차", body, css)


def slide_org_inha(org: dict) -> str:
    exec_ul, prior_rows, year_rows = org_block_data(org)
    years = org.get("yearly") or []
    timeline = "".join(
        f'<div class="yr"><b>{e(y[0])}</b><p>{e(y[1][:52])}{"…" if len(y[1])>52 else ""}</p></div>'
        for y in years[:4]
    )
    css = """
.wrap { display: grid; grid-template-rows: 1fr auto; height: 720px; padding: 40px 64px 0; }
.title { font-size: 26px; font-weight: 800; color: #1F4E79; margin: 8px 0 16px; }
.main { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 24px; min-height: 0; }
.sec { font-size: 14px; font-weight: 700; color: #1F4E79; margin-bottom: 8px; }
.timeline { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0;
  background: linear-gradient(90deg, #1F4E79, #2E75B6); padding: 20px 48px; }
.yr { color: #fff; padding: 0 12px; border-right: 1px solid rgba(255,255,255,.25); }
.yr:last-child { border-right: none; }
.yr b { display: block; font-size: 15px; margin-bottom: 6px; }
.yr p { font-size: 13px; line-height: 1.4; opacity: .95; }
"""
    body = f"""
<div class="wrap">
  <div>
    <div class="kicker">위탁 · 수행·선행·연차</div>
    <div class="title">{e(org['name'])}</div>
    <div class="main">
      <div><div class="sec">수행 내용</div><ul class="body" style="font-size:15px">{exec_ul}</ul></div>
      <div><div class="sec">선행연구</div><table class="tbl" style="font-size:12px"><tbody>{prior_rows}</tbody></table></div>
      <div><div class="sec">연차별</div><table class="tbl" style="font-size:12px"><tbody>{year_rows}</tbody></table></div>
    </div>
  </div>
  <div class="timeline">{timeline}</div>
</div>
"""
    return page(f"{org['name']} 수행·선행·연차", body, css)


def slide_org_ktr(org: dict) -> str:
    exec_ul, prior_rows, year_rows = org_block_data(org)
    phases = "".join(
        f'<div class="ph"><div class="yr">{e(y[0])}</div><p>{e(y[1][:60])}{"…" if len(y[1])>60 else ""}</p></div>'
        for y in (org.get("yearly") or [])[:4]
    )
    css = """
.wrap { padding: 40px 64px; height: 720px; display: flex; flex-direction: column; }
.title { font-size: 26px; font-weight: 800; color: #1F4E79; margin: 8px 0 20px; }
.upper { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; margin-bottom: 20px; }
.phases { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; flex: 1; }
.ph { background: #f4f7fb; border-radius: 10px; padding: 14px 12px; border-top: 3px solid #1F4E79; }
.ph .yr { font-size: 14px; font-weight: 800; color: #1F4E79; margin-bottom: 8px; }
.ph p { font-size: 13px; line-height: 1.4; }
.sec { font-size: 14px; font-weight: 700; color: #1F4E79; margin-bottom: 8px; }
"""
    body = f"""
<div class="wrap">
  <div class="kicker">위탁 · 수행·선행·연차</div>
  <div class="title">{e(org['name'])}</div>
  <div class="upper">
    <div><div class="sec">수행 내용</div><ul class="body" style="font-size:15px">{exec_ul}</ul></div>
    <div><div class="sec">선행연구</div><table class="tbl" style="font-size:13px"><tbody>{prior_rows}</tbody></table></div>
  </div>
  <div class="sec">연차별 추진계획</div>
  <div class="phases">{phases}</div>
</div>
"""
    return page(f"{org['name']} 수행·선행·연차", body, css)


def slide_org_jung(org: dict) -> str:
    exec_ul, prior_rows, _ = org_block_data(org)
    years = org.get("yearly") or []
    roadmap = "".join(
        f'<div class="rm"><div class="dot"></div><b>{e(y[0])}</b><p>{e(y[1][:48])}{"…" if len(y[1])>48 else ""}</p></div>'
        for y in years[:4]
    )
    css = """
.wrap { padding: 40px 64px; height: 720px; display: flex; flex-direction: column; }
.title { font-size: 26px; font-weight: 800; color: #1F4E79; margin: 8px 0 20px; }
.upper { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 32px; margin-bottom: 24px; }
.roadmap {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; flex: 1;
  position: relative; padding-top: 20px;
}
.roadmap::before {
  content: ''; position: absolute; top: 28px; left: 8%; right: 8%; height: 3px; background: #2E75B6;
}
.rm { text-align: center; position: relative; z-index: 1; }
.rm .dot {
  width: 16px; height: 16px; background: #1F4E79; border: 3px solid #fff; border-radius: 50%;
  margin: 0 auto 12px; box-shadow: 0 0 0 2px #1F4E79;
}
.rm b { display: block; font-size: 15px; color: #1F4E79; margin-bottom: 8px; }
.rm p { font-size: 13px; line-height: 1.4; text-align: left; background: #f8fafc; padding: 10px; border-radius: 8px; }
.sec { font-size: 14px; font-weight: 700; color: #1F4E79; margin-bottom: 8px; }
"""
    body = f"""
<div class="wrap">
  <div class="kicker">국제공동 · 수행·선행·연차</div>
  <div class="title">{e(org['name'])}</div>
  <div class="upper">
    <div><div class="sec">수행 내용</div><ul class="body" style="font-size:15px">{exec_ul}</ul></div>
    <div><div class="sec">선행연구</div><table class="tbl" style="font-size:13px"><tbody>{prior_rows}</tbody></table></div>
  </div>
  <div class="sec">연차별 추진 — 용접 공정 자동화</div>
  <div class="roadmap">{roadmap}</div>
</div>
"""
    return page(f"{org['name']} 수행·선행·연차", body, css)


# ── 13 Schedule + budget — Gantt + bar chart ─────────────────────────────────
def slide_schedule_budget(d: dict) -> str:
    phases = d["phase_goals"]
    bars = ""
    colors = ["#1F4E79", "#2E75B6", "#3d8cc4", "#5a9fd4"]
    for i, (yr, txt) in enumerate(phases):
        bars += (
            f'<div class="bar-row"><div class="by">{e(yr)}</div>'
            f'<div class="bar" style="width:{70 + i*8}%;background:{colors[i]}"></div>'
            f'<p>{e(txt[:55])}{"…" if len(txt)>55 else ""}</p></div>'
        )
    budget_vals = [int(re.sub(r"[^\d]", "", row[3] or row[1])) for row in d["budget_years"]]
    max_b = max(budget_vals) if budget_vals else 1
    bchart = "".join(
        f'<div class="bc"><div class="bf" style="height:{int(v/max_b*140)}px"></div>'
        f'<div class="bl">{e(d["budget_years"][i][0])}</div>'
        f'<div class="bv">{v:,}</div></div>'
        for i, v in enumerate(budget_vals)
    )
    css = """
.wrap { padding: 40px 64px; height: 720px; display: grid; grid-template-rows: auto 1fr auto; gap: 20px; }
h1 { font-size: 30px; font-weight: 800; margin-top: 6px; }
.gantt { display: flex; flex-direction: column; gap: 12px; justify-content: center; }
.bar-row { display: grid; grid-template-columns: 80px 1fr; gap: 16px; align-items: center; }
.by { font-size: 14px; font-weight: 800; color: #1F4E79; }
.bar { height: 28px; border-radius: 4px; min-width: 120px; }
.bar-row p { grid-column: 2; font-size: 13px; color: #475569; margin-top: -4px; }
.budget { border-top: 2px solid #1F4E79; padding-top: 16px; }
.bh { font-size: 20px; font-weight: 800; color: #1F4E79; margin-bottom: 12px; }
.bchart { display: flex; align-items: flex-end; gap: 32px; height: 180px; padding: 0 20px; }
.bc { display: flex; flex-direction: column; align-items: center; flex: 1; }
.bf { width: 56px; background: linear-gradient(180deg, #2E75B6, #1F4E79); border-radius: 4px 4px 0 0; }
.bl { font-size: 13px; font-weight: 700; color: #1F4E79; margin-top: 8px; }
.bv { font-size: 12px; color: #6b7280; margin-top: 2px; }
"""
    body = f"""
<div class="wrap">
  <div>
    <div class="kicker">추진 일정 · 연구비</div>
    <h1>4개년 단계별 목표</h1>
  </div>
  <div class="gantt">{bars}</div>
  <div class="budget">
    <div class="bh">총 연구비 {e(d['budget_total'])}</div>
    <div class="bchart">{bchart}</div>
  </div>
</div>
"""
    return page("추진 일정 및 연구비", body, css)


# ── 14 Commercialization — funnel + columns ──────────────────────────────────
def slide_commercialization(d: dict) -> str:
    strat = [
        c for c in d["commercialization_strategy"]
        if c and not c.startswith(" ") and c not in ("시장 현황 및 사업화 목표", "제품화 계획")
    ]
    css = """
.wrap { padding: 40px 64px; height: 720px; display: flex; flex-direction: column; }
h1 { font-size: 28px; font-weight: 800; margin: 8px 0 20px; }
.funnel { display: flex; align-items: center; justify-content: center; gap: 0; margin-bottom: 24px; }
.fstep {
  text-align: center; color: #fff; font-weight: 700; font-size: 15px; line-height: 1.35;
  padding: 20px 24px; clip-path: polygon(0 0, 92% 0, 100% 50%, 92% 100%, 0 100%, 8% 50%);
}
.fstep:first-child { clip-path: polygon(0 0, 92% 0, 100% 50%, 92% 100%, 0 100%); padding-left: 28px; }
.fstep:last-child { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 8% 50%); padding-right: 28px; }
.cols { flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
.sec { font-size: 16px; font-weight: 700; color: #1F4E79; margin-bottom: 10px; }
"""
    body = f"""
<div class="wrap">
  <div class="kicker">사업화</div>
  <h1>AI 기반 탄소저감형 액침냉각 통합 패키지</h1>
  <div class="funnel">
    <div class="fstep" style="background:#1F4E79;width:200px">1단계<br><span style="font-size:13px;font-weight:400">핵심 모듈</span></div>
    <div class="fstep" style="background:#2E75B6;width:220px">2단계<br><span style="font-size:13px;font-weight:400">통합 패키지</span></div>
    <div class="fstep" style="background:#3d8cc4;width:240px">3단계<br><span style="font-size:13px;font-weight:400">AI 지능형 시스템</span></div>
  </div>
  <div class="cols">
    <div><div class="sec">사업화 목표</div>
      <ul class="body">{''.join(f'<li>{e(c)}</li>' for c in d['commercialization'][:5])}</ul></div>
    <div><div class="sec">사업화 전략</div>
      <ul class="body">{''.join(f'<li>{e(c)}</li>' for c in strat[:5])}</ul></div>
  </div>
</div>
"""
    return page("사업화 목표 및 전략", body, css)


# ── 15 Impact — diagram + numbered cards ─────────────────────────────────────
def slide_impact(d: dict) -> str:
    items = "".join(
        f'<div class="card"><span class="n">{i}</span><div><b>{e(x.split(")")[0]+")" if ")" in x else "")}</b>'
        f'<p>{e(x.split(")",1)[1].strip() if ")" in x else x)}</p></div></div>'
        for i, x in enumerate(d["impact"], 1)
    )
    css = """
.wrap { display: grid; grid-template-columns: 420px 1fr; height: 720px; }
.visual {
  background: linear-gradient(160deg, #0f2d4a, #1a3d5c);
  display: flex; align-items: center; justify-content: center; padding: 24px;
}
.visual img { width: 100%; max-height: 580px; object-fit: contain; }
.content { padding: 44px 56px 44px 36px; display: flex; flex-direction: column; justify-content: center; }
.content h1 { font-size: 30px; font-weight: 800; margin: 8px 0 24px; line-height: 1.3; }
.card { display: flex; gap: 14px; margin-bottom: 14px; align-items: flex-start; }
.card .n {
  flex-shrink: 0; width: 32px; height: 32px; background: #1F4E79; color: #fff;
  font-weight: 800; font-size: 15px; display: flex; align-items: center; justify-content: center; border-radius: 8px;
}
.card b { font-size: 14px; color: #2E75B6; display: block; margin-bottom: 2px; }
.card p { font-size: 15px; line-height: 1.45; }
"""
    body = f"""
<div class="wrap">
  <div class="visual"><img src="{IMG}/BIN001E.bmp" alt="기대효과 협력체계"></div>
  <div class="content">
    <div class="kicker">기대효과</div>
    <h1>에너지 절감 · 탄소저감 ·<br>기술 확보</h1>
    {items}
  </div>
</div>
"""
    return page("기대효과", body, css)


# ── 16 Closing ─────────────────────────────────────────────────────────────
def slide_closing(d: dict) -> str:
    css = """
body {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  text-align: center; background: linear-gradient(155deg, #0f2d4a 0%, #1F4E79 50%, #2E75B6 100%);
  position: relative; overflow: hidden;
}
body::before {
  content: ''; position: absolute; width: 500px; height: 500px; border-radius: 50%;
  background: rgba(255,255,255,.04); top: -150px; right: -100px;
}
h1 { font-size: 56px; font-weight: 800; color: #fff; margin-bottom: 20px; position: relative; }
.sub { font-size: 18px; color: #c5dff5; max-width: 780px; line-height: 1.6; margin-bottom: 36px; position: relative; }
.orgs { font-size: 15px; color: #8ec5f0; letter-spacing: .05em; position: relative; }
"""
    body = f"""
<h1>감사합니다</h1>
<p class="sub">{e(d['title'])}</p>
<div class="orgs">㈜경안써머텍 · 인하대학교 · 한국화학융합시험연구원 · 중경우전대학교</div>
"""
    return page("감사합니다", body, css)


def main() -> None:
    d = json.loads(JSON.read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()
    orgs = {o["name"]: o for o in d["orgs"]}
    files: list[tuple[str, str]] = [
        ("01-cover-표지.html", slide_cover(d)),
        ("02-background_goals-개발-배경-목표.html", slide_background_goals(d)),
        ("03-method_roles-연구방법-역할.html", slide_method_roles(d)),
        ("04-capability-경안써머텍.html", slide_capability_kyung(
            orgs["㈜경안써머텍"], "책임자 역량 — (주관) ㈜경안써머텍")),
        ("05-capability-인하대학교.html", slide_capability_inha(
            orgs["인하대학교"], "책임자 역량 — (위탁) 인하대학교")),
        ("06-capability-KTR.html", slide_capability_ktr(
            orgs["한국화학융합시험연구원"], "책임자 역량 — (위탁) KTR")),
        ("07-capability-중경우전대학교.html", slide_capability_jung(
            orgs["중경우전대학교"], "책임자 역량 — (국제공동) 중경우전대학교")),
        ("08-intl_combined-국제공동연구.html", slide_intl_combined(d)),
        ("09-org_block-경안써머텍.html", slide_org_kyung(orgs["㈜경안써머텍"], "BIN000D.png")),
        ("10-org_block-인하대학교.html", slide_org_inha(orgs["인하대학교"])),
        ("11-org_block-KTR.html", slide_org_ktr(orgs["한국화학융합시험연구원"])),
        ("12-org_block-중경우전대학교.html", slide_org_jung(orgs["중경우전대학교"])),
        ("13-schedule_budget-일정-예산.html", slide_schedule_budget(d)),
        ("14-commercialization-사업화.html", slide_commercialization(d)),
        ("15-impact-기대효과.html", slide_impact(d)),
        ("16-closing-감사합니다.html", slide_closing(d)),
    ]
    for name, content in files:
        (OUT / name).write_text(content, encoding="utf-8")
    index = (
        f'<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><title>미리보기</title>'
        f"<style>body{{font-family:'Malgun Gothic',sans-serif;padding:24px}}"
        f"a{{display:block;padding:6px 0;color:#1F4E79}}</style></head><body>"
        f"<h2>{e(d['title'])}</h2><p>{len(files)} slides</p>"
    )
    for name, _ in files:
        index += f'<a href="{name}">{name}</a>\n'
    index += "</body></html>"
    (OUT / "index.html").write_text(index, encoding="utf-8")
    print(f"Wrote {len(files)} slides to {OUT}")


if __name__ == "__main__":
    main()
