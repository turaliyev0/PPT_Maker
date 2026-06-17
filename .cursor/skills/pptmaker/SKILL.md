---
name: pptmaker
description: >-
  Agent-only: Korean R&D HWP to polished presentation. Extract HWP content, then
  YOU design beautiful slides/*.html (creative layouts, strong typography), convert
  to PPTX. Use for .hwp, R&D deck, 책임자 역량, slide_plan, or PptMaker.
---

# PptMaker — agent workflow

**Agent-only.** You run every step; the user only attaches the HWP.

**You are the designer.** Scripts extract content — they do not produce the final deck. Never ship script output unchanged.

---

## Purpose

Turn a **Korean R&D HWP** into a **visually strong presentation**.

| Input | Outputs | Pipeline |
|-------|---------|----------|
| User's `.hwp` | `slides/*.html` + `presentation.pptx` | **Extract → plan → AI design HTML → PPTX** |

HTML-first is required (1280×720 inline CSS) before PPTX. No direct python-pptx path.

---

## Hard rules

1. **Facts from HWP only** — do not invent names, patents, stats, orgs, or photos
2. **1280×720 HTML** before conversion
3. **Images:** bindata from HWP/PDF only (`references/figures.md`). If no relevant bindata for a slide, merge the slide content elsewhere or redesign without a photo — never ship large blank areas
4. **Important information only** — cut repetition; merge related sections. Target **12–18 slides** for a typical R&D HWP (not 30+)
5. **No empty-looking slides** — if a slide feels sparse, **redesign** it (bigger type, cards, diagram, stat row) or **remove** it and fold the facts into another slide
6. **No boxed-section scaffold** — never gray page + multiple outlined white panels + accent-bar headings. White canvas, one focal element, ≤ 1 tinted surface per slide, architectures rotated per `references/html-slides.md`.

Everything else — layout, colors, typography, charts — is your design call.

---

## Design mandate

The deck must look **modern and professional**, not plain-empty and not an AI gimmick showcase.

| Do | Don't |
|----|-------|
| Open layouts on a white canvas — whitespace and typography organize content | Gray background + grid of outlined white panels (dashboard look) |
| ○ bullets, clean tables, split panels that fill height | Chips, stat-card grids, heavy shadows |
| Large readable type (title 26–32px, body 16–18px) | Font sizes below 14px |
| Classic layouts: title bar + body, image left / text right | Same fancy card grid on every slide |
| Each HWP figure **once** in the deck | Same image on background, goals, and method |
| Merge sparse HWP sections onto one rich slide | One thin fact per slide across the deck |
| Edit HTML yourself for polish | Stop after `build_html_from_plan.py` |

See `references/visual-design.md` and `references/html-slides.md` for inspiration — not rigid templates.

---

## Agent steps

### Step 1 — Extract HWP

```
python scripts/extract_hwp_text.py {file}.hwp
python scripts/parse_hwp.py {file}.hwp
```

Read `templates/extracted/{stem}-hwp-from-html-parsed.json` → `slide_plan`, `missing`, `orgs`, `figures`.

### Step 2 — Plan (light)

- Skim `slide_plan` — **drop or merge** slides that repeat or would look empty
- Prefer combined kinds: `background_goals`, `method_roles`, `org_block`, `schedule_budget`, `intl_combined`
- Skip `toc`, `org_intro`, `appendix_profile` unless the user asked for a long deck
- Note `missing[]`; use placeholders or omit
- **No approval gate** unless the user asked to confirm first

### Step 3 — Design HTML (you lead)

**Before designing: complete Step A of `references/figures.md`** (view all bindata images, record dimensions/aspect/content class, build the figure→slide table).

> **CRITICAL — deep bindata scan:** HWP documents for R&D proposals routinely embed full-resolution certification documents and award certificates (CE PED, ASME U/UM, UL, ISO, 표창장, 학술상) as large BMP/PNG files (800–1600px wide). These almost never appear with accurate captions in `input-figures.json`. You **must** view every bindata file visually, not just read the captions. Sorted by descending size, look especially for:
> - Portrait-format images (height > width) — likely cert documents or award letters
> - Large BMP files — often scanned certificates with ASME/CE/UL/ISO headers
> - Files with `BIN00[23][0-9]` numbering range — usually late-appended certs
>
> When found: use the actual document image in `capability` slides (cert-strip row, height ~170px) instead of tiny logo strips. The difference in visual quality and credibility is dramatic.

**Image gaps:** for slides with no matching bindata, merge sparse slides or redesign as text/stat layout — do not leave empty image wells.

**Option A (preferred):** Read parsed JSON + figures and write each `slides/{num}-{kind}-*.html` yourself with distinct, polished CSS.

**Option B (scaffold):** Run the builder for content reference only, then rewrite every file:

```
python scripts/build_html_from_plan.py {file}.hwp slides/_draft
```

Copy facts/paths from `_draft` into your designed slides under `slides/`. Delete `_draft` when done.

**Per slide:** pick layout for *this* content — cover hero, stat cards, timeline, photo grid, full-bleed image + caption band, etc. Vary structure across the deck.

Write `slides/index.html` linking all slides.

**Quality pass before Step 4:**
- Titles and body text readable at presentation distance
- No duplicate bindata images (track which `BIN*.png` you used)
- Slides feel visually distinct, not copy-pasted CSS
- **Every slide looks intentionally full** — no large dead zones; slide count ≤ ~18 unless user wants more
- No slide is a grid of outlined boxes; content sits on the canvas
- Consecutive slides use different page architectures

**Empty-space red flags — detect and fix all of these before converting:**

| Pattern | Symptom | Fix |
|---------|---------|-----|
| `justify-content: space-between` on a short list (≤6 items) in a tall column | Items float apart with huge gaps | Switch to natural `padding` per item + add a fill element (metric tiles, highlight box, spec strip) below the list |
| Wide-AR image (AR > 2.5:1) in a flex column | Large blank bands above and below the image | Wrap image in a tinted panel (`background: #f0f5fb; border-radius:10px; padding:14px`) so the panel fills the container, OR stack a spec-strip below |
| 3 exec/role cards with `gap:10px` in a tall column | Visible empty space between cards | Give each card `flex: 1` so cards share the column height evenly |
| PI portrait from a prior PDF export (< 180px natural width) displayed at CSS 120px+ | Blurry portrait in final PPTX | Cap CSS display size ≤ `natural_px / deviceScaleFactor` (typically ≤ 65–90px CSS); OR show the portrait at natural size and use a companion element (award cert image, stat facts) to fill the vertical space |
| Very narrow single column (≤200px) with portrait + sparse text | Bottom half empty | Add structured fact chips: 총 인원, 연구기간, 특허 건수, etc. stacked with dividers |

**Pre-built fill elements — use freely to eliminate dead zones:**

```html
<!-- Metric tile row (4-up) -->
<div style="display:flex;gap:10px;margin-top:14px">
  <div style="flex:1;background:#eef4fb;border-radius:8px;padding:12px;text-align:center">
    <span style="font-size:20px;font-weight:800;color:#1F4E79;display:block">VALUE</span>
    <span style="font-size:11px;color:#6b7280;line-height:1.4">LABEL<br>SUBLABEL</span>
  </div>
  <!-- repeat × 4 -->
</div>

<!-- Spec strip (4-col bordered) -->
<div style="display:flex;border:1px solid #dde2ea;border-radius:8px;overflow:hidden;flex-shrink:0">
  <div style="flex:1;padding:11px 12px;border-right:1px solid #dde2ea;background:#f4f7fb;text-align:center">
    <span style="font-size:17px;font-weight:800;color:#1F4E79;display:block">VALUE</span>
    <span style="font-size:11px;color:#6b7280;line-height:1.4">KEY<br>LABEL</span>
  </div>
  <!-- repeat -->
</div>

<!-- Highlight box -->
<div style="background:#f4f7fb;border-radius:8px;padding:12px 14px;font-size:12px;color:#374151;line-height:1.6;margin-top:12px">
  <strong style="color:#1F4E79">핵심 키워드:</strong> 내용 내용 내용 내용 내용
</div>

<!-- Tinted image panel -->
<div style="flex:1;background:#f0f5fb;border-radius:10px;padding:14px;display:flex;align-items:center;justify-content:center;min-height:0">
  <img src="..." style="max-width:100%;max-height:100%;object-fit:contain">
</div>
```

### Step 4 — Convert HTML → PPTX

```
npm install          # once, if node_modules missing
node scripts/html_to_pptx.mjs slides/ presentation.pptx
```

### Step 4.5 — Image QA (mandatory)

Render the PPTX to images and run the checklist in `references/figures.md` Step D. Fix → reconvert → recheck. Never skip.

### Step 5 — Deliver

- `slides/` — HTML preview
- `presentation.pptx`
- Brief note on `missing[]` or design choices if relevant

---

## Slide kinds (content map)

| `kind` | Typical HWP section |
|--------|---------------------|
| `cover` | 표지 (section chips replace 목차 in compact decks) |
| `background_goals` | 배경 + 목표 + 성능 하이라이트 |
| `method_roles` | 연구방법 + 기관별 역할 |
| `background` | 개발 배경 (merge into `background_goals` when compact) |
| `goals` | 개발 목표 |
| `performance` | 성능·평가 목표 |
| `method` | 연구개발 방법 |
| `org_block` | 수행 + 선행 + 연차 (per org, one slide) |
| `schedule_budget` | 세부 일정 + 연구비 |
| `intl_combined` | 국제공동 증빙 + 협력 실적 |
| `capability` | 책임자 역량 — per org |
| `intl_evidence` | 국제공동 협력 증빙 |
| `execution` | 수행 내용 — per org |
| `prior_rd` | 선행연구 — per org |
| `yearly` | 연차별 추진 — per org |
| `roles` | 기관별 역할 |
| `schedule` | 세부 일정 |
| `budget` | 연구비 |
| `commercialization` | 사업화 목표 |
| `commercialization_strategy` | 사업화 전략 |
| `impact` | 기대효과 |
| `intl_base` | 국제협력 기반 |
| `appendix_profile` | 별첨 프로필 |
| `closing` | 감사합니다 |

Kind suggests content — **not** a fixed layout. Break the pattern when it looks better.

### Proven `capability` slide blueprint (책임자 역량)

Use this 3-column structure. It fills the canvas and avoids the common dead-zone problems:

```
[col-pi: 200–220px fixed]   [col-main: flex:1]                     [col-patents: 260–280px fixed]
────────────────────────    ────────────────────────────────────    ────────────────────────────────
Portrait (80×100 CSS px)    kicker / headline / subhead             kicker "지식재산권"
Name + title + org          <hr>                                    <table> patent rows
<divider>                   Two sub-columns (핵심 역량 | 기여)         (9px per row, space-between)
Key facts (2–3 chips):        — bullet list each, flex:1
  총 N명 / N년+ / N건 특허   <hr>
<divider>                   Cert-doc strip (if certs found in
[award docs if any,           bindata, height ~170px each, 4 docs)
 flex:1, portrait images]   OR metric-tile row (4 tiles)
                            note-bar at bottom
```

**Portrait resolution rule:** source image `W × H` pixels → display at `round(W/2) × round(H/2)` CSS px (halves for `deviceScaleFactor:2`). For a 131×177 source → max display 65×88px CSS. Supplement with a stat chip column below the portrait to fill vertical space.

**Cert-doc strip pattern (for R&D orgs with ASME/CE/UL bindata):**
```html
<div style="border-top:1px solid #dde2ea;padding-top:12px;margin-top:14px">
  <p style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#2E75B6;margin-bottom:8px">보유 국제 인증서 (원본)</p>
  <div style="display:flex;gap:10px">
    <!-- for each cert BIN file found: -->
    <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px">
      <img src="../templates/extracted/input-hwp-full/bindata/BIN00XX.png"
           style="width:100%;height:170px;object-fit:contain;border:1px solid #dde2ea;border-radius:4px;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,0.06)">
      <span style="font-size:10px;color:#6b7280;text-align:center;line-height:1.3">CERT NAME<br>STANDARD</span>
    </div>
  </div>
</div>
```

---

## Scripts (helpers only)

| Script | Role |
|--------|------|
| `extract_hwp_text.py` | HWP → text + images |
| `parse_hwp.py` | text → `slide_plan` JSON |
| `build_html_from_plan.py` | Optional content scaffold — **not final design** |
| `slide_images.py` | Bindata image resolver |
| `html_to_pptx.mjs` | HTML → PPTX |

---

## References

- `references/figures.md` — figure selection, aspect-ratio sizing, image QA (read before Step 3)
- `references/visual-design.md` — design principles, anti-patterns
- `references/html-slides.md` — canvas, typography, layout ideas
- `references/slide-structure.md` — R&D section skeleton
- `references/pipeline.md` — JSON fields, paths
- `references/html-to-pptx.md` — conversion

---

*Extract content with scripts. Design the deck with your judgment.*
