# PptMaker

**AI-powered Korean R&D HWP → polished PPTX presentation.**

Give an AI agent your `.hwp` file and it handles everything: pulling the latest workflow, extracting text and embedded images, designing visually strong HTML slides, and converting them to a ready-to-present `.pptx` file.

---

## How it works

```
input.hwp
    │
    ├─ Step 0 ──► git pull (latest scripts from GitHub)
    │             verify Python + dependencies
    │
    ├─ Step 1 ──► extract_hwp_text.py + parse_hwp.py
    │             → templates/extracted/  (text + bindata images + slide_plan JSON)
    │
    ├─ Step 2 ──► inventory all images (bindata + user-provided)
    │
    ├─ Step 3 ──► plan slides (12–18, merged/trimmed)
    │
    ├─ Step 4 ──► AI designs slides/*.html  (1280×720, inline CSS)
    │
    ├─ Step 5 ──► html_to_pptx.mjs  → presentation.pptx
    │
    └─ Step 6 ──► image QA (screenshot, inspect, fix, reconvert)
```

The agent reads `WORKFLOW.md` and executes every step autonomously — no manual commands needed.

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.8+ | [python.org](https://www.python.org/downloads/) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| AI agent | any (Claude, GPT, Gemini, Cursor, etc.) | — |

---

## Installation

```bash
# Clone the repo
git clone https://github.com/turaliyev0/PPT_Maker.git
cd PPT_Maker

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

---

## Usage

### Basic

1. Copy your HWP file into the project root (any name, e.g. `input.hwp`)
2. Open the project in your AI agent or IDE
3. Provide the HWP file and say:

   > *"Read WORKFLOW.md and create the presentation from input.hwp"*

4. The agent runs the full pipeline and delivers `presentation.pptx`

### With reference images

Drop any images into the **`preloadable_images/`** folder before running the agent — no need to mention them explicitly:

```
preloadable_images/
├── prof_kim.jpg          ← PI portrait
├── award_2023.png        ← award certificate
└── old_slide_ref.jpg     ← style reference
```

The agent scans this folder automatically and incorporates relevant images:

| Image type | How it's used |
|------------|---------------|
| Professor / PI portrait | PI photo in the matching capability slide |
| Award certificate / 표창장 | Document thumbnail in the matching slide |
| Previous slide screenshots | Style / color reference only |
| High-res diagram or render | Preferred over a lower-res HWP bindata version |

> Images are **not mandatory** — the agent only uses them where they fit. See `preloadable_images/README.md` for full guidance.

### Improving an existing deck

After the initial delivery, provide feedback in plain language:

> *"Page 5 has too much empty space. Page 8 image is stretched. Add more professor details."*

The agent re-examines QA screenshots, fixes the identified slides, and reconverts.

---

## Output

| File | Description |
|------|-------------|
| `presentation.pptx` | Final deck (16:9, ready for PowerPoint / Keynote) |
| `slides/*.html` | Individual slide previews (open in any browser) |
| `slides/index.html` | Full deck thumbnail preview |

---

## Project structure

```
PptMaker/
├── scripts/
│   ├── extract_hwp_text.py      # HWP → text + embedded images
│   ├── parse_hwp.py             # text → slide_plan JSON
│   ├── build_html_from_plan.py  # (optional) content scaffold
│   ├── slide_images.py          # bindata image resolver
│   └── html_to_pptx.mjs         # HTML slides → PPTX
│
├── references/                  # design & pipeline guides (see below)
│
├── preloadable_images/          # ← drop your images here before running
│   └── README.md                # usage guide for this folder
│
├── templates/
│   └── extracted/               # auto-generated, gitignored
│
├── slides/                      # designed HTML slides (output)
│
├── WORKFLOW.md                  # full agent workflow & design rules
├── AGENTS.md                    # Cursor/agent bootstrap rule
├── requirements.txt
└── package.json
```

---

## Configuration

The agent's behavior is controlled by two files:

| File | Purpose |
|------|---------|
| `AGENTS.md` | Bootstrap rule: receive `.hwp` → run `WORKFLOW.md` |
| `WORKFLOW.md` | Full workflow: steps, design rules, empty-space fixes, layout patterns |

Edit `WORKFLOW.md` to adjust slide count targets, color preferences, or add new layout patterns.

---

## References

Detailed guides in `references/`:

| File | Contents |
|------|----------|
| `references/figures.md` | Figure selection, aspect-ratio sizing, QA checklist |
| `references/visual-design.md` | Design principles, anti-patterns |
| `references/html-slides.md` | Canvas, typography, layout ideas |
| `references/slide-structure.md` | R&D section skeleton |
| `references/pipeline.md` | JSON fields, paths |
| `references/html-to-pptx.md` | Conversion details |

---

## Python dependencies

```
olefile        # HWP binary parsing
beautifulsoup4 # HTML parsing
Pillow         # image sizing and validation
```

## Node.js dependencies

```
pptxgenjs      # PPTX generation
puppeteer      # headless Chrome for HTML → image → PPTX
```

---

## Notes

- **Supported input:** `.hwp` (HWP 5.x)
- **Slide canvas:** 1280×720 px (16:9), rendered at 2× for crisp PPTX images
- **Language:** optimized for Korean R&D proposals (과제 신청서, 사업계획서)
- **Fonts:** Malgun Gothic / 맑은 고딕 (built-in on Windows); falls back to sans-serif elsewhere
- **Offline use:** if the GitHub pull in Step 0 fails, the agent continues with the local copy

---

## License

MIT
