#!/usr/bin/env node
/* Records pages/golden-dawn-path.html as PNG frames (and, with ffmpeg on the PATH, an MP4).
   Optional: the page works without it. No npm packages: it drives a local Chrome or Edge
   through the DevTools protocol, using Node 22's built-in WebSocket and fetch.

   1. Serve the repo:            python -m http.server 8765 --bind 127.0.0.1
   (Any one step by hand: pages/golden-dawn-path.html?frame=N&embed=1, N from 0; ?t=4.5 for any moment;
    embed=1 leaves out the site header, footer and assistant.)
   2. One still per step:         node scripts/record_golden_dawn_path.mjs --stills
      The whole movie (30 fps):   node scripts/record_golden_dawn_path.mjs --movie
      Options: --mode ascent|descent   --aspect landscape|portrait (portrait = 9:16)
               --fps 30   --speed 1 (1 = six seconds a step)   --out <folder> (default: the system temp folder)
               --url http://127.0.0.1:8765/pages/golden-dawn-path.html   --chrome <path>
   Frames are drawn by the page's own window.GDPath.render(t), a pure function of time,
   so every frame is exact whatever the machine's speed. --movie then runs:
      ffmpeg -framerate 30 -i <out>/<mode>-%05d.png -c:v libx264 -pix_fmt yuv420p <out>/<mode>.mp4
   Frames are large and temporary: keep them out of the repo, and delete them once encoded. */
import { spawn, spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync, existsSync, mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const arg = (name, dflt) => { const i = process.argv.indexOf('--' + name); return i > 0 && process.argv[i + 1] && !process.argv[i + 1].startsWith('--') ? process.argv[i + 1] : dflt; };
const has = name => process.argv.includes('--' + name);
const mode = arg('mode', 'ascent');
const aspect = arg('aspect', 'landscape');
const fps = Number(arg('fps', 30));
const speed = Number(arg('speed', 1));
const out = arg('out', join(tmpdir(), 'golden-dawn-path-frames'));
const base = arg('url', 'http://127.0.0.1:8765/pages/golden-dawn-path.html');
const [W, H] = aspect === 'portrait' ? [900, 1600] : [1600, 900];
const CANDIDATES = [
  arg('chrome'), process.env.CHROME,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
].filter(Boolean);
const chromePath = CANDIDATES.find(p => existsSync(p));
if (!chromePath) { console.error('No Chrome or Edge found; pass --chrome <path>.'); process.exit(1); }
if (!has('stills') && !has('movie')) { console.error('Say --stills or --movie (see the top of this file).'); process.exit(1); }

const port = 9300 + Math.floor(Math.random() * 500);
const profile = mkdtempSync(join(tmpdir(), 'gdpath-'));
const chrome = spawn(chromePath, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
  '--hide-scrollbars', '--mute-audio', '--no-first-run', `--window-size=${W},${H}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function connect() {
  for (let i = 0; i < 50; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
      const page = list.find(t => t.type === 'page');
      if (page) return page.webSocketDebuggerUrl;
    } catch (e) { /* not up yet */ }
    await sleep(200);
  }
  throw new Error('Chrome did not open its debugging port');
}

let ws, seq = 0;
const waiting = new Map();
function send(method, params = {}) {
  const id = ++seq;
  ws.send(JSON.stringify({ id, method, params }));
  return new Promise((res, rej) => waiting.set(id, { res, rej }));
}
async function evaluate(expression) {
  const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.text + ' ' + (r.exceptionDetails.exception || {}).description);
  return r.result.value;
}
async function shot(file) {
  const r = await send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: W, height: H, scale: 1 } });
  writeFileSync(file, Buffer.from(r.data, 'base64'));
}

try {
  ws = new WebSocket(await connect());
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  ws.onmessage = ev => {
    const m = JSON.parse(ev.data);
    if (m.id && waiting.has(m.id)) { const w = waiting.get(m.id); waiting.delete(m.id); m.error ? w.rej(new Error(m.error.message)) : w.res(m.result); }
  };
  await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: `${base}?mode=${mode}&aspect=${aspect}&t=0&embed=1` });
  for (let i = 0; i < 150; i++) {          // up to 30 s for the deck, glyphs and 22 pictures
    await sleep(200);
    try { if (await evaluate(`document.body && document.body.dataset.ready === '1'`)) break; } catch (e) { /* navigating */ }
  }
  const info = await evaluate(`({ steps: GDPath.steps, sec: GDPath.STEP_SECONDS, hold: GDPath.HOLD_F })`);
  mkdirSync(out, { recursive: true });
  if (has('stills')) {
    for (let i = 0; i < info.steps; i++) {
      await evaluate(`GDPath.render(${i + info.hold})`);
      await sleep(700);                    // a new card's picture decodes after it is placed
      const f = join(out, `${mode}-${aspect}-step-${String(i + 1).padStart(2, '0')}.png`);
      await shot(f);
      console.log(f);
    }
  }
  if (has('movie')) {
    const perStep = info.sec / speed * fps, total = Math.ceil(info.steps * perStep);
    let lastStep = -1;
    for (let k = 0; k < total; k++) {
      await evaluate(`GDPath.render(${k / perStep})`);
      const step = Math.floor(k / perStep);
      if (step !== lastStep) { await sleep(700); lastStep = step; }
      await shot(join(out, `${mode}-${String(k).padStart(5, '0')}.png`));
      if (k % fps === 0) process.stdout.write(`\r${k}/${total} frames`);
    }
    console.log(`\r${total} frames in ${out}`);
    const mp4 = join(out, `${mode}-${aspect}.mp4`);
    const ff = spawnSync('ffmpeg', ['-y', '-framerate', String(fps), '-i', join(out, `${mode}-%05d.png`), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', mp4], { stdio: 'inherit' });
    console.log(ff.status === 0 ? `movie: ${mp4}` : 'ffmpeg not found or failed; the frames are there to encode by hand.');
  }
} finally {
  try { ws && ws.close(); } catch (e) { /* closing */ }
  chrome.kill();
  setTimeout(() => process.exit(0), 300);
}
