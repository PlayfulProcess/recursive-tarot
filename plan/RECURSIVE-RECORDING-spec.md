# recursive-recording — pipeline spec (blueprint for the new repo)

*Written 2026-06-15 by the Opus session. Lives here in recursive-tarot/plan ONLY because
the GitHub token was expired this session and the container is ephemeral — this is the
**durable home until `playfulprocess/recursive-recording` exists**, then it moves there as
`README.md` + `/docs`. Nothing here depends on tarot; it's a sibling project.*

## 0. Why this session couldn't create it (the unblock list)
- [ ] **Re-authorize GitHub MCP** (token expired) → lets me `create_repository` and read the
  source repos `playfulprocess/kids-book-club` and `playfulprocess/recursive-eco`.
- [ ] **Add `recursive-recording`, `kids-book-club`, `recursive-eco` to the session repo scope**
  (this session was scoped to `recursive-tarot` only).
- [ ] **Enable outbound network** (was HTTP 403) → required for **vision on existing
  illustrations** (download the image bytes so I can SEE them) and for fetching source text.
- [ ] **Confirm recursive-eco MCP approval + image-gen credits** (`generate_item_image` ≈ $0.15/img,
  3× markup; 429 if low). These run server-side, so they work even with the network block —
  but each call needs your approval.
- [ ] **Decide the voice**: AI TTS (fits the "built with Claude" story) vs. you/your daughter
  (warmer). This shapes production.

## 1. What this repo is
A **production pipeline** that turns a source (a course, a kids' book, a deck) into a
**narrated, illustrated "performance"** that renders inside recursive.eco — and, where the
source is a screencast, into a recorded walkthrough. Output is a **`sequence` grammar with
per-step `performance` objects** (timestamped clips + image/text overlays + background audio)
— a format recursive.eco already supports (see recursive-tarot `GRAMMAR_FORMAT.md`
"Performance object"). So the pipeline's deliverable is **data**, not a video file: the app is
the player.

Two pilots:
- **A. Vibe Coding 101** (from `recursive-eco`) — a screencast: Claude Code actually doing the
  steps, with voice-over.
- **B. Alice in Wonderland** (from `kids-book-club`) — a **karaoke-style ALL-CAPS** narrated
  reading, after an **illustration-improvement pre-pass** (vision → reorder → regenerate).

## 2. Repo structure
```
recursive-recording/
  README.md                      # = this spec
  docs/
    karaoke-format.md            # the ALL-CAPS timed-highlight reading spec (§5)
    illustration-qa.md           # the vision→reorder→regenerate workflow (§6)
    performance-grammar.md       # how a reading/screencast maps to a sequence+performance grammar
  pipeline/
    ingest.py                    # pull source text+images (from kids-book-club / recursive-eco)
    illustration_qa.py           # vision audit → match/reorder/flag-for-regen report (JSON)
    regenerate_images.py         # calls recursive-eco generate_item_image with corrected prompts
    build_karaoke.py             # text → ALL-CAPS timed segments → sequence grammar JSON
    narration_script.py          # text → narration script (TTS-ready, SSML optional)
    assemble_performance.py      # stitch segments+images+audio timings into the grammar
  productions/
    vibe-coding-101/             # screencast script, take notes, output grammar id
    alice-in-wonderland/         # per-passage segments, illustration map, regen log, grammar id
```

## 3. The performance/sequence output (the contract)
One reading = one `grammar_type: "sequence"` grammar, `default_preview: "performance"` semantics.
Each **item = one passage/step**, carrying:
- `sections`: `{ "Text": "<the prose>", "Narration": "<what the voice says>" }`
- `image_url`: the (possibly regenerated) illustration for this passage
- `performance`: `{ start_sec, end_sec, video_visible, volume, background_audio?, overlays[] }`
  - For **karaoke**: `overlays[]` carry the ALL-CAPS text with per-word/`per-line` timing so the
    current line highlights as the voice reads it (text overlay, `start_sec`/`end_sec` per line).
  - For **screencast**: the clip is the terminal recording; overlays caption the step.
- `metadata`: `{ passage_index, source, illustration_status: original|reordered|regenerated }`

## 4. Pilot A — Vibe Coding 101 (screencast)
1. `ingest.py` pulls the Vibe Coding 101 course text/steps from `recursive-eco`.
2. `narration_script.py` produces a **beat-by-beat screencast script**: each step = (terminal
   command(s) to run, what's on screen, the voice-over line, target duration).
3. **Recording** (the part needing a recorder, not me): run the steps in a real Claude Code
   session while `asciinema`/OBS captures the terminal; Claude Code genuinely performing the
   course is the most authentic demo. (I can DRIVE the steps; I can't be the camera.)
4. **Voice**: TTS reads the script (ElevenLabs/OS), or you record it.
5. `assemble_performance.py` cuts the recording into per-step clips and emits the sequence grammar
   (timestamps from the script beats), which plays in recursive.eco next to the written course.

## 5. Pilot B — Alice, karaoke ALL-CAPS (your daughter's format)
**Karaoke spec (`docs/karaoke-format.md`):** every passage is rendered in **ALL CAPS**, large,
high-contrast; the **current line highlights** in sync with the voice (timed text overlays);
short lines (≤~7 words) so a young reader can track. One illustration per passage, full-bleed
behind/above the text. Gentle background music at low volume (`background_audio`).

**Flow:**
1. `ingest.py` pulls Alice text + its current illustrations from `kids-book-club`.
2. **Illustration QA pre-pass** (§6) — the heart of pilot B.
3. `build_karaoke.py` splits the (ALL-CAPS) text into kid-length lines with timing.
4. `narration_script.py` → narration (slow, warm, kid-paced).
5. `assemble_performance.py` → the sequence grammar; TTS or recorded voice supplies audio.

## 6. Illustration QA workflow (`docs/illustration-qa.md`) — the vision loop
Goal: the picture on screen actually matches the words, and is good. Per passage:
1. **See it.** Download the current illustration locally and view it (vision). *(Needs network —
   blocked this session.)*
2. **Match.** Does the image depict THIS passage? Build/repair the passage→image map; **reorder**
   images that are out of sequence (free; just re-points `image_url`).
3. **Critique.** Flag mismatches/quality issues. **Worked example (your note):** the passage
   where *Alice looks through a very small door into the garden* — the current image draws the
   **door huge**, contradicting "small door." That's a flagged **regenerate**.
4. **Regenerate** the flagged ones via `regenerate_images.py` → recursive-eco
   `generate_item_image` with a corrected prompt, e.g.:
   > "A storybook illustration: a giant Alice kneeling to peer through a **tiny door, about
   > fifteen inches high**, set in the wall; through the little doorway a bright garden of
   > flowers and fountains; warm, classic children's-book watercolor; the door is clearly
   > MUCH smaller than Alice." (size 1024x1536)
   Keep the original as `*_original` in the regen log; never silently discard.
5. **Re-view** the regenerated image to confirm it fixed the issue (vision again); accept or retry.
6. Record every decision in `productions/alice-in-wonderland/illustration-map.json`
   (`passage, original_url, action: keep|reorder|regenerate, new_url, reason`).

## 7. Honesty / guardrails (same spirit as recursive-tarot)
- Public-domain sources only (Alice text/illustrations are PD; confirm the specific scans).
- Log every regenerated/reordered image with its reason; keep originals.
- The voice and the "Claude does the course on camera" framing should be disclosed (AI-narrated /
  AI-performed), not passed off as human unless you record it.

## 8. First concrete actions once unblocked (in order)
1. Re-auth GitHub → `create_repository("recursive-recording")`, push this spec as README + /docs.
2. Read `kids-book-club` Alice content → `ingest.py` → list passages + current illustrations.
3. Run the **Alice illustration QA** vision loop on 3–5 passages (incl. the tiny-door fix) as a
   visible proof; regenerate via recursive-eco MCP; assemble a 5-passage karaoke demo grammar.
4. In parallel, draft the Vibe Coding 101 screencast script from the recursive-eco course.
