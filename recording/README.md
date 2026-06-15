# recursive-recording

A production pipeline that turns a **source** — a course, a kids' book, a deck — into a
**narrated, illustrated "performance"** that plays inside [recursive.eco](https://recursive.eco),
and (for screencasts) into a recorded walkthrough.

The output is **data, not a video file**: a `sequence` grammar whose items each carry a
`performance` object (timed clip + image + text overlays + audio). The app is the player.

> Status: **local scaffold + a working Alice karaoke demo** (Jun 2026). Created locally because
> the GitHub token was expired in the session that built it; ready to push as
> `playfulprocess/recursive-recording`. See `FUTURE_PLAN.md` for the roadmap and the unblock list.

## Try the demo now (no build, no network)
Open **`karaoke/alice-karaoke.html`** in a browser. It reads Alice's *Down the Rabbit-Hole*
aloud using the browser's own speech synthesis, **karaoke-style: ALL-CAPS, one line at a time,
the current word lit up** as it's spoken. Space = play/pause, ←/→ = turn pages. If your browser
has no voices it still works as a timed read-along. Pictures are simple offline SVG plates;
the real illustrations come from the illustration step (below).

## The two pilots
- **Vibe Coding 101** (from `recursive-eco`) — a screencast: Claude Code actually doing the
  steps while the terminal records, with voice-over. `pipeline/narration_script.py` turns the
  course MDX into a beat-by-beat shooting script (see `productions/vibe-coding-101/`).
- **Alice in Wonderland** (from `kids-book-club`) — the karaoke ALL-CAPS reading above, after an
  **illustration-improvement pre-pass** (`pipeline/illustration_qa.py`): see each picture, match
  it to its passage, reorder the out-of-order ones, and **regenerate the wrong ones** (the
  worked example: the *little door* passage where the door was drawn huge — fixed so the door is
  tiny and Alice is enormous).

## Layout
```
karaoke/
  alice-passages.json     # canonical content: PD text → short ALL-CAPS lines + illustration prompts
  alice-passages.js       # generated wrapper so the HTML loads under file:// (build_karaoke.py)
  alice-karaoke.html      # the working reader (Web Speech API karaoke; self-contained)
pipeline/
  build_karaoke.py        # prose → ALL-CAPS kid-length lines; regenerates alice-passages.js
  illustration_qa.py      # vision worksheet: see → match → reorder → regenerate (size-cue checks)
  assemble_performance.py # passages → recursive.eco `sequence`+`performance` grammar (karaoke timings)
  narration_script.py     # course MDX → screencast shooting script
  sample/vibe-coding-101.mdx
productions/
  alice-in-wonderland/    # grammar.json (the sequence grammar) + illustration-map worksheet
  vibe-coding-101/        # screencast-script.md
docs/                     # karaoke-format · illustration-qa · performance-grammar
```

## Run it
```bash
python3 pipeline/build_karaoke.py --demo          # regenerate JS data + show line-splitting
python3 pipeline/assemble_performance.py          # build the Alice sequence grammar
python3 pipeline/illustration_qa.py               # build the illustration QA worksheet
python3 pipeline/narration_script.py              # build the Vibe Coding 101 screencast script
```

## What still needs a real environment
- **Vision on existing illustrations** (download + look) needs outbound network.
- **Image (re)generation** uses the recursive-eco MCP `generate_item_image` (server-side, costs
  credits) — set the returned URL as `illustration.image_url`.
- **Recording** (screen + voice): a screen recorder (asciinema/OBS) + TTS (browser speech, or
  ElevenLabs), or your own voice. The pipeline produces everything up to the camera.

Public-domain sources only; every regenerated/reordered image is logged with its reason and
the original kept. AI narration / AI-performed screencasts should be disclosed as such.
