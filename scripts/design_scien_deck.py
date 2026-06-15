#!/usr/bin/env python3
"""Polished editorial deck for Scien digital-twin R&D plan (from input.pdf)."""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "slides"
IMG = "../templates/extracted/input-hwp-full/bindata"

BASE = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1280px; height: 720px; overflow: hidden;
  font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
  background: #ffffff; color: #16181d;
}
.kicker { font-size: 14px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #6b7280; }
.headline { font-size: 34px; font-weight: 800; line-height: 1.22; color: #16181d; }
.headline em { color: #1F4E79; font-style: normal; }
.body { font-size: 17px; line-height: 1.58; color: #2c2f36; list-style: none; }
.body li { margin-bottom: 10px; padding-left: 1.15em; text-indent: -1.15em; }
.body li::before { content: "○ "; color: #2E75B6; font-weight: 700; }
.body.compact li { font-size: 16px; margin-bottom: 8px; }
.tbl { width: 100%; border-collapse: collapse; font-size: 15px; }
.tbl th { text-align: left; font-weight: 700; color: #1F4E79; border-bottom: 2px solid #1F4E79; padding: 10px 12px; }
.tbl td { border-bottom: 1px solid #e3e6ea; padding: 9px 12px; vertical-align: top; }
.hr { border: 0; border-top: 1px solid #e3e6ea; margin: 20px 0; }
"""


def e(s: str) -> str:
    return html.escape(str(s or ""), quote=True)


def page(title: str, body: str, css: str = "") -> str:
    return (
        f'<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n'
        f"<title>{e(title)}</title>\n<style>\n{BASE}{css}\n</style>\n</head>\n"
        f"<body>{body}\n</body>\n</html>\n"
    )


def slide_cover() -> str:
    chips = ["배경·목표", "플랫폼", "연구방법", "추진전략", "수행기관", "사업화"]
    chip_html = "".join(f'<span class="chip">{e(c)}</span>' for c in chips)
    css = """
body {
  background: linear-gradient(152deg, #0f2d4a 0%, #1F4E79 48%, #2E75B6 100%);
  display: flex; flex-direction: column; justify-content: center; padding: 64px 88px;
}
.kicker { color: #8ec5f0; font-size: 16px; margin-bottom: 22px; }
h1 { font-size: 48px; font-weight: 800; color: #fff; line-height: 1.28; max-width: 1040px; margin-bottom: 32px; }
.meta { font-size: 20px; color: #c5dff5; line-height: 2; margin-bottom: 36px; }
.stats { display: flex; gap: 56px; margin-bottom: 36px; }
.stats .n { font-size: 54px; font-weight: 800; color: #fff; line-height: 1; }
.stats .l { font-size: 15px; color: #a8d4f5; margin-top: 8px; }
.chips { display: flex; flex-wrap: wrap; gap: 10px; }
.chip { font-size: 14px; font-weight: 600; color: #d4e8f8; padding: 8px 16px; border: 1px solid rgba(255,255,255,.35); border-radius: 22px; }
"""
    body = f"""
<div class="kicker">기계장비산업기술개발사업 · 제조기반생산시스템</div>
<h1>인공지능 기반 무인 자율 굴착기 개발을 위한<br>초실감 디지털 트윈 플랫폼 개발</h1>
<div class="meta">주관 ㈜싸이언 · 연구책임자 강만수 · 과제번호 25609645<br>2026.06 – 2029.12 · TRL 3→7</div>
<div class="stats">
  <div><div class="n">약 62억</div><div class="l">총 연구개발비</div></div>
  <div><div class="n">3종</div><div class="l">굴착기·고소·로더 DT</div></div>
  <div><div class="n">6개 기관</div><div class="l">주관·공동 컨소시엄</div></div>
</div>
<div class="chips">{chip_html}</div>
"""
    return page("표지", body, css)


def slide_background() -> str:
    css = """
body { display: flex; flex-direction: column; padding: 48px 64px 40px; }
.top { flex: 0 0 auto; }
.headline { font-size: 32px; margin: 8px 0 18px; }
.chart { flex: 1; min-height: 0; margin-top: 16px; display: flex; align-items: center; justify-content: center; }
.chart img { width: 100%; max-height: 340px; object-fit: contain; }
"""
    body = f"""
<div class="top">
  <div class="kicker">01 · 필요성</div>
  <h1 class="headline">건설현장 <em>디지털 전환</em>과 자율 건설기계 수요</h1>
  <ul class="body compact">
    <li>실차 시제·현장 반복시험 → 비용·시간·안전 한계 — 가상 검증 환경 필요</li>
    <li>생산성 연 1% · 중대재해 3배 · 고령화 14%→27% — 구조적 위기</li>
    <li>Komatsu·Caterpillar·NVIDIA 글로벌 경쟁 가속</li>
  </ul>
</div>
<div class="chart">
  <img src="{IMG}/BIN0006.jpeg" alt="건설업 사회·경제적 현황 — 디지털 전환 필요성">
</div>
"""
    return page("개발 배경", body, css)


def slide_platform() -> str:
    css = """
body { display: grid; grid-template-columns: 0.40fr 0.60fr; height: 720px; }
.text { padding: 48px 40px 48px 64px; display: flex; flex-direction: column; justify-content: center; }
.headline { font-size: 30px; margin: 10px 0 20px; }
.diagram { background: #fafbfc; display: flex; align-items: center; justify-content: center; padding: 20px 24px; }
.diagram img { width: 100%; height: 100%; object-fit: contain; }
"""
    body = f"""
<div class="text">
  <div class="kicker">02 · 기술 정의</div>
  <h1 class="headline"><em>초실감 디지털 트윈</em><br>통합 플랫폼</h1>
  <ul class="body compact">
    <li>굴착기·고소작업대·로더 — 유압·동역학·토사·AI 통합 가상환경</li>
    <li>Omniverse·Isaac Sim·Cosmos + FMI FMU 물리모델 연계</li>
    <li>학습·검증·보정·실증 연계 — HW 제작이 아닌 가상화 플랫폼</li>
    <li>KICT Proving Ground 실차 Sim-to-Real 검증</li>
  </ul>
</div>
<div class="diagram">
  <img src="{IMG}/BIN0001.jpeg" alt="초실감 디지털 트윈 플랫폼 아키텍처 개요">
</div>
"""
    return page("플랫폼 정의", body, css)


def slide_goals() -> str:
    css = """
body { padding: 44px 64px 40px; display: flex; flex-direction: column; }
.headline { font-size: 32px; margin: 8px 0 28px; }
.stats { display: flex; gap: 0; margin-bottom: 28px; }
.stat { flex: 1; text-align: center; padding: 0 16px; border-right: 1px solid #e3e6ea; }
.stat:last-child { border-right: none; }
.stat .n { font-size: 56px; font-weight: 800; color: #1F4E79; line-height: 1; }
.stat .l { font-size: 15px; color: #4b5563; margin-top: 10px; font-weight: 600; }
.cols { display: grid; grid-template-columns: 1fr 1.1fr; gap: 48px; flex: 1; }
.sub { font-size: 18px; font-weight: 700; color: #1F4E79; margin-bottom: 12px; }
.tbl { font-size: 14px; }
.tbl td:nth-child(3), .tbl td:nth-child(4) { text-align: center; font-weight: 700; color: #1F4E79; }
"""
    body = """
<div class="kicker">03 · 목표 및 KPI</div>
<h1 class="headline">3종 DT 플랫폼 · <em>핵심 성능 목표</em></h1>
<div class="stats">
  <div class="stat"><div class="n">≥90%</div><div class="l">물리 일치도</div></div>
  <div class="stat"><div class="n">≥90%</div><div class="l">무인작업 성공률</div></div>
  <div class="stat"><div class="n">≥90%</div><div class="l">Sim-to-Real 전이</div></div>
  <div class="stat"><div class="n">≤30ms</div><div class="l">실차 데이터 연동</div></div>
</div>
<div class="cols">
  <div>
    <div class="sub">개발 목표</div>
    <ul class="body compact">
      <li>OpenUSD 3종 · FMI 2.0/3.0 · MQTT·ROS2 실시간 연동</li>
      <li>Two-Track RL + Sequential KT (30~50% 학습 단축)</li>
      <li>토사 DEM/MPM 작업환경 3종 이상</li>
    </ul>
  </div>
  <div>
    <div class="sub">성능 지표 (1→4차년도)</div>
    <table class="tbl">
      <thead><tr><th>평가 항목</th><th>단위</th><th>1차</th><th>4차 목표</th></tr></thead>
      <tbody>
        <tr><td>디지털 트윈 물리 거동 일치도</td><td>%</td><td>50</td><td>≥90</td></tr>
        <tr><td>Omniverse USD 렌더링</td><td>FPS</td><td>30</td><td>≥60</td></tr>
        <tr><td>Jetson Orin 추론 응답</td><td>ms</td><td>100</td><td>≤50</td></tr>
        <tr><td>AI 무인작업 / Sim-to-Real</td><td>%</td><td>—</td><td>≥90</td></tr>
      </tbody>
    </table>
  </div>
</div>
"""
    return page("개발 목표", body, css)


def slide_method() -> str:
    css = """
body { display: grid; grid-template-columns: 0.36fr 0.64fr; height: 720px; }
.text { padding: 44px 32px 44px 64px; display: flex; flex-direction: column; justify-content: center; }
.headline { font-size: 30px; margin: 10px 0 18px; }
.diagram { display: flex; align-items: center; justify-content: center; padding: 24px 28px 24px 12px; }
.diagram img { width: 100%; height: 100%; object-fit: contain; }
"""
    body = f"""
<div class="text">
  <div class="kicker">04 · 연구방법</div>
  <h1 class="headline"><em>Two-Track</em> 학습·검증</h1>
  <ul class="body compact">
    <li>Track 1: Isaac Sim 병렬 RL (빠른 학습)</li>
    <li>Track 2: Amesim FMU + 토사 FMU Co-simulation (정밀)</li>
    <li>AB 비교 · Sequential KT · 9 시나리오</li>
    <li>MIL→SIL→PIL→HIL→실차 V&V 5단계</li>
  </ul>
</div>
<div class="diagram">
  <img src="{IMG}/BIN0018.jpeg" alt="OpenUSD DT 환경 및 Isaac Sim Two-Track 학습">
</div>
"""
    return page("연구방법", body, css)


def slide_strategy() -> str:
    css = """
body { padding: 48px 64px; display: flex; flex-direction: column; }
.headline { font-size: 34px; margin: 10px 0 36px; }
.timeline { display: flex; position: relative; margin-bottom: 40px; }
.timeline::before { content: ''; position: absolute; top: 18px; left: 5%; right: 5%; height: 3px; background: #c5d4e8; }
.gate { flex: 1; text-align: center; position: relative; z-index: 1; }
.gate .dot { width: 22px; height: 22px; background: #1F4E79; border-radius: 50%; margin: 8px auto 14px; box-shadow: 0 0 0 4px #fff, 0 0 0 6px #1F4E79; }
.gate .when { font-size: 18px; font-weight: 800; color: #1F4E79; }
.gate .what { font-size: 16px; color: #374151; margin-top: 10px; line-height: 1.45; padding: 0 12px; }
.notes { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 8px; }
.notes h3 { font-size: 18px; font-weight: 700; color: #1F4E79; margin-bottom: 10px; }
.notes p { font-size: 16px; line-height: 1.55; color: #374151; }
"""
    body = """
<div class="kicker">05 · 추진전략</div>
<h1 class="headline">4개 <em>게이트</em> — TRL 3→7</h1>
<div class="timeline">
  <div class="gate"><div class="dot"></div><div class="when">'26 Q4</div><div class="what">DT v1·PoC<br>Gate 1</div></div>
  <div class="gate"><div class="dot"></div><div class="when">'27 Q4</div><div class="what">KOLAS·AB 검증<br>고소 OEM</div></div>
  <div class="gate"><div class="dot"></div><div class="when">'28 Q4</div><div class="what">굴착기·로더<br>실차 V&V</div></div>
  <div class="gate"><div class="dot"></div><div class="when">'29 Q3</div><div class="what">3종 통합<br>OEM 패키지</div></div>
</div>
<div class="notes">
  <div><h3>Sequential Knowledge Transfer</h3><p>굴착기→고소작업대→로더 순 학습 이식으로 장비별 신규 학습 시간 30~50% 단축</p></div>
  <div><h3>V&V 5단계 검증</h3><p>9 시나리오 × MIL·SIL·PIL·HIL·실차 = 45 검증 셀 · KICT Proving Ground 실증</p></div>
</div>
"""
    return page("추진전략", body, css)


def slide_roles() -> str:
    rows = [
        ("주관", "㈜싸이언", "강만수", "DT·AI·Cosmos·통합 플랫폼"),
        ("공동1", "㈜거비메타", "신대영", "STEP·시뮬·유압 FMU"),
        ("공동2", "KICT", "오윤석", "Proving Ground·KOLAS"),
        ("공동3", "울산대", "안경관", "토사 FMU·DEM·ROM"),
        ("공동4", "인하대", "이철희", "상위제어기·HTN"),
        ("공동5", "융기원", "홍성훈", "통합 인터페이스·검증"),
    ]
    tr = "".join(
        f"<tr><td>{e(r)}</td><td>{e(n)}</td><td>{e(p)}</td><td>{e(role)}</td></tr>"
        for r, n, p, role in rows
    )
    css = """
body { display: grid; grid-template-columns: 0.58fr 0.42fr; height: 720px; }
.left { padding: 44px 32px 44px 64px; display: flex; flex-direction: column; justify-content: center; }
.headline { font-size: 30px; margin: 10px 0 20px; }
.tbl { font-size: 14px; }
.tbl td:first-child { font-weight: 700; color: #1F4E79; width: 10%; }
.photo { display: flex; align-items: center; justify-content: center; padding: 24px; background: #fafbfc; }
.photo img { width: 100%; height: 100%; object-fit: cover; }
"""
    body = f"""
<div class="left">
  <div class="kicker">06 · 추진체계</div>
  <h1 class="headline">기관별 <em>역할 분담</em></h1>
  <table class="tbl">
    <thead><tr><th>구분</th><th>기관</th><th>책임자</th><th>역할</th></tr></thead>
    <tbody>{tr}</tbody>
  </table>
</div>
<div class="photo">
  <img src="{IMG}/BIN0023.jpeg" alt="Point Cloud 기반 3D 지형 모델링">
</div>
"""
    return page("기관별 역할", body, css)


def slide_orgs() -> str:
    css = """
body { padding: 40px 64px 36px; display: flex; flex-direction: column; }
.headline { font-size: 30px; margin: 8px 0 22px; }
.grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 28px 36px; flex: 1; }
.org h3 { font-size: 17px; font-weight: 700; color: #1F4E79; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 2px solid #1F4E79; }
.org .body { font-size: 15px; }
.org .body li { margin-bottom: 6px; }
"""
    body = """
<div class="kicker">07 · 수행기관</div>
<h1 class="headline">주관·공동기관 <em>핵심 역량</em></h1>
<div class="grid">
  <div class="org"><h3>㈜싸이언 (주관)</h3><ul class="body compact"><li>DT 플랫폼·Isaac Sim·Cosmos</li><li>Track 1·2 RL · AB 비교</li><li>데이터 로거 · OEM 패키지</li></ul></div>
  <div class="org"><h3>㈜거비메타</h3><ul class="body compact"><li>시뮬레이터·굴토 100h+</li><li>STEP 3종 · 유압 FMU</li><li>Point Cloud 지형</li></ul></div>
  <div class="org"><h3>KICT</h3><ul class="body compact"><li>연천 Proving Ground 69만㎡</li><li>실차 V&V · KOLAS</li><li>안전·시험 기준</li></ul></div>
  <div class="org"><h3>울산대</h3><ul class="body compact"><li>토사 FMU · DEM·ROM</li><li>토사 물성 DB 구축</li></ul></div>
  <div class="org"><h3>인하대</h3><ul class="body compact"><li>상위제어기 · HTN</li><li>HPC 시제품</li></ul></div>
  <div class="org"><h3>융기원</h3><ul class="body compact"><li>센서-제어-관제 검증</li><li>실험실 연계</li></ul></div>
</div>
"""
    return page("수행기관", body, css)


def slide_y1_commercialization() -> str:
    css = """
body { display: grid; grid-template-columns: 1fr 1fr; height: 720px; }
.panel { padding: 48px 52px; display: flex; flex-direction: column; justify-content: center; }
.panel.right { border-left: 1px solid #e3e6ea; }
.headline { font-size: 28px; margin: 10px 0 20px; }
.kpi .tbl { font-size: 15px; margin-top: 18px; }
.kpi .tbl td:last-child { font-weight: 800; color: #1F4E79; text-align: right; }
.callout { margin-top: 22px; font-size: 17px; line-height: 1.55; color: #1F4E79; font-weight: 700; }
"""
    body = """
<div class="panel">
  <div class="kicker">08 · 1차년도</div>
  <h1 class="headline">플랫폼 v1 · PoC</h1>
  <ul class="body compact">
    <li>DT v1 · Track 1·2 RL (9 시나리오)</li>
    <li>FMU v1 · Cosmos · 100h+ 굴토 데이터</li>
    <li>Gate 1 · KICT Proving Ground 실증</li>
  </ul>
  <div class="kpi">
    <table class="tbl"><tbody>
      <tr><td>USD 폴리곤</td><td>200만+</td></tr>
      <tr><td>유압 FMU 응답</td><td>≤15ms</td></tr>
      <tr><td>병렬 학습 환경</td><td>4,096</td></tr>
    </tbody></table>
  </div>
</div>
<div class="panel right">
  <div class="kicker">09 · 사업화</div>
  <h1 class="headline">OEM · 라이센싱</h1>
  <ul class="body compact">
    <li>고소작업대 OEM 라이센싱 (Gate 2 조기 가시화)</li>
    <li>3종 통합 패키지 · 국내외 OEM 공급</li>
    <li>FMI 표준 기반 기술이전·SaaS</li>
  </ul>
  <p class="callout">TRL 7 · KOLAS 완료 → 즉시 상용화 연계</p>
</div>
"""
    return page("연차·사업화", body, css)


def slide_budget() -> str:
    css = """
body { padding: 42px 64px 38px; display: flex; flex-direction: column; }
.headline { font-size: 32px; margin: 8px 0 24px; }
.summary { display: flex; gap: 48px; margin-bottom: 28px; padding-bottom: 24px; border-bottom: 1px solid #e3e6ea; }
.sum .n { font-size: 42px; font-weight: 800; color: #1F4E79; line-height: 1; }
.sum .l { font-size: 15px; color: #4b5563; margin-top: 8px; font-weight: 600; }
.tbl { font-size: 16px; flex: 1; }
.tbl td:nth-child(n+2) { text-align: right; font-weight: 600; }
"""
    body = """
<div class="kicker">10 · 연구개발비</div>
<h1 class="headline">총괄 예산 · 단계별 배분</h1>
<div class="summary">
  <div class="sum"><div class="n">6,196,882</div><div class="l">총 R&D (천원) · 약 62억</div></div>
  <div class="sum"><div class="n">4,112,000</div><div class="l">정부지원 (4개년)</div></div>
  <div class="sum"><div class="n">1,320,563</div><div class="l">1차년도 합계</div></div>
</div>
<table class="tbl">
  <thead><tr><th>연차</th><th>정부지원 (천원)</th><th>기관부담 (천원)</th><th>합계 (천원)</th></tr></thead>
  <tbody>
    <tr><td>1차년도</td><td>1,028,000</td><td>292,563</td><td>1,320,563</td></tr>
    <tr><td>2차년도</td><td>1,028,000</td><td>300,171</td><td>1,328,171</td></tr>
    <tr><td>3차년도</td><td>1,028,000</td><td>—</td><td>1,028,000+</td></tr>
    <tr><td>4차년도</td><td>1,028,000</td><td>—</td><td>1,028,000+</td></tr>
  </tbody>
</table>
"""
    return page("연구개발비", body, css)


def slide_impact() -> str:
    css = """
body { padding: 48px 64px; display: flex; flex-direction: column; }
.headline { font-size: 34px; margin: 10px 0 32px; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 0 56px; }
.item { padding: 20px 0; border-bottom: 1px solid #e8eaed; }
.item strong { font-size: 18px; color: #1F4E79; display: block; margin-bottom: 8px; }
.item span { font-size: 17px; color: #374151; line-height: 1.52; }
.item.wide { grid-column: 1 / -1; }
"""
    body = """
<div class="kicker">11 · 기대효과</div>
<h1 class="headline">과학기술 · 산업 · 사회</h1>
<div class="cols">
  <div class="item"><strong>기술</strong><span>Physical AI ≤50ms · ≥90% 정밀성 · FMI 표준 통합 DT</span></div>
  <div class="item"><strong>경제</strong><span>OEM 가상개발 패키지 · 개발기간 30%·비용 50% 절감</span></div>
  <div class="item"><strong>사회</strong><span>무인화 · 중대재해 예방 · 극한환경 현장 투입</span></div>
  <div class="item"><strong>정책</strong><span>미래모빌리티 초격차 · 건설·농기계 완전 무인화 직결</span></div>
  <div class="item wide"><strong>확장</strong><span>농기계·방산·광산 등 토사 상호작용 인접 산업 수평 전개</span></div>
</div>
"""
    return page("기대효과", body, css)


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
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()

    files = [
        ("01-cover-표지.html", slide_cover()),
        ("02-background-개발배경.html", slide_background()),
        ("03-platform-플랫폼정의.html", slide_platform()),
        ("04-goals-목표-KPI.html", slide_goals()),
        ("05-method-연구방법.html", slide_method()),
        ("06-strategy-추진전략.html", slide_strategy()),
        ("07-roles-기관별역할.html", slide_roles()),
        ("08-orgs-수행기관.html", slide_orgs()),
        ("09-y1_commercialization-연차-사업화.html", slide_y1_commercialization()),
        ("10-budget-연구개발비.html", slide_budget()),
        ("11-impact-기대효과.html", slide_impact()),
        ("12-closing-감사합니다.html", slide_closing()),
    ]
    for name, content in files:
        (OUT / name).write_text(content, encoding="utf-8")

    index = (
        '<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">'
        '<title>초실감 디지털 트윈 — 미리보기</title>'
        "<style>body{font-family:'Malgun Gothic',sans-serif;padding:28px 32px;max-width:720px}"
        "h2{color:#1F4E79;margin-bottom:16px}"
        "a{display:block;padding:7px 0;color:#2E75B6;text-decoration:none;font-size:15px}"
        "a:hover{text-decoration:underline}</style></head><body>"
        f"<h2>초실감 디지털 트윈 플랫폼 ({len(files)} slides)</h2>"
    )
    for name, _ in files:
        index += f'<a href="{name}">{name}</a>\n'
    index += "</body></html>"
    (OUT / "index.html").write_text(index, encoding="utf-8")
    print(f"Wrote {len(files)} slides to {OUT}")


if __name__ == "__main__":
    main()
