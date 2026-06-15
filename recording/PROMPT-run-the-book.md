# PROMPT — run the Alice book through recursive-recording

*Paste this into a fresh session that has: GitHub MCP re-authorized, network ON, the
recursive-eco MCP approved with image-gen credits, and these repos in scope —
`playfulprocess/recursive-recording`, `playfulprocess/kids-book-club`,
`playfulprocess/recursive-eco`. (If a repo isn't in scope, `list_repos` then `add_repo`.)*

---

You are working in the **recursive-recording** repo (the Chrome/Playwright recording stack +
the karaoke pipeline; read its `README.md` and `record/README.md` first). Do these three things
for **Alice's Adventures in Wonderland**, committing as you go.

## 1) Copy the kids-club book into recursive-recording (internally)
The source book is `playfulprocess/kids-book-club` and the live build is
`audiobooks.recursive.eco/books/alice-in-wonderland/booklets/book.html`.
- Use `mcp__github__get_file_contents` to read the Alice text + its illustration manifest/assets
  from `kids-book-club` (find the per-page text and each image's URL + provenance/caption — the
  captions record the generator, e.g. "DALL-E 3 (Rackham style)").
- Land a self-contained copy under `productions/alice-in-wonderland/source/` (page text, image
  URLs, and any existing per-page audio). Do **not** modify the upstream repo.
- Normalize it into `karaoke/alice-passages.json` shape (passages = pages; `lines` = the page
  text split into short ALL-CAPS lines via `pipeline/build_karaoke.py:allcaps_lines`; each
  `illustration` carries `image_url`, `prompt`/caption, and **`provenance`** — set `"ai"` when
  the caption names DALL-E/Midjourney/etc., else `"public-domain"`/`"human"`). Then
  `python3 pipeline/build_karaoke.py` to regenerate the reader data.

## 2) Vision QA — reorder, and REMAKE only AI illustrations (the door is the case)
Run `python3 pipeline/illustration_qa.py` to get
`productions/alice-in-wonderland/illustration-map.json`. For each passage:
1. **SEE** — download `current_image_url` to a temp file and view it with the Read tool (vision).
2. **MATCH / ORDER** — does it depict this page? If it belongs to another page, set `reorder_to`
   and just re-point `image_url` (free, allowed for any provenance).
3. **PROVENANCE GATE** — only `eligible_for_remake: true` (provenance == `ai`) images may be
   **regenerated**. Public-domain / human art (e.g. original Tenniel) may be reordered, **never
   remade**. The worksheet already enforces this.
4. **REMAKE via recursive.eco MCP** — for AI images that are wrong, regenerate **in recursive.eco
   so the output improves there**:
   - `mcp__recursive-eco__list_grammars` → find the Alice grammar; `get_grammar` → the page's item id.
   - `mcp__recursive-eco__generate_item_image(grammar_id, item_id, prompt=<corrected, size-pinned prompt>)`,
     or `set_item_image` to assign a chosen result.
   - **The door page** (text: "a small passage, not much larger than a rat-hole… could not even
     get her head through the doorway"): the current DALL-E plate draws the door full-height —
     wrong. Regenerate with a prompt that pins the scale, e.g.:
     > "Arthur-Rackham-style watercolor, soft and classic: a young girl in a blue dress kneeling
     > on a checkered hall floor, bending right down to peer through a TINY door only about the
     > size of a rat-hole, low in the wall — the little door is unmistakably far too small for her
     > to fit even her head; through the small opening glimpse a bright sunlit garden of roses and
     > a fountain; the door MUST look tiny and Alice MUST look much too big; warm, gentle, Alice
     > looking a little more like the classic Alice." (portrait, 1024×1536)
5. **RE-SEE** the regenerated image (vision) to confirm the door now reads as tiny and Alice too
   big. Accept or retry with a stronger scale instruction. Record verdicts (`seen`,
   `depicts_passage`, `problems`, `action`, `new_url`, `reverified`) back into the worksheet;
   keep each original URL; log every reorder/remake with its reason.

## 3) Record the whole book
- **Audio:** there is a *better audiobook* — put per-page audio at
  `productions/alice-in-wonderland/audio/<passage-id>.(wav|mp3)` and keep
  `record/config.json` → `tts.engine:"provided"` (word timestamps come from forced alignment,
  `tts.align:"whisperx"`). No existing audio for a page? switch that run to a cloud TTS adapter.
- `python3 pipeline/assemble_performance.py` (refresh the grammar from the corrected passages),
  then **`cd record && npm install && npx playwright install chromium && node orchestrate.mjs
  ../productions/alice-in-wonderland`** → `record/out/final.mp4` + `grammar.json` rewritten with
  REAL per-line timestamps. Use `record/config.json` `fullscreen:true` for a real Chrome window
  or `headless:true` (1920×1080) for deterministic CI output.
- **Publish:** push the regenerated images/grammar; if the book should live as a recursive.eco
  grammar, `create_grammar(grammar_type:"sequence")` + `add_items(...)`, then confirm it plays in
  the performance viewer.

## Guardrails
Public-domain text only; **never remake non-AI art** (gate enforces it); keep originals and log
every change; label AI narration / AI illustrations in metadata. Commit + push to the
recursive-recording branch as you complete each numbered task.
