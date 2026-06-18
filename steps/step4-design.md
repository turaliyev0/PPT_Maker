# Step 4 — Design HTML slides

## Canvas setup

Fixed canvas **1280×720 px**. Inline CSS in every file. `overflow: hidden` — nothing may extend beyond the canvas.

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1280px; height: 720px;
  font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
  background: #ffffff; color: #16181d;
  padding: 56px 64px; overflow: hidden;
}
```

**No `.card` wrappers.** Content sits on the white canvas. Use the typographic grid, hairline dividers, and at most one `.surface` per slide for the single focal element.

---

## Typography (minimum sizes — never go below these)

| Role | Size | Weight | Notes |
|------|------|--------|-------|
| Kicker / section label | 14–16px | 700 | Muted, uppercase, letter-spaced |
| Headline / action title | 28–40px | 800 | The dominant text element |
| Body / bullets | 16–20px | 400 | line-height 1.45–1.6 |
| Table cells | 14–16px | — | Never 10px |
| Stat number | 56–72px | 800 | Color `#1F4E79` |
| Footnotes | 13px | — | Absolute floor |

```css
.kicker   { font-size: 14px; font-weight: 700; letter-spacing: .12em; color: #6b7280; text-transform: uppercase; }
.headline { font-size: 36px; font-weight: 800; color: #16181d; line-height: 1.2; margin: 10px 0 32px; }
.headline em { color: #1F4E79; font-style: normal; }
.body     { font-size: 17px; line-height: 1.6; color: #2c2f36; }
.body li  { margin-bottom: 10px; list-style: none; }
.divider  { border: 0; border-top: 1px solid #e3e6ea; margin: 20px 0; }
.stat     { font-size: 64px; font-weight: 800; color: #1F4E79; line-height: 1; }
.stat-label { font-size: 15px; color: #6b7280; margin-top: 8px; }
.surface  { background: #f4f7fb; border-radius: 14px; padding: 28px 32px; }
table     { border-collapse: collapse; width: 100%; font-size: 15px; }
th        { text-align: left; font-weight: 700; color: #1F4E79; border-bottom: 2px solid #1F4E79; padding: 10px 12px; }
td        { border-bottom: 1px solid #e3e6ea; padding: 10px 12px; }
```

---

## Separation rules

1. Separate content groups with **whitespace and column alignment first**, thin hairline dividers second, tinted surfaces last.
2. Maximum **one** tinted surface per slide — for the single most important element only.
3. Section headings styled with type (size, weight, letter-spacing, color) — **never** accent bars, pills, or boxes.
4. Tables and lists sit directly on the canvas with hairline row rules — not inside an outlined card.

---

## Page architectures — rotate, never repeat two in a row

**Split (workhorse)** — image/diagram fills one side full-height to the slide edge (45–60% width); text column on the other with kicker + headline + ≤ 5 bullets.

**Editorial** — headline across the top third; below it 2–3 text columns separated by whitespace or hairlines; one accent stat or small figure anchors a corner.

**Big-number row** — 3–4 oversized stats (`.stat`) across the middle with labels; short context line below; nothing boxed.

**Full-bleed** — image or `#1F4E79` field covers all 1280×720; translucent or solid text panel overlays one side (the one place a panel is expected).

**Diagram-led** — one HWP diagram at ≥ 55% canvas, `object-fit: contain`, title above, 2–3 short annotations beside/below.

**Table-led** — the table IS the slide: title + one-line takeaway, then a well-typeset table (header rule, hairline rows, 10–12px padding).

**Timeline** — horizontal line with year markers and stacked labels; type and spacing only.

**Dark cover/closing** — full-bleed `#1F4E79`→`#2E75B6` gradient, white 44–56px title, minimal meta line.

| Content type | Architecture ideas |
|---|---|
| Cover | Full-bleed dark or full-bleed image; bold 44–56px title stack |
| Goals / background | Large headline + 3 punchy bullets OR hero diagram + caption strip |
| Performance / budget | CSS bar charts with big labels |
| Capability | 3-column: PI column + main column + patents column |
| Execution / method | Diagram-led or Split |
| Schedule | Timeline |
| Closing | Minimal, centered, generous whitespace |

---

## Image handling in HTML

```css
/* Size the container to the image — never the reverse */
.img-well { display: flex; align-items: center; justify-content: center; }
.img-well img { width: 100%; height: 100%; object-fit: contain; }  /* charts, diagrams */
.img-well.photo img { object-fit: cover; }                          /* photos — only after verifying crop */
```

```html
<img src="../templates/extracted/input-hwp-full/bindata/BIN0012.png" alt="설명">
```

- Give every image container proportions that match the image's natural aspect ratio
- Charts / diagrams: always `object-fit: contain` — cropped axes = automatic failure
- Photos: `cover` only after verifying the crop loses nothing important
- Never upscale past ~1.5× natural width
- Never render a chart narrower than ~480px
- Every placed image needs explicit `width`/`height` or a sized flex/grid cell — never rely on intrinsic size

---

## Anti-patterns — detect and fix

| Problem | Fix |
|---------|-----|
| Gray background + outlined white panels | White canvas; ≤ 1 tinted surface per slide |
| Vertical accent bar / pill before every heading | Style headings with typography only |
| Navy header bar repeated on every slide | Large type on canvas; dark fields for cover/closing only |
| Same architecture on consecutive slides | Rotate — see architectures above |
| Half-empty panels | Delete the box; size columns to content; merge sparse sections |
| `justify-content: space-between` in a tall column with sparse items | Switch to natural `padding` per item; add fill element below |
| `margin-top: auto` on image at bottom of column | Remove it; add a highlight box or metric row before the image |
| Fixed small px on cert/award image | Use `width:100%; height:auto` — container width controls size |
| `<img>` with no explicit width inside a flex column | Always set `width:100%; height:auto; object-fit:contain` |
| Wide-AR image (AR > 2.5:1) in a flex column | Wrap in tinted panel (`background:#f0f5fb; padding:14px`) or add spec-strip below |
| Image smaller than 25% of its surrounding column | Enlarge or restructure |
| Image stuck to a corner | Fix container alignment |
| Blank area > ~80px with nothing in it | Add fill content or restructure |
| 10–12px body text | Rewrite copy shorter; increase font size |
| Delivering scaffold output unchanged | Always redesign HTML yourself |

---

## File naming

```
slides/01-cover-표지.html
slides/08-capability-경안써머텍.html
slides/index.html
```

Prefix = order from `slide_plan`.

---

## Pre-slide checklist (before moving to the next slide)

- [ ] Layout architecture is different from the previous slide
- [ ] This image has not appeared on any earlier slide
- [ ] Every image has `width`/`height` or a sized flex cell — no intrinsic sizing
- [ ] No `justify-content: space-between` in a tall column with sparse items
- [ ] No `margin-top: auto` pushing an image to the bottom
- [ ] No fixed small `px` dimensions on cert images
- [ ] Container aspect matches image aspect (letterbox bands < 10%)
- [ ] No empty zone > ~80px

---

## Before-PPTX self-review

- [ ] Nothing under 14px (13px for footnotes only)
- [ ] No HWP image used on more than one slide
- [ ] Every slide looks different from its neighbors
- [ ] Deck feels cohesive but not repetitive
- [ ] No slide looks empty; count is 12–18
- [ ] No slide uses gray-bg + outlined-panels scaffold
- [ ] Every slide has one clear focal element
