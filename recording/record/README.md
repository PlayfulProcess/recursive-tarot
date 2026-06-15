# record/ — the Chrome recording stack

Drive **Chrome with Playwright** to turn a performance (a karaoke reading, a screencast) into a
**video + a sequence grammar with exact timestamps**, orchestrating multiple tools (TTS,
forced-alignment, ffmpeg) behind one command.

## The one thing the architecture is built around
**Web Speech (`speechSynthesis`) audio is NOT recordable** — it's produced at the OS layer, not
in the page, so no MediaRecorder/tab-capture/ffmpeg can grab it. (It's great for the *live*
read-along in `../karaoke/alice-karaoke.html`, but not for a file.)

So for **recording** we use **audio that exists as a file**, plus **word timestamps**:
- **You already have a better audiobook** → `tts/provided.mjs`: take that audio + the text,
  get word timestamps via **forced alignment** (`align/forced-align.mjs`, WhisperX/aeneas) — or
  accept marks you supply. *(This is the primary path for your case.)*
- **No audio yet** → a cloud TTS that returns audio + marks: `tts/elevenlabs.mjs`
  (with-timestamps), `tts/google.mjs` (SSML `<mark>` timepoints), `tts/azure.mjs` (WordBoundary).

## Pipeline (`orchestrate.mjs`)
```
source (passages / grammar + audiobook)
  → TTS adapter            → { audioPath, wordMarks:[{word,line,passage,t0,t1}] }   (or align existing audio)
  → manifest.json          (passages + audio + marks + image_url/svg)
  → player/perform.html    renders the karaoke timeline driven BY THE MARKS (deterministic clock)
  → recorder.mjs           Playwright opens Chrome (fullscreen/1080p), plays the timeline, records video (webm)
  → ffmpeg                 mux the recorded video with the concatenated audio → final.mp4
  → grammar.json           sequence+performance grammar with REAL timestamps + media url
```
Visuals and audio align *by construction*: the page is driven by the same word marks that came
from (or were aligned to) the audio, and ffmpeg muxes that exact audio in. No reliance on
capturing page audio.

## Tools it orchestrates
| Tool | Role | Where |
|---|---|---|
| **Playwright + Chromium** | open Chrome (headful/fullscreen or headless 1080p), drive the page, record video | `recorder.mjs` |
| **TTS adapter** | text → audio + word marks (or wrap your audiobook) | `tts/*.mjs` |
| **Forced alignment** | existing audio + text → word timestamps | `align/forced-align.mjs` |
| **ffmpeg** | mux/concat audio+video, encode MP4 | `orchestrate.mjs` (via `ffmpeg-static`) |
| **perform.html** | the recordable player — marks-driven karaoke; exposes `window.__ready/__done` | `../player/perform.html` |

## Setup (runs on a machine with network + a display or Xvfb)
```bash
cd record
npm install                 # playwright, ffmpeg-static, (optional) tts SDKs
npx playwright install chromium
cp config.example.json config.json     # pick tts engine, voice, resolution, fps, paths
node orchestrate.mjs ../productions/alice-in-wonderland   # → out/alice.mp4 + grammar.json
```
> Can't run in the build sandbox (no npm/Chromium/network here) — this is a real, runnable
> scaffold. `recorder.mjs` works standalone against any `perform.html?manifest=…`.

## Recording knobs (`config.json`)
- `headless` (true for CI; false + `fullscreen` for a real Chrome window),
- `viewport` (1920×1080 default), `fps`, `tts.engine`, `tts.voice`, `paths.out`.

## Disclosure
AI-narrated readings / AI-performed screencasts are labelled as such in the grammar metadata.
