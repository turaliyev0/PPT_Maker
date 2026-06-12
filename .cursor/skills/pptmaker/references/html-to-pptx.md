# HTML → PPTX (mandatory Step 4)

PptMaker **always** builds HTML first, then converts to PPTX. This is the only supported output path.

## How it works

1. Agent writes designed `slides/*.html` (1280×720, inline CSS) — optional `_draft` scaffold from `build_html_from_plan.py`
2. `html_to_pptx.mjs` uses **Puppeteer** to screenshot each slide at 2× resolution
3. **PptxGenJS** embeds each PNG as a full-bleed slide in `presentation.pptx`

```bash
npm install
node scripts/html_to_pptx.mjs slides/ presentation.pptx
```

## Tradeoffs

| | Screenshot pipeline (used) |
|--|--|
| Editable in PowerPoint | No — slides are images |
| Korean font fidelity | High — Chromium renders 맑은 고딕 |
| Layout control | CSS — agent can edit HTML between steps |
| Layout iteration | Edit HTML, re-run Step 4 only |

## Future: editable PPTX

If editable text is required later, consider [slide-gen](https://github.com/0-AI-UG/slide-gen) or html2pptx as a separate converter — still HTML-first.
