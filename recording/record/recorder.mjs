#!/usr/bin/env node
// recorder.mjs — open Chrome with Playwright, render a manifest in player/perform.html, and
// record the (silent) video of the karaoke timeline. Audio is muxed later by orchestrate.mjs.
//
//   node recorder.mjs --manifest path/to/manifest.json --out out/clip.webm [--headful] [--fullscreen]
//
// The manifest is INJECTED into the page (window.__manifest) so no static server / file:// fetch
// is needed. Timing comes from the manifest's word marks → deterministic, recordable.
import { chromium } from 'playwright';
import { readFile, mkdir, rename, readdir } from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, resolve, join } from 'node:path';

const __dir = dirname(fileURLToPath(import.meta.url));
const PLAYER = resolve(__dir, '../player/perform.html');

export async function record({ manifest, out, headless = true, fullscreen = false,
                               viewport = { width: 1920, height: 1080 }, extraMs = 1500 }) {
  const data = typeof manifest === 'string'
    ? JSON.parse(await readFile(manifest, 'utf8')) : manifest;

  const outDir = dirname(resolve(out));
  await mkdir(outDir, { recursive: true });

  const args = fullscreen ? ['--start-fullscreen', '--autoplay-policy=no-user-gesture-required']
                          : ['--autoplay-policy=no-user-gesture-required'];
  const browser = await chromium.launch({ headless, args });
  const context = await browser.newContext({
    viewport, recordVideo: { dir: outDir, size: viewport },
  });
  const page = await context.newPage();
  // load the player (no manifest in URL — we inject it), audio off (muxed later)
  await page.goto(pathToFileURL(PLAYER).href + '?audio=off');
  await page.waitForFunction('typeof window.__manifest === "function"', { timeout: 15000 });
  await page.evaluate((m) => window.__manifest(m), data);
  await page.waitForFunction('window.__ready === true', { timeout: 15000 });
  const total = await page.evaluate(() => window.__total || 0);
  await page.evaluate(() => window.__start());
  await page.waitForFunction('window.__done === true', { timeout: total * 1000 + 60000 });
  await page.waitForTimeout(extraMs);

  const videoPath = await page.video().path();
  await context.close();            // finalizes the webm
  await browser.close();
  await rename(videoPath, resolve(out));
  return { out: resolve(out), durationSec: total };
}

// CLI
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const a = process.argv.slice(2);
  const get = (f, d) => { const i = a.indexOf(f); return i >= 0 ? a[i + 1] : d; };
  const r = await record({
    manifest: get('--manifest'),
    out: get('--out', 'out/clip.webm'),
    headless: !a.includes('--headful'),
    fullscreen: a.includes('--fullscreen'),
  });
  console.log('recorded', r.out, '(~' + r.durationSec.toFixed(1) + 's timeline)');
}
