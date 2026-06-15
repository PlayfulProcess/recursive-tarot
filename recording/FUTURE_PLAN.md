# recursive-recording — future plan

## Vision
One pipeline, many sources → **narrated, illustrated performances** that live as data in
recursive.eco. A kids' book, a course, a tarot reading, a poem — all become the same
`sequence`+`performance` shape and play through one viewer. The recording is a *projection* of
the source, the way the tarot meta-grammar is a projection of the decks.

## Unblock checklist (to move off the local scaffold)
- [ ] **Re-authorize GitHub MCP** → `create_repository("recursive-recording")`, push this repo.
- [ ] **Add `recursive-recording`, `kids-book-club`, `recursive-eco` to the session scope.**
- [ ] **A session with outbound network** → vision on existing illustrations + source fetch.
- [ ] **recursive-eco MCP approved + image-gen credits** (`generate_item_image` ≈ $0.15/img).
- [ ] **Pick the voice**: AI TTS (fits "built with Claude") vs. you / your daughter.

## Roadmap
**M1 — Alice pilot, end to end (highest value).**
1. `ingest.py`: pull Alice text + current illustrations from `kids-book-club`.
2. Run `illustration_qa.py`, then the vision loop on every passage — reorder, and regenerate the
   wrong ones (start with the little-door fix). Record verdicts in `illustration-map.json`.
3. Real audio: TTS each passage (or record), measure true clip boundaries, replace the estimated
   timings in `assemble_performance.py`’s output.
4. Publish the `sequence` grammar to recursive.eco (MCP `create_grammar` + `add_items`); confirm
   it plays in the performance viewer.

**M2 — Vibe Coding 101 screencast.**
1. `narration_script.py` on the real recursive-eco course → shooting script.
2. Record: Claude Code performs the steps live while the terminal captures (asciinema/OBS).
3. Voice-over from the script; cut into per-scene clips; assemble the sequence grammar.

**M3 — Make it a real pipeline.**
- `ingest.py` adapters per source type (epub/MDX/grammar).
- Karaoke timing from the actual TTS audio (word timestamps) instead of estimates.
- A tiny `productions/` index + a `_collection.json` so recordings list in the app.
- Optional: render a standalone MP4 from the sequence grammar (headless browser + ffmpeg) for
  YouTube, while the grammar stays the source of truth.

**M4 — Self-serve.** Any user points the pipeline at a public-domain book → gets a karaoke
reading. The illustration-QA loop becomes a reusable "fix my book's pictures" tool.

## Open questions
- Karaoke word-sync: best cross-browser source of word timestamps (Web Speech `boundary` is
  uneven; cloud TTS gives real marks but costs/needs network).
- Where recordings live: their own repo (here) vs. inside each source repo.
- Disclosure UX for AI voice / AI-performed screencasts.
