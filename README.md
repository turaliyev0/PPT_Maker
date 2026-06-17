# PptMaker

**AI-powered Korean R&D HWP → polished PPTX presentation.**

Attach a `.hwp` file to the Cursor AI agent and it handles everything: extracting text and embedded images, designing visually strong HTML slides, and converting them to a ready-to-present `.pptx` file.

---

## How it works

```
input.hwp
    │
    ├─ extract_hwp_text.py  ──► templates/extracted/   (text + bindata images)
    ├─ parse_hwp.py          ──► slide_plan JSON
    │
    ├─ AI designs slides     ──► slides/*.html          (1280×720, inline CSS)
    │
    └─ html_to_pptx.mjs      ──► presentation.pptx
```

The agent reads the `.cursor/skills/pptmaker/SKILL.md` workflow and does every step autonomously — no manual commands needed.

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.9+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| Cursor IDE | latest | [cursor.com](https://cursor.com) |

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/your-username/PptMaker.git
cd PptMaker

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Node.js dependencies
npm install
```

---

## Usage

### Basic

1. Copy your HWP file into the project root and name it `input.hwp`
2. Open the project in **Cursor**
3. In the chat, attach `input.hwp` and say:

   > *"Read the skill and create the presentation from input.hwp"*

4. The agent runs the full pipeline and delivers `presentation.pptx`

### With reference images

If you have existing presentation slides, professor portraits, or other reference images, put them in a folder (e.g., `presentation_1-images/`) and mention it in the chat:

> *"Use input.hwp and the images in @presentation_1-images as reference"*

The agent will use:
- **Professor portraits** → PI photo in capability slides
- **Award/certificate images** → displayed as document thumbnails
- **Previous slide screenshots** → style/color reference only

### Improving an existing deck

After the initial delivery, provide feedback in plain language:

> *"Page 5 has too much empty space. Page 8 images are too small. Add more details about the professors."*

The agent will re-examine QA screenshots, fix the identified slides, and reconvert.

---

## Output

| File | Description |
|------|-------------|
| `presentation.pptx` | Final presentation (16:9, ready for PowerPoint / Keynote) |
| `slides/*.html` | Individual slide previews (open in browser) |
| `slides/index.html` | Full deck thumbnail preview |

---

## Project structure

```
PptMaker/
├── scripts/
│   ├── extract_hwp_text.py    # HWP → text + embedded images
│   ├── parse_hwp.py           # text → slide_plan JSON
│   ├── build_html_from_plan.py # (optional) content scaffold
│   ├── slide_images.py         # bindata image resolver
│   └── html_to_pptx.mjs        # HTML slides → PPTX
│
├── templates/
│   └── extracted/              # auto-generated, gitignored
│
├── slides/                     # designed HTML slides (tracked)
├── presentation_1-images/      # user reference images (tracked)
│
├── .cursor/
│   └── skills/pptmaker/
│       ├── SKILL.md            # agent workflow & design rules
│       └── references/         # design guides
│
├── requirements.txt
├── package.json
└── input.hwp                   # your source document
```

---

## Configuration

The agent's behavior is controlled by two files:

| File | Purpose |
|------|---------|
| `AGENTS.md` | Top-level rule: attach `.hwp` → run workflow |
| `.cursor/skills/pptmaker/SKILL.md` | Full workflow: steps, design rules, empty-space fixes, layout patterns |

Edit `SKILL.md` to adjust slide count targets, color preferences, or add new layout patterns.

---

## Python dependencies

```
hwp5       # HWP file parsing
pymupdf    # PDF fallback extraction
Pillow     # Image sizing and validation
```

## Node.js dependencies

```
pptxgenjs  # PPTX generation
puppeteer  # Headless Chrome for HTML → image → PPTX
```

---

## Notes

- **Supported input:** `.hwp` (HWP 5.x), `.pdf` (limited, via `extract_pdf_images.py`)
- **Slide canvas:** 1280×720 px (16:9), rendered at 2× for crisp PPTX images
- **Language:** optimized for Korean R&D proposals (과제 신청서, 사업계획서)
- **Fonts:** Malgun Gothic / 맑은 고딕 (built-in on Windows); falls back to sans-serif on other platforms

---

## License

MIT
