#!/usr/bin/env node
/** Convert slides/*.html to presentation.pptx via Puppeteer screenshots + PptxGenJS. */
import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";
import puppeteer from "puppeteer";
import PptxGenJS from "pptxgenjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

const slidesDir = path.resolve(ROOT, process.argv[2] || "slides");
const outFile = path.resolve(ROOT, process.argv[3] || "presentation.pptx");

const files = fs
  .readdirSync(slidesDir)
  .filter((f) => f.endsWith(".html") && f !== "index.html")
  .sort();

if (!files.length) {
  console.error(`No slide HTML files in ${slidesDir}. Run build_html_from_plan.py first.`);
  process.exit(1);
}

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_16x9";
pptx.author = "PptMaker";

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 2 });

for (const file of files) {
  const filePath = path.join(slidesDir, file);
  const url = pathToFileURL(filePath).href;
  await page.goto(url, { waitUntil: "networkidle0", timeout: 60000 });
  await page.evaluateHandle("document.fonts.ready");
  await page.addStyleTag({
    content: "*, *::before, *::after { animation: none !important; transition: none !important; }",
  });
  const png = await page.screenshot({ type: "png", fullPage: false });
  const slide = pptx.addSlide();
  slide.addImage({
    data: `image/png;base64,${png.toString("base64")}`,
    x: 0,
    y: 0,
    w: "100%",
    h: "100%",
  });
  console.log(`  + ${file}`);
}

await browser.close();
await pptx.writeFile({ fileName: outFile });
console.log(`Wrote ${outFile} (${files.length} slides)`);
