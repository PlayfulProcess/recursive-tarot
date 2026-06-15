// tts/elevenlabs.mjs — synthesize audio AND get character/word timestamps in one call.
// Uses the ElevenLabs "with-timestamps" endpoint. Needs ELEVENLABS_API_KEY (env, never commit).
// Returns { audioPath, marks:[{word,line,wi,t0,t1}] }.
import { writeFile } from 'node:fs/promises';
import { attachLineIndex } from './index.mjs';

const API = 'https://api.elevenlabs.io/v1/text-to-speech';

export async function synthesizeElevenLabs({ lines, voice = 'Rachel', voiceId, outPath }) {
  const key = process.env.ELEVENLABS_API_KEY;
  if (!key) throw new Error('set ELEVENLABS_API_KEY to use the elevenlabs adapter');
  const id = voiceId || voice;     // pass a real voice_id in config for production
  const text = lines.join(' ');

  const res = await fetch(`${API}/${id}/with-timestamps`, {
    method: 'POST',
    headers: { 'xi-api-key': key, 'content-type': 'application/json' },
    body: JSON.stringify({ text, model_id: 'eleven_multilingual_v2' }),
  });
  if (!res.ok) throw new Error(`elevenlabs ${res.status}: ${await res.text()}`);
  const j = await res.json();      // { audio_base64, alignment:{characters,character_start_times_seconds,...} }

  await writeFile(outPath, Buffer.from(j.audio_base64, 'base64'));

  // collapse character alignment → word [{word,t0,t1}]
  const a = j.alignment || j.normalized_alignment;
  const timed = charsToWords(a.characters, a.character_start_times_seconds, a.character_end_times_seconds);
  return { audioPath: outPath, marks: attachLineIndex(lines, timed) };
}

function charsToWords(chars, starts, ends) {
  const words = []; let cur = '', t0 = null, t1 = 0;
  for (let i = 0; i < chars.length; i++) {
    const c = chars[i];
    if (/\s/.test(c)) { if (cur) { words.push({ word: cur, t0, t1 }); cur = ''; t0 = null; } }
    else { if (t0 === null) t0 = starts[i]; t1 = ends[i]; cur += c; }
  }
  if (cur) words.push({ word: cur, t0, t1 });
  return words;
}
