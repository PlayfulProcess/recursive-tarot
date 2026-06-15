#!/usr/bin/env node
// orchestrate.mjs — the spine. Source → TTS/align → manifest → record (Chrome) → ffmpeg mux →
// a sequence+performance grammar with REAL timestamps.
//
//   node orchestrate.mjs ../productions/alice-in-wonderland
//
// Reads config.json (or config.example.json). For "provided" TTS, expects per-passage audio at
// <production>/<tts.providedAudioDir>/<passage.id>.(wav|mp3) — drop your better audiobook there.
import { readFile, writeFile, mkdir, access } from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, resolve, join } from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import ffmpegPath from 'ffmpeg-static';
import { synthesize } from './tts/index.mjs';
import { record } from './recorder.mjs';
const exec = promisify(execFile);
const __dir = dirname(fileURLToPath(import.meta.url));

async function loadConfig() {
  for (const f of ['config.json', 'config.example.json'])
    try { return JSON.parse(await readFile(resolve(__dir, f), 'utf8')); } catch {}
  throw new Error('no config.json / config.example.json');
}
async function findAudio(dir, id) {
  for (const ext of ['wav', 'mp3', 'm4a', 'ogg'])
    try { const p = join(dir, `${id}.${ext}`); await access(p); return p; } catch {}
  return null;
}

async function main() {
  const prod = resolve(process.argv[2] || '../productions/alice-in-wonderland');
  const cfg = await loadConfig();
  const grammar = JSON.parse(await readFile(join(prod, 'grammar.json'), 'utf8'));
  const work = resolve(__dir, cfg.paths.work), out = resolve(__dir, cfg.paths.out);
  await mkdir(work, { recursive: true });
  const audioDir = join(prod, cfg.tts.providedAudioDir || 'audio');

  // 1) per-passage audio + marks
  const passages = [];
  for (const it of grammar.items) {
    const lines = (it.sections?.Text || '').split(/(?<=[.!?])\s+/).filter(Boolean);
    const linesArr = it._lines || lines;   // prefer real karaoke lines if carried
    const opts = { lines: linesArr, voice: cfg.tts.voice };
    if (cfg.tts.engine === 'provided') {
      opts.audioIn = await findAudio(audioDir, it.id);
      if (!opts.audioIn) { console.warn(`! no audio for ${it.id} in ${audioDir} — skipping`); continue; }
      opts.aligner = cfg.tts.align;
    } else { opts.outPath = join(work, `${it.id}.mp3`); }
    const { audioPath, marks } = await synthesize(cfg.tts.engine, opts);
    const dur = marks.length ? marks[marks.length - 1].t1 + 0.4 : 4;
    passages.push({ id: it.id, title: it.name, image_url: it.image_url,
                    svg: it.metadata?._svg || null, lines: linesArr,
                    audio: pathToFileURL(audioPath).href, audioDur: +dur.toFixed(2), marks });
  }
  const manifest = { title: grammar.name, gap: 1.0, passages };
  await writeFile(join(work, 'manifest.json'), JSON.stringify(manifest, null, 2));

  // 2) record the silent video of the timeline
  const webm = join(out, 'clip.webm');
  const { durationSec } = await record({ manifest, out: webm,
    headless: cfg.headless, fullscreen: cfg.fullscreen, viewport: cfg.viewport });

  // 3) mux: place each passage audio at its timeline start, mix, overlay on the video
  const mp4 = join(out, 'final.mp4');
  await muxAV(webm, manifest, mp4);

  // 4) write the grammar with real timestamps
  let t = 0;
  for (const it of grammar.items) {
    const p = passages.find(x => x.id === it.id); if (!p) continue;
    it.performance = it.performance || {};
    it.performance.overlays = p.marks.map(m => ({ kind: 'text', content: p.lines[m.line],
      start_sec: +(t + m.t0).toFixed(2), end_sec: +(t + m.t1).toFixed(2) }));
    it.performance.start_sec = +t.toFixed(2);
    it.performance.end_sec = +(t + p.audioDur).toFixed(2);
    it.metadata = { ...(it.metadata || {}), narration: 'tts:' + cfg.tts.engine, video: 'final.mp4' };
    t += p.audioDur + manifest.gap;
  }
  grammar.metadata = { ...(grammar.metadata || {}), recorded: true, media: 'final.mp4',
                       duration_sec: +durationSec.toFixed(2) };
  await writeFile(join(prod, 'grammar.json'), JSON.stringify(grammar, null, 2));
  console.log(`done → ${mp4}\n      ${join(prod, 'grammar.json')} updated with real timestamps`);
}

async function muxAV(videoIn, manifest, outPath) {
  // build: -i video -i a1 -i a2 ... ; adelay each audio to its start; amix; map video+mix
  const args = ['-y', '-i', videoIn];
  const fps = []; let starts = [], t = 0;
  for (const p of manifest.passages) { starts.push(t); args.push('-i', fileURLToPath(p.audio)); t += p.audioDur + manifest.gap; }
  const filt = manifest.passages.map((p, i) =>
    `[${i + 1}:a]adelay=${Math.round(starts[i] * 1000)}|${Math.round(starts[i] * 1000)}[a${i}]`).join(';');
  const mix = manifest.passages.map((_, i) => `[a${i}]`).join('') +
              `amix=inputs=${manifest.passages.length}:normalize=0[aout]`;
  args.push('-filter_complex', `${filt};${mix}`, '-map', '0:v', '-map', '[aout]',
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', outPath);
  await exec(ffmpegPath, args);
}

main().catch(e => { console.error(e); process.exit(1); });
