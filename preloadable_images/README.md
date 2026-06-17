# preloadable_images

Drop any images here before running the agent. The agent will scan this folder automatically and incorporate relevant images into the presentation.

## What to put here

| Image type | Example filenames | How it's used |
|------------|------------------|---------------|
| Professor / PI portrait photo | `prof_kim.jpg`, `pi_lee.png` | PI photo in the matching capability slide |
| Award certificate / 표창장 / 학술상 | `award_2023.jpg`, `certificate.png` | Document thumbnail in the matching capability slide |
| Previous presentation screenshot | `old_slide_01.png` | Style / color palette reference only |
| High-resolution diagram or render | `system_diagram.png` | Preferred over a lower-res HWP bindata version |

## Notes

- Images are **not mandatory** — the agent uses them only if they match slide content
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`
- Higher resolution is always better — never upscale before placing here
- The agent will never force an image into a slide where it doesn't belong
