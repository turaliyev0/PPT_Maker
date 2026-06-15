# Figures — selection, sizing, placement

Bad image handling is the #1 way a deck fails. Follow this file strictly.

## Step A — Inventory before designing (mandatory)

Before writing any slide HTML:

1. Open `templates/extracted/{stem}-figures.json` and list every bindata image with its caption.
2. **View each image file** in `bindata/` yourself (open the file — do not rely on the caption alone).
3. Record for each image:
   - natural width × height in px (run: `python -c "from PIL import Image; import glob; [print(p, Image.open(p).size) for p in sorted(glob.glob('templates/extracted/*-hwp-full/bindata/*'))]"`)
   - aspect ratio (W/H)
   - content class: `photo` (real-world photo), `diagram` (flowchart/architecture/schematic), `chart` (axes, numbers, data), `screenshot`, `portrait` (person), `logo/seal`
   - one-line description of what it actually shows
4. Build a figure→slide assignment table BEFORE designing. Every assignment must answer: "does this image illustrate THIS slide's facts?" If no slide is a genuine match, **do not use the image at all**. An unused figure is fine; a mismatched figure is a defect.

Hard mismatches to reject: market/industry charts on 책임자 역량 slides, generic campus/building photos on 사업화 slides, robot statistics on slides about cooling systems. If the caption topic ≠ slide topic, it does not go on the slide.

**No bindata match?** Merge the slide content elsewhere or redesign without a photo — do not leave a text-only slide with large empty margins.

## Step B — Sizing rules (aspect ratio drives the layout)

**The container adapts to the image — never the reverse.**

1. Compute the image's aspect ratio first, then choose a layout slot whose proportions are within ~20% of it. A 3:1 wide diagram gets a full-width row; a 3:4 portrait gets a narrow column; a 4:3 photo gets roughly a 4:3 well.
2. `object-fit` policy by content class:
   - `chart`, `diagram`, `screenshot`: **always `object-fit: contain`**, never `cover`. Cropping a chart's axis or a diagram's edge is an automatic failure.
   - `photo`: `cover` allowed only when the crop loses nothing important (verify by viewing); otherwise `contain`.
   - `portrait`: fixed-ratio frame (e.g. 3:4), `cover`, face centered.
3. When using `contain`, the container's aspect must be close to the image's — if `contain` would leave letterbox bands thicker than ~10% of the container, resize the container instead of accepting dead bands. White/transparent letterbox on a white panel is acceptable; gray placeholder backgrounds behind images are not.
4. Minimum useful size: if an image would render smaller than ~360px wide (charts/diagrams: ~480px) it is too small to read — give it a bigger slot or drop it.
5. Never scale an image past ~1.5× its natural pixel width (blurry after the 2× Puppeteer screenshot).

## Step C — Placement rules

1. **No floating-image bands.** Never center one or two small images inside a full-width strip. If a row contains images, the images (plus small gaps/captions) must fill ≥ 90% of the row's width — otherwise restructure: make it a text+image split, enlarge one image, or move the image to another slide.
2. **Size = information value.** Charts and process diagrams that carry the slide's argument may take 50–60% of the canvas. Decorative photos take ≤ 25–30% and never more area than the slide's text content. A purely decorative image next to an empty/「해당 없음」 panel is wrong — shrink the image and merge panels, or cut the image.
3. **Side-by-side images** must share the same rendered height, with equal gaps, captions underneath in a consistent style. Don't pair images with wildly different aspect ratios in one row; stack or separate them instead.
4. Charts extracted from the HWP keep their full frame visible: axis labels, legend, source line. If part of a chart is unreadable at the planned size, either enlarge it or rebuild the numbers as a CSS chart/stat row instead of embedding the image.
5. Every placed image gets explicit `width`/`height` or a sized flex/grid cell — never rely on intrinsic size to "work out".

## Step D — Visual QA on rendered output (mandatory, after Step 4 conversion)

After producing `presentation.pptx`, render and inspect it:

```bash
soffice --headless --convert-to pdf presentation.pptx
pdftoppm -jpeg -r 100 presentation.pdf qa/slide
```

View every `qa/slide-*.jpg` and check images specifically:

- [ ] No chart/diagram is cropped (axes, legends, edges all visible)
- [ ] No image is stretched or in a container of clearly wrong aspect
- [ ] No row of images floating in > 10% empty band space
- [ ] Every image is topically relevant to its slide
- [ ] No image appears twice (PI photo exception)
- [ ] No gray/empty letterbox zones around images

Fix offending `slides/*.html`, re-run Step 4, re-check only the fixed slides. Do not deliver until this checklist passes.
