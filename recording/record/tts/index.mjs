// tts/index.mjs — adapter dispatch + the shared mark model.
//
// Every adapter returns: { audioPath, marks } where marks = [{ word, line, wi, t0, t1 }]
//   line = index of the line within the passage, wi = word index within that line,
//   t0/t1 = seconds from the passage's audio start. perform.html highlights by (line, wi).
//
// engine "provided"  → wrap an EXISTING audio file + the passage lines (forced alignment).
// engine "elevenlabs"/"google"/"azure" → synthesize audio AND get marks from the TTS engine.
import { synthesizeProvided } from './provided.mjs';
import { synthesizeElevenLabs } from './elevenlabs.mjs';

const ADAPTERS = {
  provided: synthesizeProvided,
  elevenlabs: synthesizeElevenLabs,
  // google: ...,  azure: ...   (same signature)
};

/** words-with-line-index helper: flatten passage lines → [{word,line,wi}] in reading order. */
export function flattenWords(lines) {
  const out = [];
  lines.forEach((line, li) =>
    line.split(/\s+/).filter(Boolean).forEach((w, wi) =>
      out.push({ word: w.replace(/[^\p{L}\p{N}']/gu, ''), raw: w, line: li, wi })));
  return out;
}

/** Map a flat list of timed words (from alignment/TTS) onto the passage's (line, wi) slots. */
export function attachLineIndex(lines, timedWords) {
  const slots = flattenWords(lines);
  const n = Math.min(slots.length, timedWords.length);
  const marks = [];
  for (let i = 0; i < n; i++) {
    marks.push({ word: slots[i].raw, line: slots[i].line, wi: slots[i].wi,
                 t0: timedWords[i].t0, t1: timedWords[i].t1 });
  }
  return marks;
}

export async function synthesize(engine, opts) {
  const fn = ADAPTERS[engine];
  if (!fn) throw new Error(`unknown tts engine "${engine}" (have: ${Object.keys(ADAPTERS).join(', ')})`);
  return fn(opts);   // → { audioPath, marks }
}
