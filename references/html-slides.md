# HTML slides — canvas & design toolkit

Fixed canvas **1280×720**. Inline CSS in each file. **You choose the layout** — below is a strong baseline, not a mandatory template.

## Typography baseline (minimum sizes)

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1280px; height: 720px;
  font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
  background: #ffffff; color: #16181d;
  padding: 56px 64px; overflow: hidden;
}
.kicker   { font-size: 14px; font-weight: 700; letter-spacing: .12em; color: #6b7280; text-transform: uppercase; }
.headline { font-size: 36px; font-weight: 800; color: #16181d; line-height: 1.2; margin: 10px 0 32px; }
.headline em { color: #1F4E79; font-style: normal; }   /* accent words, not accent bars */
.body     { font-size: 17px; line-height: 1.6; color: #2c2f36; }
.body li  { margin-bottom: 10px; list-style: none; }
.divider  { border: 0; border-top: 1px solid #e3e6ea; margin: 20px 0; }  /* hairline, the ONLY default separator */
.stat     { font-size: 64px; font-weight: 800; color: #1F4E79; line-height: 1; }
.stat-label { font-size: 15px; color: #6b7280; margin-top: 8px; }
.surface  { background: #f4f7fb; border-radius: 14px; padding: 28px 32px; }  /* max ONE per slide, for the focal element only */
table     { border-collapse: collapse; width: 100%; font-size: 15px; }
th        { text-align: left; font-weight: 700; color: #1F4E79; border-bottom: 2px solid #1F4E79; padding: 10px 12px; }
td        { border-bottom: 1px solid #e3e6ea; padding: 10px 12px; }
```

**No `.card` wrappers.** Do not wrap each content section in a bordered/shaded box. Content sits on the white canvas; use the typographic grid, hairline dividers, and at most one `.surface` per slide for the focal element. Tables use header rule + hairline rows, never an enclosing border box.

```css
/* Size the container to the image, not the image to the container */
.img-well { display: flex; align-items: center; justify-content: center; }
.img-well img { width: 100%; height: 100%; object-fit: contain; } /* charts, diagrams, screenshots */
.img-well.photo img { object-fit: cover; }                         /* photos only, after verifying the crop */
```

Adjust per slide — a stat slide might use 48px numbers; a dense table slide might use 15px cells but never 10px.

## Page architectures (rotate — never two identical in a row)

**Split (workhorse)** — image/diagram fills one side full-height to the slide edge (45–60% width, sized to its aspect ratio); text column on the other side with kicker + headline + ≤ 5 points.

**Editorial** — headline across the top third; below it 2–3 text columns separated by whitespace or hairlines; one accent stat or small figure anchors a corner.

**Big-number row** — 3–4 `.stat` numbers across the middle with labels; one short context line below; nothing boxed.

**Full-bleed** — image or `#1F4E79` field covers all 1280×720; a translucent or solid text panel overlays one side (this is the one place a panel is expected).

**Diagram-led** — one HWP diagram at ≥ 55% canvas, `object-fit: contain`, title above, 2–3 short annotations beside/below it.

**Table-led** — the table IS the slide: title + one-line takeaway, then a well-typeset table (header rule, hairline rows, generous 10–12px cell padding).

**Timeline** — horizontal line with year markers and stacked labels; type and spacing only, no pill borders unless they earn it.

**Dark cover/closing** — full-bleed `#1F4E79`→`#2E75B6` gradient, white 44–56px title, minimal meta line.

## Image paths & sizing

```html
<img src="../templates/extracted/input-hwp-full/bindata/BIN0012.png" alt="설명">
```

- Look up each image's natural W×H (figures inventory) and give its container matching proportions
- Charts/diagrams: `object-fit: contain`, full frame visible — cropped axes = failure
- Photos: `cover` allowed only if the crop was verified by viewing the image
- Use captions from `*-figures.json` for `alt` text; each bindata file once per deck (PI photo exception)
- Don't upscale past ~1.5× natural width; don't render charts narrower than ~480px

## File naming

```
slides/01-cover-표지.html
slides/08-capability-경안써머텍.html
slides/index.html
```

Prefix = order from `slide_plan`.

## Workflow

1. Read parsed JSON for text, tables, figure map
2. Optionally skim `slides/_draft/` from the builder for raw content
3. **Write final HTML yourself** — unique CSS per slide is encouraged
4. `node scripts/html_to_pptx.mjs slides/ presentation.pptx`

Content from HWP only. Design from your judgment.
