// align/forced-align.mjs — get per-word timestamps for EXISTING audio + its transcript.
// Wraps a CLI aligner (WhisperX preferred; aeneas fallback). Returns [{word,t0,t1}] (seconds).
//
// WhisperX:  pip install whisperx   → word-level timestamps from ASR + alignment.
// aeneas:    pip install aeneas      → forced alignment to a given transcript.
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { readFile, writeFile, mkdtemp } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
const exec = promisify(execFile);

export async function forcedAlign({ audioIn, text, aligner = 'whisperx' }) {
  if (aligner === 'whisperx') return whisperx(audioIn);
  if (aligner === 'aeneas') return aeneas(audioIn, text);
  throw new Error(`unknown aligner "${aligner}"`);
}

async function whisperx(audioIn) {
  const dir = await mkdtemp(join(tmpdir(), 'rr-align-'));
  // produces <name>.json with segments[].words[] = {word,start,end}
  await exec('whisperx', [audioIn, '--align_model', 'WAV2VEC2_ASR_LARGE_LV60K_960H',
                          '--output_format', 'json', '--output_dir', dir]);
  const base = audioIn.split('/').pop().replace(/\.[^.]+$/, '');
  const j = JSON.parse(await readFile(join(dir, base + '.json'), 'utf8'));
  const out = [];
  for (const seg of j.segments || [])
    for (const w of seg.words || [])
      if (w.start != null && w.end != null) out.push({ word: w.word.trim(), t0: w.start, t1: w.end });
  return out;
}

async function aeneas(audioIn, text) {
  const dir = await mkdtemp(join(tmpdir(), 'rr-aeneas-'));
  const txt = join(dir, 'words.txt'), outJ = join(dir, 'out.json');
  await writeFile(txt, text.split(/\s+/).join('\n'));   // one word per line
  await exec('python3', ['-m', 'aeneas.tools.execute_task', audioIn, txt,
    'task_language=eng|is_text_type=plain|os_task_file_format=json', outJ]);
  const j = JSON.parse(await readFile(outJ, 'utf8'));
  return (j.fragments || []).map(f => ({ word: (f.lines || [''])[0], t0: +f.begin, t1: +f.end }));
}
