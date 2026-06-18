# PptMaker — agent workflow

**You run every step; the user only provides the HWP (and optional reference images).**

**You are the designer.** Scripts extract content — they do not produce the final deck. Never ship script output unchanged.

---

## Purpose

Turn a **Korean R&D HWP** into a **visually strong presentation**.

| Input | Outputs | Pipeline |
|-------|---------|----------|
| `{name}.hwp` + optional images | `slides/*.html` + `presentation.pptx` | Extract → plan → AI design HTML → PPTX |

HTML-first is required (1280×720 inline CSS) before PPTX. No direct python-pptx path.

---

## Hard rules

1. **Facts from HWP only** — do not invent names, patents, stats, orgs, or photos
2. **1280×720 HTML** before conversion
3. **Images:** bindata from HWP + any user-provided images (see Step 2). Never leave large blank areas
4. **Important information only** — cut repetition; merge related sections. Target **12–18 slides**
5. **No empty-looking slides** — redesign (bigger type, cards, diagram, stat row) or fold into another slide
6. **No boxed-section scaffold** — white canvas, one focal element, ≤ 1 tinted surface per slide

Everything else — layout, colors, typography — is your design call.

---

## Design mandate

The deck must look **modern and professional**.

| Do | Don't |
|----|-------|
| Open layouts on a white canvas — whitespace and typography organize content | Gray background + grid of outlined white panels |
| Bullets, clean tables, split panels that fill height | Chips, stat-card grids, heavy shadows |
| Large readable type (title 26–32px, body 16–18px) | Font sizes below 14px |
| Classic layouts: title bar + body, image left / text right | Same card grid on every slide |
| Each HWP figure **once** in the deck | Same image on multiple slides |
| Merge sparse HWP sections onto one rich slide | One thin fact per slide |

See `references/visual-design.md` and `references/html-slides.md` for inspiration — not rigid templates.

---

## Steps

### Step 0 — Bootstrap (run once per session)

#### 0-A. Pull latest workflow updates

The canonical workflow lives at `https://github.com/turaliyev0/PPT_Maker.git`. Always pull before starting so you work with the latest scripts, references, and `WORKFLOW.md`.

```bash
# Always pull using the direct URL — do NOT rely on a named remote
# (the remote may be named "origin", "orign", or anything else depending on the device)
git pull https://github.com/turaliyev0/PPT_Maker.git main
# if that fails, try master branch:
git pull https://github.com/turaliyev0/PPT_Maker.git master

# If the project folder is NOT a PPT_Maker clone (e.g. first-time setup),
# clone into a sibling folder and copy scripts + references across:
git clone https://github.com/turaliyev0/PPT_Maker.git _pptmaker_latest
xcopy /E /I /Y _pptmaker_latest\scripts scripts
xcopy /E /I /Y _pptmaker_latest\references references
xcopy /E /I /Y _pptmaker_latest\templates templates
copy /Y _pptmaker_latest\WORKFLOW.md WORKFLOW.md
rmdir /S /Q _pptmaker_latest
```

> If `git pull` fails (no remote, offline, auth error) — log the error, skip this step, and continue with the local copy. Never block the workflow on a network error.

#### 0-B. Verify Python

```bash
python --version
```

- If Python **3.8 or later** is returned → continue.
- If the command fails or returns Python 2 → try `python3 --version`.
  - If `python3` works, use `python3` in place of `python` for all subsequent script calls.
  - If neither works → tell the user Python is not installed and provide the install link: https://www.python.org/downloads/ — then stop.

Also confirm the required packages are available:

```bash
python -c "import olefile, bs4, Pillow; print('OK')" 2>&1
```

If any package is missing, install them before proceeding:

```bash
pip install olefile beautifulsoup4 Pillow
```

---

### Step 1 — Extract HWP

```bash
python scripts/extract_hwp_text.py {file}.hwp
python scripts/parse_hwp.py {file}.hwp
```

Read `templates/extracted/{stem}-hwp-from-html-parsed.json` → `slide_plan`, `missing`, `orgs`, `figures`.

---

### Step 2 — Inventory all image sources

Before designing, build a complete picture of every image available. Check **both** sources:

#### A. HWP bindata (`templates/extracted/{stem}-hwp-full/bindata/`)

> **Critical — always scan visually.** R&D proposals routinely embed full-resolution certification and award documents (CE PED, ASME U/UM, UL, ISO, 표창장, 학술상) as large BMP/PNG files (800–1600px wide). The `input-figures.json` captions are often wrong. View every file. Look especially for:
> - Portrait-format files (height > width) — likely cert documents or award letters
> - Large BMP files — often scanned international certificates
> - Files with `BIN00[23][0-9]` range — usually late-appended certs
>
> Use actual document images in `capability` slides (cert-strip row, ~170px height) — far more credible than logo thumbnails.

Record each image: path · dimensions · aspect ratio · content class (diagram / portrait / cert-doc / award / logo).

#### B. User-provided images (`preloadable_images/`)

The project has a dedicated **`preloadable_images/`** folder for user-supplied images. Scan it **before designing**. Also check any other image folder the user mentions (e.g., `presentation_1-images/`).

| Image type found | How to use |
|-----------------|-----------|
| Professor / PI portrait photo | Use as the PI portrait in the matching `capability` slide |
| Award certificate / 표창장 / 학술상 | Display as a document thumbnail in the matching `capability` slide |
| Previous presentation screenshot | Extract style / color palette reference only — do not copy content verbatim |
| High-res diagram or render | Prefer over a lower-res bindata equivalent for the same subject |

> Using user-provided images is **not mandatory** — only include them if they match the slide content. Never force an image into a slide where it doesn't belong. Always prefer the highest-resolution version of the same subject.

---

### Step 3 — Plan (light)

- Skim `slide_plan` — **drop or merge** slides that repeat or would look empty
- Prefer combined kinds: `background_goals`, `method_roles`, `org_block`, `schedule_budget`, `intl_combined`
- Skip `toc`, `org_intro`, `appendix_profile` unless the user asked for a long deck
- Note `missing[]`; use placeholders or omit
- **No approval gate** unless the user asked to confirm first

---

### Step 4 — Design HTML

**Option A (preferred):** Read parsed JSON + figures and write each `slides/{num}-{kind}-*.html` yourself with distinct, polished CSS.

**Option B (scaffold):** Run the builder for content reference only, then rewrite every file:

```bash
python scripts/build_html_from_plan.py {file}.hwp slides/_draft
```

Copy facts/paths from `_draft` into your designed slides under `slides/`. Delete `_draft` when done.

**Per slide:** pick layout for *this* content — cover hero, stat cards, timeline, photo grid, full-bleed image + caption band, etc. Vary structure across the deck.

Write `slides/index.html` linking all slides.

#### Quality pass before converting

- Titles and body text readable at presentation distance
- No duplicate bindata images (track which `BIN*.png` you used)
- Slides feel visually distinct, not copy-pasted CSS
- **Every slide looks intentionally full** — no large dead zones
- No slide is a grid of outlined boxes
- Consecutive slides use different page architectures

#### Empty-space & image alignment red flags — detect and fix before converting

| Pattern | Symptom | Fix |
|---------|---------|-----|
| `justify-content: space-between` on ≤6 items in a tall column | Items float apart | Switch to natural `padding` per item + add a fill element below |
| Wide-AR image (AR > 2.5:1) in a flex column | Blank bands above and below | Wrap in a tinted panel (`background:#f0f5fb; border-radius:10px; padding:14px`) or add a spec-strip below |
| 3 exec/role cards with `gap:10px` in a tall column | Gaps between cards | Give each card `flex:1` |
| PI portrait < 180px natural width displayed at CSS 120px+ | Blurry portrait in PPTX | Max CSS size = `round(natural_px / 2)` at `deviceScaleFactor:2`; fill remaining space with stat chips or award doc |
| Narrow column (≤200px) with portrait + sparse text | Bottom half empty | Add fact chips: 총 인원, 연구기간, 특허 건수, etc. |
| Cert/doc image inside a tall `flex:1` container with `object-fit:contain` | Image floats in the middle of an empty box | Use `width:100%; height:auto` + `align-items:flex-start` on the parent |
|| `margin-top:auto` on image at bottom of column | Image snaps to corner with large empty gap above | Remove `margin-top:auto`; add a highlight box or metric row before the image |
|| Fixed small px size on cert/award image (e.g. `width:52px; height:66px`) | Tiny thumbnail lost in whitespace | Use `width:100%; height:auto` — container width controls the size |
|| `<img>` has no explicit `width` inside a flex column | Renders at natural pixel size — may be tiny or invisible | Always set `width:100%; height:auto; object-fit:contain` on every slide image |

> **QA checklist — run after every screenshot pass:**
> 1. Is any image smaller than 25% of its surrounding column width? → enlarge
> 2. Is any image stuck to a corner (top-left, bottom-left, bottom-right)? → fix container alignment
> 3. Is there a visible blank area larger than ~80px tall or wide with nothing in it? → add fill content or move image up
> 4. Do all cert/doc images span the full column width? → `width:100%` if not
> 5. Check slide visually — if anything looks misaligned or unprofessional, fix it before converting

#### Pre-built fill elements

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
  <strong style="color:#1F4E79">핵심 키워드:</strong> 내용 내용 내용
</div>

<!-- Tinted image panel (wide-AR diagrams) -->
<div style="flex:1;background:#f0f5fb;border-radius:10px;padding:14px;display:flex;align-items:center;justify-content:center;min-height:0">
  <img src="..." style="max-width:100%;max-height:100%;object-fit:contain">
</div>

<!-- Document / cert display (natural size, top-aligned) -->
<div style="display:flex;align-items:flex-start;gap:14px">
  <div style="flex:1;display:flex;flex-direction:column;gap:6px">
    <img src="..." style="width:100%;height:auto;border:1px solid #c8d9ec;border-radius:6px;box-shadow:0 3px 12px rgba(31,78,121,.12)">
    <p style="font-size:11px;color:#9ca3af;text-align:center">캡션</p>
  </div>
</div>
```

---

### Step 5 — Convert HTML → PPTX

```bash
npm install          # once, if node_modules missing
node scripts/html_to_pptx.mjs slides/ presentation.pptx
```

---

### Step 6 — Image QA (mandatory)

Render slides to screenshots and run the checklist in `references/figures.md` Step D. Fix → reconvert → recheck. Never skip.

**Also check visual layout — not just content:**
- Every image fills its container. No image is tiny, cropped into a corner, or floating with dead space around it.
- No blank area larger than ~80px with no content.
- Cert/doc images use `width:100%; height:auto` — never fixed small px dimensions.
- Remove any `margin-top:auto` that pushes an image to the bottom of a column.
- If a screenshot looks bad (misaligned, unprofessional, image in corner), fix the HTML and reconvert before delivering.

---

### Step 7 — Deliver

- `slides/` — HTML preview
- `presentation.pptx`
- Brief note on `missing[]` or design choices if relevant

---

## Slide kinds (content map)

| `kind` | Typical HWP section |
|--------|---------------------|
| `cover` | 표지 |
| `background_goals` | 배경 + 목표 + 성능 하이라이트 |
| `method_roles` | 연구방법 + 기관별 역할 |
| `org_block` | 수행 + 선행 + 연차 (per org) |
| `capability` | 책임자 역량 — per org |
| `schedule_budget` | 세부 일정 + 연구비 |
| `intl_combined` | 국제공동 증빙 + 협력 실적 |
| `commercialization` | 사업화 목표·전략 |
| `impact` | 기대효과 |
| `closing` | 감사합니다 |

*(Other kinds: `background`, `goals`, `performance`, `method`, `execution`, `prior_rd`, `yearly`, `roles`, `schedule`, `budget`, `intl_evidence`, `intl_base`, `appendix_profile`)*

Kind suggests content — **not** a fixed layout. Break the pattern when it looks better.

---

## Proven `capability` slide blueprint

3-column structure that fills the canvas and avoids dead zones:

```
[col-pi: 200–230px]         [col-main: flex:1]                    [col-patents: 245–270px]
─────────────────────       ───────────────────────────────────   ─────────────────────────
Portrait (65–90px CSS)      kicker / headline / subhead           kicker "지식재산권"
Name + title + org          <hr>                                  <table> patent rows
Key fact chips              Stats row (논문 N편 · 특허 N건 등)        with patent numbers
Career timeline             Capabilities bullet list
<divider>                   Research connection table (2-col)
Award cert docs             Cert-doc strip OR metric tile row
(portrait format imgs)      note-bar at bottom
```

**Portrait resolution rule:** `max_css_px = round(source_px / 2)` at `deviceScaleFactor:2`.  
A 131×177 source → max 65×88px CSS. Fill remaining column height with stat chips or award document thumbnails.

**Cert-doc strip:**
```html
<div style="border-top:1px solid #dde2ea;padding-top:12px;margin-top:14px">
  <p style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#2E75B6;margin-bottom:8px">
    보유 국제 인증서 (원본)
  </p>
  <div style="display:flex;gap:10px">
    <!-- repeat per cert found in bindata -->
    <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px">
      <img src="../templates/extracted/{stem}-hwp-full/bindata/BIN00XX.png"
           style="width:100%;height:170px;object-fit:contain;border:1px solid #dde2ea;border-radius:4px;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.06)">
      <span style="font-size:10px;color:#6b7280;text-align:center;line-height:1.3">CERT NAME<br>STANDARD</span>
    </div>
  </div>
</div>
```

---

## Scripts

| Script | Role |
|--------|------|
| `scripts/extract_hwp_text.py` | HWP → text + embedded images |
| `scripts/parse_hwp.py` | text → `slide_plan` JSON |
| `scripts/build_html_from_plan.py` | Optional content scaffold — **not final design** |
| `scripts/slide_images.py` | Bindata image resolver |
| `scripts/html_to_pptx.mjs` | HTML slides → PPTX (Puppeteer + pptxgenjs) |

---

## References

| File | Contents |
|------|----------|
| `references/figures.md` | Figure selection, aspect-ratio sizing, QA checklist |
| `references/visual-design.md` | Design principles, anti-patterns |
| `references/html-slides.md` | Canvas, typography, layout ideas |
| `references/slide-structure.md` | R&D section skeleton |
| `references/pipeline.md` | JSON fields, paths |
| `references/html-to-pptx.md` | Conversion details |

---

*Extract content with scripts. Design the deck with your judgment.*
