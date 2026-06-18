# PptMaker — Workflow

**You run every step. The user only provides the HWP (and optional images).**  
**You are the designer** — scripts extract content, you produce the final deck.

Technical details for each step live in `steps/`. Read the step file before you begin that step.

---

## Hard rules

1. **HWP facts only** — never invent names, patents, stats, orgs, or photos
2. **HTML before PPTX** — 1280×720 inline-CSS HTML is always built first
3. **One image = one slide** — each `BIN*.png` / `BIN*.bmp` appears on exactly one slide; track usage as you go
4. **12–18 slides** — merge sparse sections, cut repetition
5. **No empty-looking slides** — redesign or merge; never ship a slide that looks half-done
6. **No boxed scaffold** — white canvas; ≤ 1 tinted surface per slide

---

## Step 0 — Bootstrap

Verify Python 3.8+ and required packages:

```bash
python --version
python -c "import olefile, bs4, Pillow; print('OK')" 2>&1
```

If packages are missing: `pip install olefile beautifulsoup4 Pillow`

---

## Step 1 — Extract HWP

> 📖 Read **`steps/step1-extract.md`** before this step.

```bash
python scripts/extract_hwp_text.py {file}.hwp
python scripts/parse_hwp.py {file}.hwp
```

Read the output JSON at `templates/extracted/{stem}-hwp-from-html-parsed.json`.  
Note: `slide_plan`, `missing[]`, `orgs`, `figures` — these drive the entire deck.

---

## Step 2 — Inventory all images

> 📖 Read **`steps/step2-images.md`** (Steps A, B, C) before this step.

- Scan every file in `templates/extracted/{stem}-hwp-full/bindata/` — view them, record dimensions and content class
- Scan `preloadable_images/` for user-provided images
- Build a figure→slide assignment table **before designing anything**

---

## Step 3 — Plan slides

> 📖 Read **`steps/step3-plan.md`** before this step.

- Drop or merge slides that would repeat or look empty
- Use combined kinds: `background_goals`, `method_roles`, `org_block`, `schedule_budget`, `intl_combined`
- Skip `toc`, `org_intro`, `appendix_profile` unless the user asked for them
- Target 12–18 slides; no approval gate unless the user asked to confirm first

---

## Step 4 — Design HTML slides

> 📖 Read **`steps/step4-design.md`** before this step.

Write each `slides/{num}-{kind}-*.html` yourself with distinct, polished CSS.  
Optionally use the scaffold for raw content only — always rewrite:

```bash
python scripts/build_html_from_plan.py {file}.hwp slides/_draft
```

Write `slides/index.html` linking all slides. Delete `_draft` when done.

---

## Step 5 — Convert HTML → PPTX

> 📖 Read **`steps/step5-convert.md`** before this step.

```bash
npm install          # once, if node_modules missing
node scripts/html_to_pptx.mjs slides/ presentation.pptx
```

---

## Step 6 — Visual QA

> 📖 Read **`steps/step2-images.md`** (Step D) before this step.

Screenshot every slide, inspect each one. Fix → reconvert → recheck. Never skip.

```bash
node -e "
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
(async () => {
  const browser = await puppeteer.launch({args:['--no-sandbox']});
  const files = fs.readdirSync('slides').filter(f => f.endsWith('.html') && f !== 'index.html').sort();
  fs.mkdirSync('qa_screenshots', {recursive:true});
  for (const f of files) {
    const page = await browser.newPage();
    await page.setViewport({width:1280, height:720, deviceScaleFactor:2});
    await page.goto('file:///' + path.resolve('slides/' + f).replace(/\\\\/g,'/'), {waitUntil:'networkidle0'});
    await page.screenshot({path:'qa_screenshots/' + f.replace('.html','.png')});
    await page.close();
  }
  await browser.close();
  console.log('done');
})();
" 2>&1
```

Do not deliver until the full QA checklist in `steps/step2-images.md` Step D passes.

---

## Step 7 — Deliver

- `slides/` — HTML preview
- `presentation.pptx` — final file
- Brief note on any `missing[]` items or notable design choices

---

## Steps reference

| File | Step | Contents |
|------|------|----------|
| `steps/step1-extract.md` | 1 | Script outputs, JSON fields, file paths |
| `steps/step2-images.md` | 2, 6 | Image inventory, sizing rules, placement, QA checklist |
| `steps/step3-plan.md` | 3 | R&D deck flow, kind map, merge strategy |
| `steps/step4-design.md` | 4 | Canvas, typography, page architectures, anti-patterns |
| `steps/step5-convert.md` | 5 | Conversion details, tradeoffs |

---

## Scripts

| Script | Role |
|--------|------|
| `scripts/extract_hwp_text.py` | HWP → text + embedded images |
| `scripts/parse_hwp.py` | text → `slide_plan` JSON |
| `scripts/extract_pdf.py` | PDF → text + embedded images (alternative input) |
| `scripts/extract_pdf_images.py` | PDF → embedded images only |
| `scripts/build_html_from_plan.py` | Optional content scaffold — not final design (uses `html_slides.py`) |
| `scripts/html_slides.py` | Slide scaffolding engine used by `build_html_from_plan.py` |
| `scripts/html_to_pptx.mjs` | HTML slides → PPTX |
