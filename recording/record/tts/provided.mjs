// tts/provided.mjs — PRIMARY path: you already have a (better) audiobook.
// Input: an existing audio file for the passage + the passage lines.
// Output: { audioPath, marks } — word timestamps obtained by FORCED ALIGNMENT of the audio to
// the text (align/forced-align.mjs). If a marks JSON is supplied alongside the audio, use it.
import { readFile, access } from 'node:fs/promises';
import { forcedAlign } from '../align/forced-align.mjs';
import { attachLineIndex } from './index.mjs';

export async function synthesizeProvided({ lines, audioIn, marksIn, aligner = 'whisperx' }) {
  if (!audioIn) throw new Error('provided TTS needs `audioIn` (path to the existing audio file)');

  // 1) if pre-computed word marks were supplied, trust them
  if (marksIn) {
    const timed = JSON.parse(await readFile(marksIn, 'utf8'));   // [{word,t0,t1}, ...]
    return { audioPath: audioIn, marks: attachLineIndex(lines, timed) };
  }

  // 2) otherwise force-align the audio to the passage text → per-word [{t0,t1}]
  await access(audioIn);
  const text = lines.join(' ');
  const timed = await forcedAlign({ audioIn, text, aligner });   // [{word,t0,t1}, ...]
  return { audioPath: audioIn, marks: attachLineIndex(lines, timed) };
}
