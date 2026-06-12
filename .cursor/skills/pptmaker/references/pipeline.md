# HWP pipeline — extract → design → PPTX

**Agent-only.** Scripts extract; **you design** the HTML.

## Flow

```
{file}.hwp
  → extract_hwp_text.py     text + bindata images
  → parse_hwp.py            slide_plan JSON
  → YOU write slides/*.html   ← design step (mandatory, AI-led)
  → html_to_pptx.mjs        presentation.pptx
```

Optional scaffold (not final output):

```bash
python scripts/build_html_from_plan.py {file}.hwp slides/_draft
```

## Step 1 outputs

| Path | Contents |
|------|----------|
| `templates/extracted/{stem}-hwp-from-html.txt` | Plain text |
| `templates/extracted/{stem}-hwp-full/bindata/` | Images |
| `templates/extracted/{stem}-figures.json` | Figure map |
| `templates/extracted/{stem}-hwp-from-html-parsed.json` | Full parse + `slide_plan` |

## Step 3 outputs (your work)

| Path | Contents |
|------|----------|
| `slides/{num}-{kind}-*.html` | Designed slides — unique layouts, readable type |
| `slides/index.html` | Browser preview index |

## Step 4

```bash
npm install   # once
node scripts/html_to_pptx.mjs slides/ presentation.pptx
```

## Missing data

| Situation | Action |
|-----------|--------|
| No PI photo | Styled placeholder or typography-only layout |
| No patents | 「해당 없음」 in a clean card |
| Section absent | Omit from deck |
| Ambiguous gap | Ask user |

## `slide_plan` entry

```json
{
  "num": "08",
  "kind": "capability",
  "header": "책임자 역량 - (위탁) 인하대학교",
  "action_title": "...",
  "include": true
}
```

Logic: `parse_hwp.py` → `build_slide_plan()`. Layout is **not** prescribed by kind.
