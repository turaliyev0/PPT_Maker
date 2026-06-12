#!/usr/bin/env python3
"""Generate polished HTML slides from input.pdf extracted content."""
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
.slide {
  width: 100%; height: 100%;
  display: flex; flex-direction: column;
}
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
.fill { flex: 1; display: flex; flex-direction: column; justify-content: center; }
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
    css = """
body { display: grid; grid-template-columns: 1.05fr 0.95fr; }
.left {
  background: linear-gradient(155deg, #0f2d4a 0%, #1F4E79 45%, #2E75B6 100%);
  padding: 48px 52px 48px 64px; display: flex; flex-direction: column; justify-content: center;
  position: relative; overflow: hidden;
}
.left::after {
  content: ''; position: absolute; right: -60px; top: -60px; width: 300px; height: 300px;
  border-radius: 50%; background: rgba(255,255,255,.06);
}
.left .kicker { color: #8ec5f0; font-size: 16px; margin-bottom: 20px; }
.left h1 { font-size: 40px; font-weight: 800; color: #fff; line-height: 1.32; margin-bottom: 28px; position: relative; z-index: 1; }
.meta { font-size: 19px; color: #c5dff5; line-height: 2; margin-bottom: 32px; position: relative; z-index: 1; }
.chips { display: flex; flex-wrap: wrap; gap: 10px; position: relative; z-index: 1; }
.chip {
  font-size: 14px; font-weight: 600; color: #d4e8f8; padding: 8px 16px;
  border: 1px solid rgba(255,255,255,.4); border-radius: 22px;
}
.right {
  background: #f7f9fc; display: flex; flex-direction: column; justify-content: center;
  padding: 44px 48px; border-left: 1px solid #e3e6ea;
}
.right h2 { font-size: 17px; font-weight: 700; color: #6b7280; letter-spacing: .1em; margin-bottom: 28px; }
.stat-row { margin-bottom: 28px; }
.stat-row .num { font-size: 48px; font-weight: 800; color: #1F4E79; line-height: 1; }
.stat-row .lbl { font-size: 17px; color: #4b5563; margin-top: 8px; line-height: 1.4; }
.org-list { font-size: 17px; color: #2c2f36; line-height: 1.85; margin-top: 8px; }
.org-list strong { color: #1F4E79; font-size: 18px; }
"""
    chips = ["배경·목표", "플랫폼", "연구방법", "기관별 역할", "추진전략", "사업화"]
    chip_html = "".join(f'<span class="chip">{e(c)}</span>' for c in chips)
    body = f"""
<div class="left">
  <div class="kicker">기계장비산업기술개발사업 · 제조기반생산시스템</div>
  <h1>인공지능 기반 무인 자율 굴착기 개발을 위한<br>초실감 디지털 트윈 플랫폼 개발</h1>
  <div class="meta">
    주관 ㈜싸이언 · 연구책임자 강만수<br>
    2026.06 – 2029.12 (3년 7개월) · TRL 3→7
  </div>
  <div class="chips">{chip_html}</div>
</div>
<div class="right">
  <h2>PROJECT AT A GLANCE</h2>
  <div class="stat-row"><div class="num">약 62억</div><div class="lbl">총 연구개발비<br>(6,196,882천원)</div></div>
  <div class="stat-row"><div class="num">3종</div><div class="lbl">굴착기 · 고소작업대 · 로더<br>통합 플랫폼</div></div>
  <div class="org-list">
    <strong>공동</strong> 거비메타 · KICT · 울산대 · 인하대 · 융기원<br>
    <strong>수요</strong> 수산세보틱스 · 트림블 · 레디로버
  </div>
</div>
"""
    return page("표지", body, css)


def slide_background() -> str:
    css = """
body { display: grid; grid-template-columns: 0.88fr 1.12fr; height: 720px; }
.text { padding: 44px 36px 44px 56px; display: flex; flex-direction: column; justify-content: center; }
.text .headline { font-size: 34px; margin-bottom: 28px; }
.img-panel { background: #f4f7fb; display: flex; align-items: center; justify-content: center; padding: 24px 28px; height: 100%; }
.img-panel img { width: 100%; height: 100%; object-fit: contain; }
"""
    body = f"""
<div class="text">
  <div class="kicker">01 · 필요성</div>
  <h1 class="headline">건설현장 <em>디지털 전환</em>과<br>자율 건설기계 수요</h1>
  <ul class="body">
    <li>실차 시제·현장 반복시험 의존 → 비용·시간·안전 한계</li>
    <li>생산성 증가율 연 1% · 중대재해 3배 · 고령화 14%→27%</li>
    <li>디지털 트윈 시장 CAGR 41.4% · 자율 건설장비 급성장</li>
    <li>Komatsu·Caterpillar·NVIDIA 글로벌 디지털 전환 경쟁</li>
  </ul>
</div>
<div class="img-panel"><img src="{IMG}/BIN0006.jpeg" alt="건설업 사회경제적 현황"></div>
"""
    return page("개발 배경", body, css)


def slide_platform() -> str:
    css = """
body { display: grid; grid-template-columns: 0.36fr 0.64fr; height: 720px; }
.text { padding: 36px 28px 36px 56px; display: flex; flex-direction: column; justify-content: center; }
.text .headline { font-size: 30px; margin-bottom: 22px; }
.text .body { font-size: 17px; }
.text .body li { margin-bottom: 15px; }
.text .tagline { margin-top: 20px; font-size: 16px; font-weight: 700; color: #1F4E79; line-height: 1.5; padding-top: 16px; border-top: 2px solid #e3e6ea; }
.img-panel { background: #f4f7fb; display: flex; align-items: stretch; justify-content: center; padding: 10px 14px; height: 100%; }
.img-panel img { width: 100%; height: 100%; object-fit: contain; }
"""
    body = f"""
<div class="text">
  <div class="kicker">02 · 기술 정의</div>
  <h1 class="headline"><em>초실감 디지털 트윈</em><br>통합 플랫폼</h1>
  <ul class="body">
    <li>굴착기·고소작업대·로더 유압·동역학·토사·AI 정책 가상 통합</li>
    <li>Omniverse·Isaac Sim·Cosmos + FMI FMU 물리모델 연계</li>
    <li>실차 보정 → Sim-to-Real → KICT Proving Ground 실증</li>
    <li>학습·검증·실증 연계 가상화 플랫폼 (HW 제작 아님)</li>
    <li>ISO 23247 · ASME V&V 40 · OpenUSD 표준 기반 확장</li>
  </ul>
  <p class="tagline">TRL 3→7 · 4차년 OEM 패키지화</p>
</div>
<div class="img-panel"><img src="{IMG}/BIN0001.jpeg" alt="개발 아키텍처 개요도"></div>
"""
    return page("플랫폼 정의", body, css)


def slide_goals() -> str:
    css = """
.pad { padding: 36px 56px 32px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 28px 56px; flex: 1; align-content: stretch; }
.grid > div { display: flex; flex-direction: column; justify-content: center; }
.grid .body { font-size: 18px; }
.grid .subhead { font-size: 22px; }
.stats { display: flex; gap: 18px; margin-top: 22px; }
.stat { flex: 1; text-align: center; padding: 28px 12px; background: #f4f7fb; border-radius: 14px; }
.stat .n { font-size: 56px; font-weight: 800; color: #1F4E79; line-height: 1; }
.stat .l { font-size: 17px; color: #4b5563; margin-top: 12px; line-height: 1.45; font-weight: 600; }
"""
    body = """
<div class="slide pad">
  <div class="kicker">03 · 최종 목표</div>
  <h1 class="headline">3종 건설기계 <em>AI 자율작업</em> 플랫폼 완성</h1>
  <div class="grid">
    <div>
      <div class="subhead">디지털 트윈 플랫폼</div>
      <ul class="body compact">
        <li>OpenUSD 기반 3종 DT · FMI FMU 패키징</li>
        <li>물리·거동 일치도 각 90% 이상</li>
        <li>MQTT·OPC-UA·ROS2 연동 ≤30ms</li>
        <li>건설기계 DT 자산 통합 관리 체계</li>
      </ul>
    </div>
    <div>
      <div class="subhead">AI 학습·자율작업</div>
      <ul class="body compact">
        <li>Two-Track RL + Sequential KT</li>
        <li>무인작업 성공률 90% · Sim-to-Real 90%</li>
        <li>토사환경 3종(진흙·모래·자갈)</li>
        <li>9개 자율작업 시나리오 반복 검증</li>
      </ul>
    </div>
  </div>
  <div class="stats">
    <div class="stat"><div class="n">≥90%</div><div class="l">디지털트윈<br>물리 일치도</div></div>
    <div class="stat"><div class="n">≥90%</div><div class="l">AI 무인작업<br>성공률</div></div>
    <div class="stat"><div class="n">≥90%</div><div class="l">실차 전이<br>성공률</div></div>
    <div class="stat"><div class="n">3종</div><div class="l">굴착기·고소작업대<br>·로더 DT</div></div>
  </div>
</div>
"""
    return page("개발 목표", body, css)


def slide_performance() -> str:
    css = """
.pad { padding: 36px 56px 32px; }
.tbl { font-size: 15px; flex: 1; }
.tbl th, .tbl td { padding: 13px 14px; }
.tbl td:nth-child(3), .tbl td:nth-child(4) { text-align: center; font-weight: 700; color: #1F4E79; }
.note { font-size: 15px; color: #6b7280; margin-top: 14px; }
.headline { margin-bottom: 18px; }
"""
    rows = [
        ("디지털 트윈 물리 거동 일치도", "%", "50→90", "9 시나리오 RMSE · KICT 시험성적서"),
        ("Omniverse USD 렌더링 속도", "FPS", "30→60", "3종 풀 USD 1080p 30분 평균"),
        ("Jetson Orin AGX 추론 응답", "ms", "100→≤50", "FP16 양자화 1000회 평균"),
        ("단순 물리 모델 응답 지연", "ms", "—", "Operating Envelope ≤15"),
        ("AI 무인작업 성공률", "%", "—", "≥90 (4차년도 목표)"),
        ("학습모델 실차 전이 성공률", "%", "—", "≥90 (Iterative Loop)"),
    ]
    tr = "".join(
        f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>"
        for a, b, c, d in rows
    )
    body = f"""
<div class="slide pad">
  <div class="kicker">04 · 성능 목표</div>
  <h1 class="headline">핵심 <em>KPI</em> 및 평가체계</h1>
  <table class="tbl">
    <thead><tr><th style="width:32%">평가 항목</th><th style="width:8%">단위</th><th style="width:14%">1차→4차년도</th><th>평가 방법</th></tr></thead>
    <tbody>{tr}</tbody>
  </table>
  <p class="note">※ ISO 23247 · ASME V&V 40 · KOLAS 시험성적서 기반 단계별 검증</p>
</div>
"""
    return page("성능 목표", body, css)


def slide_method() -> str:
    css = """
body { display: grid; grid-template-columns: 0.38fr 0.62fr; height: 720px; }
.text { padding: 40px 28px 40px 56px; display: flex; flex-direction: column; justify-content: center; }
.text .headline { font-size: 32px; margin-bottom: 22px; }
.text .body { font-size: 17px; }
.text .body li { margin-bottom: 13px; }
.img-panel { background: #f4f7fb; display: flex; align-items: center; padding: 14px 18px; height: 100%; }
.img-panel img { width: 100%; height: 100%; object-fit: contain; }
"""
    body = f"""
<div class="text">
  <div class="kicker">05 · 연구방법</div>
  <h1 class="headline"><em>Two-Track</em><br>학습·검증 체계</h1>
  <ul class="body">
    <li>Track 1: Isaac Sim 병렬 RL — 패턴·인지 정책</li>
    <li>Track 2: Amesim 유압 FMU + 토사 FMU Co-sim</li>
    <li>AB 비교 — 유압 FMU 필요성 95% 신뢰구간</li>
    <li>Sequential KT — 학습시간 30~50% 단축</li>
    <li>MIL→SIL→PIL→HIL→실차 V&V 5단 사슬</li>
  </ul>
</div>
<div class="img-panel"><img src="{IMG}/BIN0018.jpeg" alt="OpenUSD·Isaac Sim 학습환경"></div>
"""
    return page("연구방법", body, css)


def slide_strategy() -> str:
    css = """
.pad { padding: 38px 56px 34px; }
.timeline { display: flex; margin: 8px 0 28px; position: relative; flex: 1; align-items: flex-start; padding-top: 8px; }
.timeline::before { content: ''; position: absolute; top: 36px; left: 6%; right: 6%; height: 4px; background: #c5d4e8; }
.gate { flex: 1; text-align: center; position: relative; z-index: 1; }
.gate .dot { width: 22px; height: 22px; background: #1F4E79; border-radius: 50%; margin: 18px auto 14px; border: 4px solid #fff; box-shadow: 0 0 0 2px #1F4E79; }
.gate .when { font-size: 17px; font-weight: 800; color: #1F4E79; }
.gate .what { font-size: 15px; color: #374151; margin-top: 10px; line-height: 1.5; padding: 0 8px; font-weight: 500; }
.cols { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 22px; }
.col { padding: 22px 24px; background: #f4f7fb; border-radius: 12px; }
.col h3 { font-size: 18px; font-weight: 700; color: #1F4E79; margin-bottom: 12px; }
.col p { font-size: 16px; line-height: 1.58; color: #374151; }
.headline { margin-bottom: 16px; }
"""
    body = """
<div class="slide pad">
  <div class="kicker">06 · 추진전략</div>
  <h1 class="headline">4개 <em>게이트</em> 마일스톤 (TRL 3→7)</h1>
  <div class="timeline">
    <div class="gate"><div class="dot"></div><div class="when">'26 Q4 Gate 1</div><div class="what">DT v1 · Track PoC<br>상위제어기 요구사양</div></div>
    <div class="gate"><div class="dot"></div><div class="when">'27 Q4 Gate 2</div><div class="what">고소작업대 KOLAS<br>AB 비교 · HPC 시제품</div></div>
    <div class="gate"><div class="dot"></div><div class="when">'28 Q4 Gate 3</div><div class="what">굴착기 KOLAS<br>Loop 1·2 · 로더 신규</div></div>
    <div class="gate"><div class="dot"></div><div class="when">'29 Q3 Gate 4</div><div class="what">3종 통합 OEM<br>종합 KOLAS · 실차 90%</div></div>
  </div>
  <div class="cols">
    <div class="col"><h3>Sequential KT</h3><p>고소작업대→굴착기(30% 단축)→로더(50% 단축). PPO·토사 FMU·HTN 계획 이식.</p></div>
    <div class="col"><h3>이중 컴퓨팅</h3><p>Jetson Orin AGX(≤50ms) + HPC 실차탑재 서버. 인지·추론과 고부하 연산 분리.</p></div>
    <div class="col"><h3>V&V 5단 사슬</h3><p>MIL→SIL→PIL→HIL→실차. 3종×3작업 9시나리오×5단 = 45 검증 셀.</p></div>
  </div>
</div>
"""
    return page("추진전략", body, css)


def slide_roles() -> str:
    css = """
.pad { padding: 36px 56px 32px; }
.tbl { font-size: 15px; flex: 1; }
.tbl td:first-child { font-weight: 700; color: #1F4E79; white-space: nowrap; width: 10%; }
.tbl td:nth-child(2) { font-weight: 600; width: 22%; }
.tbl td:nth-child(3) { width: 12%; }
.headline { margin-bottom: 16px; }
"""
    rows = [
        ("주관", "㈜싸이언", "강만수", "DT 플랫폼·AI 학습환경·Cosmos·데이터 로거·통합"),
        ("공동1", "㈜거비메타", "신대영", "STEP·시뮬레이터·굴토데이터·유압 FMU"),
        ("공동2", "한국건설기술연구원", "오윤석", "Proving Ground·실차 V&V·KOLAS 실증"),
        ("공동3", "울산대 산학협력단", "안경관", "토사 DEM·토사해석 FMU·ASME V&V"),
        ("공동4", "인하대 산학협력단", "이철희", "자율형 상위제어기·HTN·안전필터"),
        ("공동5", "차세대융합기술연구원", "홍성훈", "센서-제어기-관제 통합 인터페이스 검증"),
    ]
    tr = "".join(
        f"<tr><td>{e(r)}</td><td>{e(n)}</td><td>{e(p)}</td><td>{e(role)}</td></tr>"
        for r, n, p, role in rows
    )
    body = f"""
<div class="slide pad">
  <div class="kicker">07 · 추진체계</div>
  <h1 class="headline">기관별 <span class="accent">역할</span> 분담</h1>
  <table class="tbl">
    <thead><tr><th>구분</th><th>기관</th><th>책임자</th><th>핵심 역할</th></tr></thead>
    <tbody>{tr}</tbody>
  </table>
</div>
"""
    return page("기관별 역할", body, css)


def slide_org_scien() -> str:
    css = """
.pad { padding: 36px 56px 32px; }
.headline { font-size: 34px; color: #1F4E79; margin-bottom: 20px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px 40px; flex: 1; min-height: 0; }
.block { padding: 32px 36px; background: #f4f7fb; border-radius: 14px; display: flex; flex-direction: column; justify-content: center; min-height: 100%; }
.block .subhead { margin-bottom: 20px; font-size: 22px; border: none; padding: 0; }
.block .body { font-size: 18px; }
.block .body li { margin-bottom: 14px; }
"""
    body = """
<div class="slide pad">
  <div class="kicker">08 · 주관기관</div>
  <h1 class="headline">㈜싸이언 — 디지털트윈 플랫폼 총괄</h1>
  <div class="grid">
    <div class="block">
      <div class="subhead">Y1 핵심 산출</div>
      <ul class="body compact">
        <li>OpenUSD 자산 변환 (폴리곤 200만+)</li>
        <li>Isaac Sim 4,096 병렬 · Track 1·2 RL PoC</li>
        <li>Cosmos 합성 데이터셋 v1 (정합 95%)</li>
        <li>굴착기·고소작업대 데이터 로거 1차</li>
        <li>9개 자율작업 시나리오 학습 파이프라인</li>
      </ul>
    </div>
    <div class="block">
      <div class="subhead">통합·검증 (Y1~Y4)</div>
      <ul class="body compact">
        <li>MQTT·OPC-UA·ROS2 실시간 연동</li>
        <li>Omniverse·Isaac·Cosmos·FMU·AI 통합</li>
        <li>Track 1·2 AB 비교 · KPI 성능 검증</li>
        <li>Sequential KT 총괄 · OEM 패키지화</li>
        <li>3종 통합 DT 플랫폼 완성 (Y4)</li>
      </ul>
    </div>
  </div>
</div>
"""
    return page("주관 싸이언", body, css)


def slide_org_partners() -> str:
    css = """
body { display: grid; grid-template-rows: auto 1fr auto; height: 720px; padding: 38px 56px 32px; }
.headline { font-size: 34px; margin-bottom: 20px; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 24px 40px; align-content: stretch; }
.org { padding: 26px 30px; background: #f4f7fb; border-radius: 14px; display: flex; flex-direction: column; }
.org h3 { font-size: 21px; font-weight: 700; color: #1F4E79; margin-bottom: 16px; }
.org .body { font-size: 17px; flex: 1; }
.org .body li { margin-bottom: 11px; }
.img-band { margin-top: 20px; display: grid; grid-template-columns: 1.4fr 1fr; gap: 24px; align-items: center; background: #eef3f9; border-radius: 12px; padding: 16px 24px; }
.img-band img { width: 100%; height: 140px; object-fit: contain; border-radius: 8px; }
.img-band p { font-size: 17px; color: #374151; line-height: 1.55; font-weight: 500; }
"""
    body = f"""
<div class="kicker">09 · 공동기관 (1)</div>
<h1 class="headline">거비메타 · 한국건설기술연구원</h1>
<div class="cols">
  <div class="org">
    <h3>㈜거비메타</h3>
    <ul class="body">
      <li>굴착기 시뮬레이터 + 베테랑 운전자 굴토 100시간+</li>
      <li>STEP 3종 · 광산 Point Cloud · Amesim 유압 FMU v1</li>
      <li>유압 FMU 응답 ≤15ms · 실측 오차 ≤5%</li>
      <li>가상지형 고정밀 Point Cloud 인도</li>
    </ul>
  </div>
  <div class="org">
    <h3>한국건설기술연구원</h3>
    <ul class="body">
      <li>연천 SOC 실증연구센터 (69만㎡) Proving Ground</li>
      <li>굴착기·고소작업대·로더 실차 V&V · KOLAS</li>
      <li>안전관리·시험절차·평가기준 수립</li>
      <li>야간·위험환경 실증시험 지원</li>
    </ul>
  </div>
</div>
<div class="img-band">
  <img src="{IMG}/BIN0023.jpeg" alt="광산 Point Cloud 지형">
  <p>광산 환경 Point Cloud → Isaac Sim 가상 작업환경 구축 · 거비메타 제공 지형 데이터</p>
</div>
"""
    return page("공동 거비메타 KICT", body, css)


def slide_org_univ() -> str:
    css = """
.pad { padding: 38px 56px 34px; }
.headline { margin-bottom: 22px; }
.cols { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; flex: 1; min-height: 0; }
.org { padding: 26px 28px; background: #f4f7fb; border-radius: 14px; display: flex; flex-direction: column; justify-content: center; }
.org h3 { font-size: 19px; font-weight: 700; color: #1F4E79; margin-bottom: 16px; line-height: 1.35; }
.org .body { font-size: 17px; flex: 1; }
.org .body li { margin-bottom: 12px; }
"""
    body = """
<div class="slide pad">
  <div class="kicker">10 · 공동기관 (2)</div>
  <h1 class="headline">울산대 · 인하대 · 융기원</h1>
  <div class="cols">
    <div class="org">
      <h3>울산대 산학협력단</h3>
      <ul class="body compact">
        <li>토사해석 FMU v1 (3종 토사×광산)</li>
        <li>DEM 정밀 모델 · ROM 변환</li>
        <li>버킷-토사 상호작용 · ASME V&V</li>
        <li>건설기계 특화 토사 물성 DB</li>
        <li>Lab-scale 버킷 반력 측정 장치</li>
      </ul>
    </div>
    <div class="org">
      <h3>인하대 산학협력단</h3>
      <ul class="body compact">
        <li>자율형 상위제어기 아키텍처</li>
        <li>HTN 기반 자율공정 계획</li>
        <li>운영영역 인식 · 안전필터</li>
        <li>HPC 연계형 시제품 (Y2~Y4)</li>
        <li>Caterpillar 글로벌 자문 반영</li>
      </ul>
    </div>
    <div class="org">
      <h3>차세대융합기술연구원</h3>
      <ul class="body compact">
        <li>센서-상위제어기 인터페이스 검증</li>
        <li>관제센터 통합 연계 검증</li>
        <li>실험실 환경 데이터 동기화</li>
        <li>실환경 조건 검증 데이터 확보</li>
        <li>지장물 위험도 판별 기술 연계</li>
      </ul>
    </div>
  </div>
</div>
"""
    return page("공동 대학·연구원", body, css)


def slide_y1() -> str:
    css = """
.pad { padding: 38px 56px 34px; }
.cols { display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 40px; flex: 1; align-items: stretch; }
.left-col { display: flex; flex-direction: column; justify-content: center; }
.left-col .body { font-size: 17px; }
.kpi-box { background: #f4f7fb; border-radius: 14px; padding: 28px 32px; display: flex; flex-direction: column; justify-content: center; }
.kpi-box .subhead { font-size: 20px; margin-bottom: 18px; border: none; padding: 0; }
.kpi-box .tbl { font-size: 17px; }
.kpi-box .tbl td { padding: 14px 12px; }
.kpi-box .tbl td:last-child { font-weight: 800; color: #1F4E79; font-size: 19px; text-align: right; }
"""
    body = """
<div class="slide pad">
  <div class="kicker">11 · 1차년도</div>
  <h1 class="headline">플랫폼 v1 · Two-Track PoC</h1>
  <div class="cols">
    <div class="left-col">
      <ul class="body">
        <li>OpenUSD·Omniverse·Isaac Sim DT 플랫폼 v1 구축</li>
        <li>굴착기·고소작업대 Track 1·2 강화학습 PoC (9 시나리오)</li>
        <li>유압동력학 FMU v1 · 토사해석 FMU v1 · 3종 토사환경</li>
        <li>굴토작업 데이터 100시간+ · Cosmos 멀티모달 데이터셋</li>
        <li>인하대 상위제어기 인터페이스 · 융기원 실험실 검증</li>
        <li>Gate 1: DT v1 + Track PoC + KICT Proving Ground 연계</li>
      </ul>
    </div>
    <div class="kpi-box">
      <div class="subhead">정량 KPI (Y1)</div>
      <table class="tbl">
        <tbody>
          <tr><td>USD 폴리곤</td><td>200만+</td></tr>
          <tr><td>Cosmos 정합</td><td>95%</td></tr>
          <tr><td>유압 FMU 응답</td><td>≤15ms</td></tr>
          <tr><td>토사 FMU 정합</td><td>≥95%</td></tr>
          <tr><td>굴토작업 데이터</td><td>100시간+</td></tr>
          <tr><td>병렬 학습 환경</td><td>4,096</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
"""
    return page("1차년도 계획", body, css)


def slide_budget() -> str:
    css = """
.pad { padding: 38px 56px 34px; }
.summary { display: flex; gap: 28px; margin-bottom: 28px; }
.sum-item { flex: 1; padding: 24px 28px; background: #f4f7fb; border-radius: 14px; }
.sum-item .n { font-size: 40px; font-weight: 800; color: #1F4E79; line-height: 1; }
.sum-item .l { font-size: 16px; color: #4b5563; margin-top: 10px; line-height: 1.45; font-weight: 600; }
.tbl { font-size: 17px; flex: 1; }
.tbl td:nth-child(2), .tbl td:nth-child(3), .tbl td:nth-child(4) { text-align: right; font-variant-numeric: tabular-nums; font-weight: 600; }
.tbl td { padding: 15px 16px; }
.note { font-size: 15px; color: #6b7280; margin-top: 16px; }
"""
    body = """
<div class="slide pad">
  <div class="kicker">12 · 연구개발비</div>
  <h1 class="headline">총괄 예산 · 단계별 배분</h1>
  <div class="summary">
    <div class="sum-item"><div class="n">6,196,882</div><div class="l">총 연구개발비 (천원)<br>약 62억원</div></div>
    <div class="sum-item"><div class="n">4,112,000</div><div class="l">정부지원 (천원)<br>4개년 합계</div></div>
    <div class="sum-item"><div class="n">1,320,563</div><div class="l">1차년도 합계 (천원)<br>정부+기관부담</div></div>
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
  <p class="note">※ 2026.06.01 – 2029.12.31 (3년 7개월) · 1단계 1~4차년도</p>
</div>
"""
    return page("연구개발비", body, css)


def slide_commercialization() -> str:
    css = """
.pad { padding: 38px 56px 34px; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 32px 48px; flex: 1; align-content: center; }
.col .subhead { font-size: 20px; }
.col .body { font-size: 17px; }
.highlight { margin-top: auto; padding: 22px 28px; background: #eef3f9; border-left: 5px solid #1F4E79; font-size: 18px; line-height: 1.62; border-radius: 0 12px 12px 0; }
.highlight strong { color: #1F4E79; font-size: 19px; }
"""
    body = """
<div class="slide pad">
  <div class="kicker">13 · 사업화</div>
  <h1 class="headline">OEM 라이센싱 · 플랫폼 사업화</h1>
  <div class="cols">
    <div class="col">
      <div class="subhead">사업화 목표</div>
      <ul class="body compact">
        <li>고소작업대 OEM 라이센싱 조기 가시화 (Gate 2)</li>
        <li>FMU 3종 + ROM 라이브러리 사업화 자산</li>
        <li>굴착기·로더 3종 통합 OEM 패키지 (Y4)</li>
        <li>사업화 누적 매출 25억 원 목표</li>
        <li>개발기간 30% · 시험비용 50% 절감 제안</li>
      </ul>
    </div>
    <div class="col">
      <div class="subhead">사업화 전략</div>
      <ul class="body compact">
        <li>수산세보틱스·트림블·레디로버 수요 연계 실증</li>
        <li>기술이전·라이선싱·플랫폼 SaaS 병행</li>
        <li>FMI 표준 기반 플랫폼 독립 이식성</li>
        <li>가상 제품개발 SW 패키지 OEM 공급</li>
        <li>과제 종료 즉시 상용화·기술이전 연계</li>
      </ul>
    </div>
  </div>
  <div class="highlight"><strong>4차년 마일스톤:</strong> DT 플랫폼 → AI 학습 → 실차 실증 → OEM 라이센싱. TRL 7 · KOLAS 인증 완료 상태로 즉시 상용화.</div>
</div>
"""
    return page("사업화", body, css)


def slide_impact() -> str:
    css = """
.pad { padding: 36px 56px 32px; }
.grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 18px 22px; flex: 1; align-content: stretch; }
.card { padding: 22px 24px; border-top: 4px solid #1F4E79; background: #fafbfc; display: flex; flex-direction: column; }
.card h3 { font-size: 19px; font-weight: 700; color: #1F4E79; margin-bottom: 12px; }
.card p { font-size: 16px; line-height: 1.58; color: #374151; flex: 1; }
.headline { margin-bottom: 18px; }
"""
    body = """
<div class="slide pad">
  <div class="kicker">14 · 기대효과</div>
  <h1 class="headline">과학기술 · 산업 · 사회 파급</h1>
  <div class="grid">
    <div class="card"><h3>기술적</h3><p>Physical AI·ROM 실시간성(≤50ms)과 정밀성(≥90%) 동시 확보. Sim-to-Real 앙상블·AAS 표준 선도.</p></div>
    <div class="card"><h3>경제적</h3><p>국산 OEM 기술패키지로 글로벌 스마트건설 대응. 기술이전·라이선싱·플랫폼 사업화 신규 시장.</p></div>
    <div class="card"><h3>사회적</h3><p>고위험·야간·재난 현장 무인화. Safety Interlock 중대재해 예방. 숙련인력 부족 구조적 완화.</p></div>
    <div class="card"><h3>정책 연계</h3><p>미래모빌리티 초격차 '건설·농기계 완전 무인화' 직결. 과제 종료 즉시 현장 투입 가능.</p></div>
    <div class="card"><h3>확장성</h3><p>FMI 프로토콜을 농기계·방산·광산으로 수평 전개. 개방형 검증 인프라 지속 운영.</p></div>
    <div class="card"><h3>고용</h3><p>본 사업 청년 인력 채용. 사업화 단계 ~40명 신규 고용. 내국인 중심 R&D 인력 양성.</p></div>
  </div>
</div>
"""
    return page("기대효과", body, css)


def slide_closing() -> str:
    css = """
body {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  text-align: center; background: linear-gradient(155deg, #0f2d4a 0%, #1F4E79 50%, #2E75B6 100%);
}
h1 { font-size: 64px; font-weight: 800; color: #fff; margin-bottom: 28px; }
.sub { font-size: 22px; color: #c5dff5; max-width: 900px; line-height: 1.65; margin-bottom: 40px; }
.orgs { font-size: 18px; color: #8ec5f0; letter-spacing: .03em; line-height: 2; }
"""
    body = """
<h1>감사합니다</h1>
<p class="sub">인공지능 기반 무인 자율 굴착기 개발을 위한<br>초실감 디지털 트윈 플랫폼 개발</p>
<div class="orgs">㈜싸이언 · ㈜거비메타 · 한국건설기술연구원<br>울산대학교 · 인하대학교 · 차세대융합기술연구원</div>
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
        ("04-goals-개발목표.html", slide_goals()),
        ("05-performance-성능목표.html", slide_performance()),
        ("06-method-연구방법.html", slide_method()),
        ("07-strategy-추진전략.html", slide_strategy()),
        ("08-roles-기관별역할.html", slide_roles()),
        ("09-org-싸이언.html", slide_org_scien()),
        ("10-org-거비메타-KICT.html", slide_org_partners()),
        ("11-org-대학연구원.html", slide_org_univ()),
        ("12-y1-1차년도.html", slide_y1()),
        ("13-budget-연구개발비.html", slide_budget()),
        ("14-commercialization-사업화.html", slide_commercialization()),
        ("15-impact-기대효과.html", slide_impact()),
        ("16-closing-감사합니다.html", slide_closing()),
    ]
    for name, content in files:
        (OUT / name).write_text(content, encoding="utf-8")
    index = (
        '<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><title>미리보기</title>'
        "<style>body{font-family:'Malgun Gothic',sans-serif;padding:24px}"
        "a{display:block;padding:6px 0;color:#1F4E79}</style></head><body>"
        "<h2>초실감 디지털 트윈 플랫폼</h2>"
    )
    for name, _ in files:
        index += f'<a href="{name}">{name}</a>\n'
    index += "</body></html>"
    (OUT / "index.html").write_text(index, encoding="utf-8")
    print(f"Wrote {len(files)} slides to {OUT}")


if __name__ == "__main__":
    main()
