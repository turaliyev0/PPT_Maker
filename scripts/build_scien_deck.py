#!/usr/bin/env python3
"""Generate polished HTML slides with bindata images."""
from __future__ import annotations

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from slide_images import SCIEN_IMAGE_SPECS, ResolvedImage, html_src, resolve_all  # noqa: E402

OUT = ROOT / "slides"
STEM = "input"

BASE = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1280px; height: 720px; overflow: hidden;
  font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
  background: #ffffff; color: #16181d;
}
.slide { width: 100%; height: 100%; display: flex; flex-direction: column; }
.pad { padding: 44px 56px 40px; flex: 1; display: flex; flex-direction: column; }
.kicker { font-size: 15px; font-weight: 700; letter-spacing: .12em; color: #6b7280; margin-bottom: 6px; }
.headline { font-size: 36px; font-weight: 800; line-height: 1.22; margin-bottom: 22px; color: #16181d; }
.headline em, .headline .accent { color: #1F4E79; font-style: normal; }
.body { font-size: 18px; line-height: 1.62; color: #2c2f36; list-style: none; }
.body li { margin-bottom: 12px; padding-left: 1.2em; text-indent: -1.2em; }
.body li::before { content: "○ "; color: #2E75B6; font-weight: 700; }
.body.compact li { margin-bottom: 9px; font-size: 17px; }
.tbl { width: 100%; border-collapse: collapse; font-size: 16px; }
.tbl th { text-align: left; font-weight: 700; color: #1F4E79; border-bottom: 2px solid #1F4E79; padding: 12px 14px; font-size: 15px; }
.tbl td { border-bottom: 1px solid #e3e6ea; padding: 11px 14px; vertical-align: top; line-height: 1.45; }
.tbl tbody tr:last-child td { border-bottom: none; }
.subhead { font-size: 19px; font-weight: 700; color: #1F4E79; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 2px solid #1F4E79; }
.split { display: grid; height: 720px; }
.split .text-col { padding: 40px 36px 40px 56px; display: flex; flex-direction: column; justify-content: center; }
.split .img-col { background: #f4f7fb; display: flex; align-items: center; justify-content: center; padding: 16px 20px; overflow: hidden; }
.split .img-col img { width: 100%; height: 100%; object-fit: cover; border-radius: 4px; }
.split.diagram .img-col img { object-fit: contain; }
.img-cap { font-size: 13px; color: #6b7280; margin-top: 8px; text-align: center; }
"""


def e(s: str) -> str:
    return html.escape(str(s or ""), quote=True)


def page(title: str, body: str, css: str = "") -> str:
    return (
        f'<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n'
        f"<title>{e(title)}</title>\n<style>\n{BASE}{css}\n</style>\n</head>\n"
        f"<body>{body}\n</body>\n</html>\n"
    )


def img_tag(img: ResolvedImage | None, diagram: bool = False) -> str:
    if not img:
        return ""
    cls = "diagram" if diagram else ""
    return f'<img src="{html_src(img)}" alt="{e(img.alt)}">'


def split_slide(
    text_html: str,
    img: ResolvedImage | None,
    *,
    text_fr: str = "0.52fr",
    img_fr: str = "0.48fr",
    diagram: bool = False,
    img_left: bool = False,
) -> str:
    if not img:
        return f'<div class="slide pad">{text_html}</div>'
    extra = " diagram" if diagram else ""
    cols = (
        f'<div class="img-col">{img_tag(img, diagram)}</div>'
        f'<div class="text-col">{text_html}</div>'
        if img_left
        else f'<div class="text-col">{text_html}</div>'
        f'<div class="img-col">{img_tag(img, diagram)}</div>'
    )
    return f'<div class="split{extra}" style="grid-template-columns:{text_fr} {img_fr}">{cols}</div>'


def slide_cover(img: ResolvedImage | None) -> str:
    chips = ["배경·목표", "플랫폼", "연구방법", "기관별 역할", "추진전략", "사업화"]
    chip_html = "".join(f'<span class="chip">{e(c)}</span>' for c in chips)
    if img:
        css = """
body { display: grid; grid-template-columns: 1fr 1fr; }
.left {
  background: linear-gradient(155deg, #0f2d4a 0%, #1F4E79 45%, #2E75B6 100%);
  padding: 48px 52px 48px 64px; display: flex; flex-direction: column; justify-content: center;
}
.left .kicker { color: #8ec5f0; font-size: 16px; margin-bottom: 20px; }
.left h1 { font-size: 38px; font-weight: 800; color: #fff; line-height: 1.32; margin-bottom: 28px; }
.left .meta { font-size: 19px; color: #c5dff5; line-height: 2; margin-bottom: 28px; }
.chips { display: flex; flex-wrap: wrap; gap: 10px; }
.chip { font-size: 14px; font-weight: 600; color: #d4e8f8; padding: 8px 16px; border: 1px solid rgba(255,255,255,.4); border-radius: 22px; }
.right { position: relative; overflow: hidden; }
.right img { width: 100%; height: 100%; object-fit: cover; }
.right .overlay {
  position: absolute; inset: 0; background: linear-gradient(90deg, rgba(15,45,74,.85) 0%, rgba(15,45,74,.2) 55%, transparent 100%);
  display: flex; flex-direction: column; justify-content: flex-end; padding: 40px 44px;
}
.right .stat { font-size: 48px; font-weight: 800; color: #fff; }
.right .lbl { font-size: 17px; color: #c5dff5; margin-top: 8px; }
"""
        hero = f'<img src="{html_src(img)}" alt="{e(img.alt)}">'
        body = f"""
<div class="left">
  <div class="kicker">기계장비산업기술개발사업 · 제조기반생산시스템</div>
  <h1>인공지능 기반 무인 자율 굴착기 개발을 위한<br>초실감 디지털 트윈 플랫폼 개발</h1>
  <div class="meta">주관 ㈜싸이언 · 연구책임자 강만수<br>2026.06 – 2029.12 · TRL 3→7</div>
  <div class="chips">{chip_html}</div>
</div>
<div class="right">{hero}<div class="overlay"><div class="stat">약 62억</div><div class="lbl">총 연구개발비 · 3종 건설기계 통합</div></div></div>
"""
        return page("표지", body, css)

    css = """
body {
  background: linear-gradient(155deg, #0f2d4a 0%, #1F4E79 45%, #2E75B6 100%);
  display: flex; flex-direction: column; justify-content: center; padding: 56px 80px;
}
.kicker { color: #8ec5f0; font-size: 17px; font-weight: 700; letter-spacing: .1em; margin-bottom: 24px; }
h1 { font-size: 46px; font-weight: 800; color: #fff; line-height: 1.28; margin-bottom: 32px; max-width: 1000px; }
.meta { font-size: 21px; color: #c5dff5; line-height: 2; margin-bottom: 36px; }
.stats { display: flex; gap: 48px; margin-bottom: 36px; }
.stats .n { font-size: 52px; font-weight: 800; color: #fff; }
.stats .l { font-size: 16px; color: #a8d4f5; margin-top: 6px; }
.chips { display: flex; flex-wrap: wrap; gap: 10px; }
.chip { font-size: 14px; font-weight: 600; color: #d4e8f8; padding: 8px 16px; border: 1px solid rgba(255,255,255,.4); border-radius: 22px; }
"""
    body = f"""
<div class="kicker">기계장비산업기술개발사업 · 제조기반생산시스템</div>
<h1>인공지능 기반 무인 자율 굴착기 개발을 위한<br>초실감 디지털 트윈 플랫폼 개발</h1>
<div class="meta">주관 ㈜싸이언 · 연구책임자 강만수<br>2026.06 – 2029.12 · TRL 3→7</div>
<div class="stats">
  <div><div class="n">약 62억</div><div class="l">총 연구개발비</div></div>
  <div><div class="n">3종</div><div class="l">건설기계 DT 통합</div></div>
  <div><div class="n">TRL 3→7</div><div class="l">4개 게이트 실증</div></div>
</div>
<div class="chips">{chip_html}</div>
"""
    return page("표지", body, css)


def slide_background(img: ResolvedImage | None) -> str:
    text = """
  <div class="kicker">01 · 필요성</div>
  <h1 class="headline">건설현장 <em>디지털 전환</em>과<br>자율 건설기계 수요</h1>
  <ul class="body">
    <li>실차 시제·현장 반복시험 → 비용·시간·안전 한계</li>
    <li>생산성 연 1% · 중대재해 3배 · 고령화 14%→27%</li>
    <li>디지털 트윈 CAGR 41.4% · 자율 건설장비 급성장</li>
    <li>Komatsu·Caterpillar·NVIDIA 글로벌 경쟁 가속</li>
  </ul>
"""
    return page("개발 배경", split_slide(text, img, text_fr="0.46fr", img_fr="0.54fr"))


def slide_platform(img: ResolvedImage | None) -> str:
    text = """
  <div class="kicker">02 · 기술 정의</div>
  <h1 class="headline"><em>초실감 디지털 트윈</em><br>통합 플랫폼</h1>
  <ul class="body compact">
    <li>굴착기·고소작업대·로더 유압·동역학·토사·AI 통합</li>
    <li>Omniverse·Isaac Sim·Cosmos + FMI FMU 연계</li>
    <li>Sim-to-Real → KICT Proving Ground 실증</li>
    <li>학습·검증·실증 가상화 (HW 제작 아님)</li>
  </ul>
"""
    return page("플랫폼 정의", split_slide(text, img, text_fr="0.38fr", img_fr="0.62fr", diagram=True))


def slide_goals_performance() -> str:
    """Merged goals + KPI table — reduces one sparse slide."""
    css = """
.pad { padding: 36px 56px 32px; }
.top { display: grid; grid-template-columns: 1fr 1fr; gap: 28px 48px; margin-bottom: 20px; }
.stats { display: flex; gap: 16px; margin-bottom: 18px; }
.stat { flex: 1; text-align: center; padding: 18px 10px; background: #f4f7fb; border-radius: 12px; }
.stat .n { font-size: 44px; font-weight: 800; color: #1F4E79; }
.stat .l { font-size: 15px; color: #4b5563; margin-top: 8px; font-weight: 600; }
.tbl { font-size: 14px; }
.tbl td:nth-child(3) { text-align: center; font-weight: 700; color: #1F4E79; }
.headline { font-size: 32px; margin-bottom: 16px; }
.subhead { font-size: 18px; }
"""
    rows = [
        ("디지털 트윈 물리 거동 일치도", "50→≥90%"),
        ("Omniverse USD 렌더링", "30→≥60 FPS"),
        ("Jetson Orin 추론 응답", "100→≤50 ms"),
        ("AI 무인작업 / Sim-to-Real", "≥90%"),
    ]
    tr = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in rows)
    body = f"""
<div class="slide pad">
  <div class="kicker">03 · 목표 및 KPI</div>
  <h1 class="headline">개발 <em>목표</em> · 성능 지표</h1>
  <div class="stats">
    <div class="stat"><div class="n">≥90%</div><div class="l">물리 일치도</div></div>
    <div class="stat"><div class="n">≥90%</div><div class="l">무인작업 성공률</div></div>
    <div class="stat"><div class="n">≥90%</div><div class="l">실차 전이율</div></div>
    <div class="stat"><div class="n">3종</div><div class="l">DT 모델</div></div>
  </div>
  <div class="top">
    <div>
      <div class="subhead">디지털 트윈</div>
      <ul class="body compact">
        <li>OpenUSD 3종 · FMI FMU · MQTT·ROS2 ≤30ms</li>
        <li>Two-Track RL + Sequential KT</li>
      </ul>
    </div>
    <div>
      <div class="subhead">핵심 KPI (1→4차년도)</div>
      <table class="tbl"><tbody>{tr}</tbody></table>
    </div>
  </div>
</div>
"""
    return page("개발 목표", body, css)


def slide_method(img: ResolvedImage | None) -> str:
    text = """
  <div class="kicker">04 · 연구방법</div>
  <h1 class="headline"><em>Two-Track</em><br>학습·검증</h1>
  <ul class="body compact">
    <li>Track 1: Isaac Sim 병렬 RL</li>
    <li>Track 2: Amesim FMU + 토사 FMU Co-sim</li>
    <li>AB 비교 · Sequential KT 30~50% 단축</li>
    <li>MIL→SIL→PIL→HIL→실차 V&V</li>
  </ul>
"""
    return page("연구방법", split_slide(text, img, text_fr="0.36fr", img_fr="0.64fr", diagram=True))


def slide_strategy(img: ResolvedImage | None) -> str:
    css = """
.pad.strat { padding: 40px 56px 36px; }
.timeline { display: flex; position: relative; margin: 20px 0 24px; }
.timeline::before { content: ''; position: absolute; top: 16px; left: 4%; right: 4%; height: 4px; background: #c5d4e8; }
.gate { flex: 1; text-align: center; position: relative; z-index: 1; }
.gate .dot { width: 24px; height: 24px; background: #1F4E79; border-radius: 50%; margin: 4px auto 12px; border: 4px solid #fff; box-shadow: 0 0 0 2px #1F4E79; }
.gate .when { font-size: 17px; font-weight: 800; color: #1F4E79; }
.gate .what { font-size: 15px; color: #374151; margin-top: 8px; line-height: 1.45; padding: 0 8px; }
.mini { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 8px; }
.mini .col { padding: 18px 20px; background: #f4f7fb; border-radius: 12px; }
.mini h3 { font-size: 17px; font-weight: 700; color: #1F4E79; margin-bottom: 8px; }
.mini p { font-size: 16px; line-height: 1.55; color: #374151; }
.headline { font-size: 34px; margin-bottom: 8px; }
"""
    text = """
  <div class="kicker">05 · 추진전략</div>
  <h1 class="headline">4개 <em>게이트</em> (TRL 3→7)</h1>
  <div class="timeline">
    <div class="gate"><div class="dot"></div><div class="when">'26 Q4</div><div class="what">DT v1·PoC</div></div>
    <div class="gate"><div class="dot"></div><div class="when">'27 Q4</div><div class="what">KOLAS·AB</div></div>
    <div class="gate"><div class="dot"></div><div class="when">'28 Q4</div><div class="what">굴착기·로더</div></div>
    <div class="gate"><div class="dot"></div><div class="when">'29 Q3</div><div class="what">3종 OEM</div></div>
  </div>
  <div class="mini">
    <div class="col"><h3>Sequential KT</h3><p>고소→굴착→로더 학습 30~50% 단축</p></div>
    <div class="col"><h3>V&V 5단</h3><p>9 시나리오×5단 = 45 검증 셀</p></div>
  </div>
"""
    if img:
        css += """
.split.strat { grid-template-columns: 0.58fr 0.42fr; }
.text-col .timeline { margin-top: 8px; }
.gate .when { font-size: 14px; }
.gate .what { font-size: 12px; }
.mini { grid-template-columns: 1fr; gap: 10px; }
.mini .col { padding: 14px 16px; }
.mini h3 { font-size: 15px; }
.mini p { font-size: 14px; }
.headline { font-size: 30px; margin-bottom: 12px; }
"""
        body = split_slide(text, img, text_fr="0.58fr", img_fr="0.42fr")
        body = body.replace('class="split"', 'class="split strat"', 1)
        return page("추진전략", body, css)
    body = f'<div class="slide pad strat">{text}</div>'
    return page("추진전략", body, css)


def slide_roles(img: ResolvedImage | None) -> str:
    css = """
.tbl { font-size: 16px; }
.tbl td:first-child { font-weight: 700; color: #1F4E79; width: 9%; }
.headline { font-size: 34px; margin-bottom: 18px; }
.split.roles { grid-template-columns: 0.62fr 0.38fr; }
.split.roles .tbl { font-size: 14px; }
.split.roles .headline { font-size: 30px; margin-bottom: 14px; }
"""
    rows = [
        ("주관", "㈜싸이언", "강만수", "DT·AI·Cosmos·통합"),
        ("공동1", "㈜거비메타", "신대영", "STEP·시뮬·FMU"),
        ("공동2", "KICT", "오윤석", "Proving Ground·KOLAS"),
        ("공동3", "울산대", "안경관", "토사 FMU·DEM"),
        ("공동4", "인하대", "이철희", "상위제어기·HTN"),
        ("공동5", "융기원", "홍성훈", "통합 인터페이스"),
    ]
    tr = "".join(f"<tr><td>{e(r)}</td><td>{e(n)}</td><td>{e(p)}</td><td>{e(role)}</td></tr>" for r, n, p, role in rows)
    text = f"""
  <div class="kicker">06 · 추진체계</div>
  <h1 class="headline">기관별 <span class="accent">역할</span></h1>
  <table class="tbl"><thead><tr><th>구분</th><th>기관</th><th>책임자</th><th>역할</th></tr></thead><tbody>{tr}</tbody></table>
"""
    if img:
        body = split_slide(text, img, text_fr="0.62fr", img_fr="0.38fr")
        body = body.replace('class="split"', 'class="split roles"', 1)
        return page("기관별 역할", body, css)
    return page("기관별 역할", f'<div class="slide pad">{text}</div>', css)


def slide_orgs_combined(img_partners: ResolvedImage | None, img_univ: ResolvedImage | None) -> str:
    """Merged org slides — bindata band only when a figure is assigned."""
    css = """
body { padding: 32px 48px 28px; display: flex; flex-direction: column; height: 720px; }
.headline { font-size: 30px; margin-bottom: 14px; }
.grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; flex: 1; min-height: 0; }
.org { padding: 16px 18px; background: #f4f7fb; border-radius: 12px; overflow: hidden; }
.org h3 { font-size: 16px; font-weight: 700; color: #1F4E79; margin-bottom: 8px; }
.org .body { font-size: 14px; }
.org .body li { margin-bottom: 6px; }
.img-band { margin-top: 14px; height: 168px; background: #eef3f9; border-radius: 10px; overflow: hidden; display: flex; align-items: center; justify-content: center; }
.img-band img { width: 100%; height: 100%; object-fit: contain; padding: 8px; }
"""
    img_html = ""
    if img_partners and img_univ:
        css += """
.imgs { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px; height: 150px; }
.imgs .frame { background: #eef3f9; border-radius: 10px; overflow: hidden; display: flex; align-items: center; justify-content: center; }
.imgs img { width: 100%; height: 100%; object-fit: cover; }
.imgs .frame.contain img { object-fit: contain; padding: 6px; }
"""
        img_html = f"""<div class="imgs">
  <div class="frame contain">{img_tag(img_partners)}</div>
  <div class="frame">{img_tag(img_univ)}</div>
</div>"""
    elif img_partners:
        img_html = f'<div class="img-band">{img_tag(img_partners, diagram=True)}</div>'
    body = f"""
<div class="kicker">07 · 수행기관</div>
<h1 class="headline">주관 · 공동기관 <em>핵심 역량</em></h1>
<div class="grid">
  <div class="org"><h3>㈜싸이언 (주관)</h3><ul class="body compact"><li>DT 플랫폼·Isaac Sim·Cosmos</li><li>Track 1·2 RL · AB 비교</li><li>데이터 로거 · OEM 패키지</li></ul></div>
  <div class="org"><h3>㈜거비메타</h3><ul class="body compact"><li>시뮬레이터·굴토 100h+</li><li>STEP 3종 · 유압 FMU</li><li>Point Cloud 지형</li></ul></div>
  <div class="org"><h3>KICT</h3><ul class="body compact"><li>연천 Proving Ground 69만㎡</li><li>실차 V&V · KOLAS</li><li>안전·시험 기준</li></ul></div>
  <div class="org"><h3>울산대</h3><ul class="body compact"><li>토사 FMU · DEM·ROM</li><li>토사 물성 DB</li></ul></div>
  <div class="org"><h3>인하대</h3><ul class="body compact"><li>상위제어기 · HTN</li><li>HPC 시제품</li></ul></div>
  <div class="org"><h3>융기원</h3><ul class="body compact"><li>센서-제어-관제 검증</li><li>실험실 연계</li></ul></div>
</div>
{img_html}
"""
    return page("수행기관", body, css)


def slide_y1_commercialization(img_y1: ResolvedImage | None, img_comm: ResolvedImage | None) -> str:
    """Merge Y1 plan + commercialization — text-only when no bindata."""
    css = """
body { display: grid; grid-template-columns: 1fr 1fr; height: 720px; }
.panel { padding: 40px 44px; display: flex; flex-direction: column; justify-content: center; }
.panel.right { background: #f7f9fc; border-left: 1px solid #e3e6ea; }
.headline { font-size: 30px; margin-bottom: 18px; }
.kpi .tbl { font-size: 16px; margin-top: 16px; }
.kpi .tbl td:last-child { font-weight: 800; color: #1F4E79; text-align: right; }
.highlight { margin-top: 20px; padding: 16px 20px; background: #eef3f9; border-left: 4px solid #1F4E79; font-size: 16px; line-height: 1.55; }
.body.compact li { font-size: 17px; }
"""
    body = """
<div class="panel">
  <div class="kicker">08 · 1차년도</div>
  <h1 class="headline">플랫폼 v1 · PoC</h1>
  <ul class="body compact">
    <li>DT v1 · Track 1·2 RL (9 시나리오)</li>
    <li>FMU v1 · Cosmos · 100h+ 굴토데이터</li>
    <li>Gate 1 · KICT Proving Ground</li>
  </ul>
  <div class="kpi">
    <table class="tbl"><tbody>
      <tr><td>USD 폴리곤</td><td>200만+</td></tr>
      <tr><td>유압 FMU</td><td>≤15ms</td></tr>
      <tr><td>병렬 환경</td><td>4,096</td></tr>
    </tbody></table>
  </div>
</div>
<div class="panel right">
  <div class="kicker">09 · 사업화</div>
  <h1 class="headline">OEM · 라이센싱</h1>
  <ul class="body compact">
    <li>고소작업대 OEM (Gate 2)</li>
    <li>3종 통합 패키지 · 매출 25억</li>
    <li>기술이전·SaaS · FMI 표준</li>
  </ul>
  <div class="highlight"><strong>TRL 7</strong> · KOLAS 완료 → 즉시 상용화</div>
</div>
"""
    return page("Y1·사업화", body, css)


def slide_budget() -> str:
    css = """
.pad { padding: 38px 56px 34px; }
.summary { display: flex; gap: 24px; margin-bottom: 22px; }
.sum-item { flex: 1; padding: 22px 24px; background: #f4f7fb; border-radius: 14px; }
.sum-item .n { font-size: 38px; font-weight: 800; color: #1F4E79; }
.sum-item .l { font-size: 16px; color: #4b5563; margin-top: 8px; font-weight: 600; }
.tbl { font-size: 17px; flex: 1; }
.tbl td:nth-child(n+2) { text-align: right; font-weight: 600; }
"""
    body = """
<div class="slide pad">
  <div class="kicker">10 · 연구개발비</div>
  <h1 class="headline">총괄 예산 · 단계별 배분</h1>
  <div class="summary">
    <div class="sum-item"><div class="n">6,196,882</div><div class="l">총 R&D (천원) · 약 62억</div></div>
    <div class="sum-item"><div class="n">4,112,000</div><div class="l">정부지원 4개년</div></div>
    <div class="sum-item"><div class="n">1,320,563</div><div class="l">1차년도 합계</div></div>
  </div>
  <table class="tbl">
    <thead><tr><th>연차</th><th>정부지원</th><th>기관부담</th><th>합계</th></tr></thead>
    <tbody>
      <tr><td>1차년도</td><td>1,028,000</td><td>292,563</td><td>1,320,563</td></tr>
      <tr><td>2차년도</td><td>1,028,000</td><td>300,171</td><td>1,328,171</td></tr>
      <tr><td>3차년도</td><td>1,028,000</td><td>—</td><td>1,028,000+</td></tr>
      <tr><td>4차년도</td><td>1,028,000</td><td>—</td><td>1,028,000+</td></tr>
    </tbody>
  </table>
</div>
"""
    return page("연구개발비", body, css)


def slide_impact(img: ResolvedImage | None) -> str:
    css = """
.pad.impact .cols { display: grid; grid-template-columns: 1fr 1fr; gap: 20px 40px; margin-top: 8px; }
.pad.impact .item { padding: 18px 0; border-bottom: 1px solid #e8eaed; }
.pad.impact .item strong { font-size: 18px; color: #1F4E79; display: block; margin-bottom: 6px; }
.pad.impact .item span { font-size: 17px; color: #374151; line-height: 1.5; }
.headline { font-size: 34px; }
"""
    text = """
  <div class="kicker">11 · 기대효과</div>
  <h1 class="headline">과학기술 · 산업 · 사회</h1>
  <div class="cols">
    <div class="item"><strong>기술</strong><span>Physical AI ≤50ms · ≥90% 정밀성</span></div>
    <div class="item"><strong>경제</strong><span>OEM 패키지 · 신규 시장</span></div>
    <div class="item"><strong>사회</strong><span>무인화 · 중대재해 예방</span></div>
    <div class="item"><strong>정책</strong><span>미래모빌리티 초격차 직결</span></div>
    <div class="item" style="grid-column:1/-1"><strong>확장</strong><span>농기계·방산·광산 수평 전개</span></div>
  </div>
"""
    if img:
        text_list = """
  <div class="kicker">11 · 기대효과</div>
  <h1 class="headline">과학기술 · 산업 · 사회</h1>
  <ul class="body compact">
    <li><strong style="color:#1F4E79">기술</strong> — Physical AI ≤50ms · ≥90% 정밀성</li>
    <li><strong style="color:#1F4E79">경제</strong> — OEM 패키지 · 신규 시장</li>
    <li><strong style="color:#1F4E79">사회</strong> — 무인화 · 중대재해 예방</li>
    <li><strong style="color:#1F4E79">정책</strong> — 미래모빌리티 초격차 직결</li>
    <li><strong style="color:#1F4E79">확장</strong> — 농기계·방산·광산 수평 전개</li>
  </ul>
"""
        return page("기대효과", split_slide(text_list, img, text_fr="0.55fr", img_fr="0.45fr"))
    return page("기대효과", f'<div class="slide pad impact">{text}</div>', css)


def slide_closing() -> str:
    css = """
body { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
  background: linear-gradient(155deg, #0f2d4a 0%, #1F4E79 50%, #2E75B6 100%); }
h1 { font-size: 64px; font-weight: 800; color: #fff; margin-bottom: 28px; }
.sub { font-size: 22px; color: #c5dff5; max-width: 900px; line-height: 1.65; margin-bottom: 40px; }
.orgs { font-size: 18px; color: #8ec5f0; line-height: 2; }
"""
    body = """
<h1>감사합니다</h1>
<p class="sub">인공지능 기반 무인 자율 굴착기 개발을 위한<br>초실감 디지털 트윈 플랫폼 개발</p>
<div class="orgs">㈜싸이언 · ㈜거비메타 · KICT · 울산대 · 인하대 · 융기원</div>
"""
    return page("감사합니다", body, css)


def main() -> None:
    print(f"Resolving bindata images for '{STEM}'...")
    images = resolve_all(STEM, SCIEN_IMAGE_SPECS)
    for sid, img in images.items():
        print(f"  [{sid}] {img.rel_path} ({img.width}x{img.height})")

    def g(sid: str) -> ResolvedImage | None:
        return images.get(sid)

    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()

    files = [
        ("01-cover-표지.html", slide_cover(None)),
        ("02-background-개발배경.html", slide_background(g("background"))),
        ("03-platform-플랫폼정의.html", slide_platform(g("platform"))),
        ("04-goals_performance-목표-KPI.html", slide_goals_performance()),
        ("05-method-연구방법.html", slide_method(g("method"))),
        ("06-strategy-추진전략.html", slide_strategy(None)),
        ("07-roles-기관별역할.html", slide_roles(None)),
        ("08-orgs-수행기관.html", slide_orgs_combined(g("org_partners"), None)),
        ("09-y1_commercialization-연차-사업화.html", slide_y1_commercialization(None, None)),
        ("10-budget-연구개발비.html", slide_budget()),
        ("11-impact-기대효과.html", slide_impact(None)),
        ("12-closing-감사합니다.html", slide_closing()),
    ]
    for name, content in files:
        (OUT / name).write_text(content, encoding="utf-8")

    index = (
        '<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><title>미리보기</title>'
        "<style>body{font-family:'Malgun Gothic',sans-serif;padding:24px}"
        "a{display:block;padding:6px 0;color:#1F4E79}</style></head><body>"
        f"<h2>초실감 디지털 트윈 ({len(files)} slides)</h2>"
    )
    for name, _ in files:
        index += f'<a href="{name}">{name}</a>\n'
    index += "</body></html>"
    (OUT / "index.html").write_text(index, encoding="utf-8")
    print(f"Wrote {len(files)} slides to {OUT}")


if __name__ == "__main__":
    main()
