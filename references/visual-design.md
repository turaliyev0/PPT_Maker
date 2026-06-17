# Visual design — agent-led

You are a presentation designer. Target look: **modern editorial** — like a deck from a top design agency. Content sits directly on the canvas, organized by whitespace, alignment, and typographic hierarchy — **not by drawing boxes around everything**.

**Default canvas:** white (`#ffffff`) background, generous margins, a strong typographic grid. Dark navy is for the cover/closing and at most 1–2 full-bleed section breaks — not a repeated header bar on every slide.

**Banned scaffold (the #1 failure):** gray page background + multiple outlined white "panel" boxes + a vertical accent bar before each section title, repeated on every slide. Never build slides this way.

**Separation rules:**
- Separate content groups with whitespace and column alignment first, thin hairline dividers second, tinted surfaces last.
- Maximum **one** tinted/elevated surface per slide, used deliberately for the single most important element (a key stat, the highlight column, a callout) — never as a wrapper for every section.
- Section headings are styled with type (size, weight, letter-spacing, color), not with accent bars, pills, or boxes.
- Tables and lists sit directly on the canvas with hairline row rules — not inside an outlined card.

**Each slide has ONE focal point** (a large image, a chart, a big number, or a bold statement) and supporting content arranged around it asymmetrically. If every element has equal visual weight, the slide is wrong.

## Core principles

1. **Typography first** — if text is hard to read on a projector, the slide fails
   - Section label: 14–16px, muted
   - Action title / headline: **28–40px**, bold
   - Body / bullets: **16–20px**, line-height 1.45–1.6
   - Tables: **14–16px** minimum; never 10px
   - Footnotes only: 13px floor

2. **One figure, one home — and the right home** — each HWP bindata image appears **once**, on the slide whose content it actually depicts (see `references/figures.md`)
   - Assign by viewing the image, never by caption keyword match
   - An image whose topic doesn't match the slide topic is worse than no image: leave the slide image-free and design with typography/CSS charts instead
   - Track used figure paths while designing

3. **Layout variety via structure, not boxes** — rotate genuinely different page architectures across the deck:
   - **Split**: full-height image or diagram on one side (45–60% width, bleeding to the slide edge), text column on the other
   - **Editorial columns**: headline zone on top-left, 2–3 ragged text columns below, no enclosing boxes
   - **Big-number row**: 3–4 oversized stats (56–72px) with small labels, hairline separators only
   - **Full-bleed**: image or dark field covering the whole canvas with a text panel overlaid on one side
   - **Diagram-led**: one large diagram center/top (≥ 55% of canvas), short annotations around it
   - **Table-led**: one well-typeset table as the hero, title and one-line takeaway above it
   No two consecutive slides may use the same architecture, and the gray-bg + white-cards scaffold is never one of them.

4. **Visual hierarchy** — one focal point per slide (photo, chart, or headline stat)
   - Supporting text stays secondary; cut copy rather than shrink fonts

5. **Information density** — decks should feel **complete**, not **long**
   - Target **12–18 slides** for a typical R&D HWP; merge 배경+목표, 방법+역할, 수행+선행+연차 per org, 일정+예산, 사업화 목표+전략
   - Drop 목차, 주관기관 단독 소개, 별첨 프로필 unless the user wants a full appendix deck
   - 책임자 역량 stays — one slide per org, with full 이력 on that slide (no duplicate appendix)

6. **Content defines the footprint** — never draw a container first and pour content in
   - A half-empty box is a layout bug: remove the box, let the content sit on the canvas, and rebalance the columns
   - If a section has 3 lines of content, it gets a narrow column or merges with a neighbor — not a full-height panel
   - Whitespace at the canvas edge is good (margins, breathing room); whitespace trapped *inside* a border is bad

7. **Polish with CSS** — gradients, rounded cards, subtle shadows, accent lines, colored section bands
   - Primary anchor `#1F4E79` is a starting point, not a prison — add complementary accents (#E8F4FC, #2E75B6, warm grays)

## When to use what

| Content type | Design ideas |
|--------------|--------------|
| Cover | Full-bleed dark or full-bleed image cover; bold 44–56px title stack |
| Goals / background | Large headline + 3 punchy bullets OR single hero diagram with caption strip |
| Performance / budget | CSS bar/stack charts with big labels; numbers readable at a glance |
| Capability | Large PI photo, history as timeline or cards, patents in a compact grid |
| Execution / method | One strong diagram + short bullets, or dual-panel with distinct images |
| Yearly / schedule | Horizontal timeline with year pills, not a cramped table |
| Closing | Minimal, centered, generous whitespace |
| Any content slide | Pick one architecture from principle 3; never the boxed-panel scaffold |

Charts and numbers must come from parsed HWP data — style them creatively, don't invent values.

## Anti-patterns (fix these)

| Problem | Fix |
|---------|-----|
| Same roadmap image on 5 slides | Assign each figure to its best single slide |
| 10–12px body text | Rewrite copy shorter; increase font size |
| Every slide = image left + bullets right | Change structure slide by slide |
| Full-width bullet list, no visual | Add chart, card layout, or one strong image |
| Gray placeholder boxes everywhere | Design around missing assets (typography-only slide, icon strip, styled 「해당 없음」) |
| Delivering `build_html_from_plan.py` output as-is | Always redesign HTML yourself |
| 30+ slides repeating the same structure | Merge sections; aim for 12–18 slides |
| Slide with title + one bullet and huge whitespace | Redesign layout or merge into another slide |
| Chart/diagram cropped by `object-fit: cover` | Charts and diagrams always use `contain` in a container matched to their aspect ratio |
| Small images centered in a wide empty band | Images fill ≥ 90% of their row, or the layout becomes a text+image split |
| Decorative photo dominating the slide next to a thin/empty panel | Image area proportional to information value; merge panels, shrink or cut the photo |
| Industry/market chart pasted onto an unrelated slide (e.g. 역량, 사업화) | Use figures only where topically relevant; otherwise omit |
| Gray letterbox/placeholder zones around an image | Resize the container to the image's aspect; letterbox bands > 10% mean the slot is wrong |
| Gray background + grid of outlined white panels | White canvas; whitespace and alignment separate content; ≤ 1 tinted surface per slide |
| Vertical accent bar / pill before every section heading | Style headings with typography only (weight, size, spacing, color) |
| Navy header bar repeated on every slide | Slide title as large type on the canvas; reserve dark fields for cover/closing/section breaks |
| Half-empty panels (box bigger than its content) | Delete the box; size columns to content; merge sparse sections |
| Image alone in a full-width strip with empty gutters | Integrate: full-height side image, full-bleed with overlay, or image column matched to its aspect |
| Every element same visual weight | One focal element per slide; everything else clearly secondary |

## Content integrity (unchanged)

- Text and numbers from HWP / parsed JSON only
- Images from `templates/extracted/.../bindata/` via `*-figures.json` paths
- No invented stats, stock photos, or reference-deck copy

## Before PPTX

Quick self-review:

- [ ] Fonts readable (nothing under 14px except tiny labels)
- [ ] No duplicate HWP images (except PI photo pair)
- [ ] Slides look **different** from each other
- [ ] Deck feels cohesive (color palette + spacing rhythm) but not repetitive
- [ ] No slide looks empty; count is ~12–18 unless user asked for more
- [ ] Images pass `references/figures.md` Step D (no crops, no mismatched figures, no floating bands, containers match aspect ratios)
- [ ] No slide uses the gray-bg + outlined-panels scaffold; ≤ 1 tinted surface per slide
- [ ] No two consecutive slides share the same architecture
- [ ] Every slide has one clear focal element

Fix in `slides/*.html`, then run conversion.
