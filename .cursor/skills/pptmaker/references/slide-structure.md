# Common R&D deck structure

Common Korean R&D deck skeleton — **structure only, never copy content from other decks**.

All R&D decks share one skeleton. Depth varies with HWP; there are no fixed “types.”

**Default deck length:** ~12–18 slides. Merge sparse HWP blocks; skip 목차·별첨 unless the user wants a long deck.

## Flow

```
표지
  ↓
[목차]                    ← longer decks
  ↓
Project spine             ← once each, if HWP has section
  주관기관 소개 · 배경 · 목표 · 성능목표 · 방법
  ↓
Per participating org     ← REPEATS for each org
  책임자 역량 (professor page)
  → [국제공동 증빙]       ← if applicable, once
  수행 내용
  선행연구
  연차별 추진
  ↓
Project wrap              ← once each, if HWP has section
  기관별 역할 · 일정 · 예산 · 사업화 · 기대효과
  ↓
[별첨 PI 프로필]          ← extended CV when HWP has data
[감사합니다]
```

## Always prioritize

1. **책임자 역량** — appears in every reference deck; one slide per org with photo, 이력, 특허 when available
2. **Per-org block** — execution → prior_rd → yearly mirrors partner supplement decks
3. **HWP-driven inclusion** — skip any block the HWP does not contain

## Map to `slide_plan` kinds

| Reference section | `kind` |
|-------------------|--------|
| 표지 | `cover` |
| 목차 | `toc` |
| 주관기관 / 회사 연혁 | `org_intro` |
| 개발 배경 | `background` |
| 개발 목표 | `goals` |
| 성능평가 / 목표표 | `performance` |
| 연구개발 방법 | `method` |
| 책임자 역량 | `capability` |
| 국제공동 협력 증빙 | `intl_evidence` |
| 수행 내용 | `execution` |
| 선행연구개발 | `prior_rd` |
| 연차별 추진계획 | `yearly` |
| 기관별 역할 | `roles` |
| 세부 일정 | `schedule` |
| 연구비 | `budget` |
| 사업화 / 기대효과 | `commercialization`, `impact` |
| 별첨 프로필 | `appendix_profile` |
| 감사합니다 | `closing` |
