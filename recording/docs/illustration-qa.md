# Illustration QA — the vision loop

Goal: the picture on screen actually matches the words, and is good. Driven by
`pipeline/illustration_qa.py`, which emits a worksheet (`productions/<book>/illustration-map.json`).

## The loop, per passage
1. **SEE** — download `illustration.image_url` locally and look at it (agent vision). *Needs
   outbound network.*
2. **MATCH** — does it depict THIS passage? Set `depicts_passage`.
3. **ORDER** — if it belongs to another passage, set `reorder_to` (free: just re-points the url).
4. **CRITIQUE** — record problems. The script pre-flags **size cues the picture must honor**
   ("tiny", "fifteen inches", "nine feet", "huge", "grew"…), because size is what storybook
   art most often gets wrong.
5. **DECIDE** — `action`: keep · reorder · regenerate.
6. **APPLY** — regenerate via recursive-eco MCP `generate_item_image(grammar_id, item_id,
   prompt)`; set the returned URL as `image_url`; **re-SEE** to confirm it fixed the issue. Keep
   the original (`*_original`); log the reason.

## The worked example (the door)
Passage *The Little Door*: text says the door is **"fifteen inches high"** and Alice is far too
big. The original plate drew the **door huge** — a size-cue violation. Fix → `action: regenerate`
with a prompt that pins the sizes:

> "A GIANT young girl in a blue dress kneeling to peer through a TINY door only about fifteen
> inches high; the little door is unmistakably MUCH smaller than her head; through the small
> doorway a bright garden; the door must look tiny and the girl must look huge." (1024×1536)

Then re-view: is the door now clearly tiny and Alice clearly huge? If yes, accept; if not, retry
with a stronger size instruction.

## Why a script can't finish it alone
Steps 2–4 require *seeing* the image. The script structures the worksheet, detects the size cues
to check, and stages the regenerate prompts; the agent (or a person) supplies the eyes and the
verdict. That division keeps it honest — no picture is declared "fixed" without being looked at.
