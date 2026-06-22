# Use case — Clone & illustrate a deck through the recursive.eco MCP

*How a brand-new, fully-illustrated tarot got built end to end — by reading one deck's
text, transplanting it into a new deck, and attaching another deck's art — using nothing
but the recursive.eco MCP. Plus the one bug we had to fix in the platform to make it
possible, and three honest gotchas for the course.*

> Companion to [`build-ontoject-via-mcp.md`](./build-ontoject-via-mcp.md), which built the
> *Elemental_Play* layer. This one is the **whole-deck clone**: create → fill text → attach
> images → cast → verify.

## The brief

> "I have two decks. One ('**The Ontoject: A Tarot of Playful Process**') has all the finished
> writing — Reflection, Poetic_Entry, Elemental_Play, Facet, Existential_Entry,
> Visual_Contemplation. The other ('**Playful Process: The Path of the Ontoject**') has the
> R2 card images. Make me a **third** deck, *The Ontoject — Illustrated*, that marries the two
> — entirely through the MCP, the way any user who just cloned recursive-tarot would."

## The toolbox (8 MCP tools)

`list_grammars` · `get_grammar` · `create_grammar` · `add_item` · `update_item` ·
`set_item_image` · `delete_item` · `cast`. No SQL, no R2 keys, no GitHub.

## The build, step by step

1. **Find the sources.** `list_grammars("Path of the Ontoject")` →
   `list_grammars("ontoject")`. (Note: what looked like an "account id" was actually the
   **grammar id** `a4938271…`.) Four "Path of the Ontoject" copies exist; the live one with
   images is `a4938271…`; the finished-text deck is `fe8ceb69…`.
2. **Read the text deck in full.** `get_grammar(fe8ceb69…)` → 24 cards, each with its complete
   sections. (This is the step the bug below blocked — see "The fix.")
3. **Create the target.** `create_grammar("The Ontoject — Illustrated", type=tarot)` →
   new id **`e8c4ca59-7841-4b5d-ad56-584ff52c859d`**.
4. **Transplant the text.** 24 × `add_item` — name + keywords + the full `sections` map in a
   single call each (add_item takes sections inline, so no separate update needed). Run in
   parallel batches of ~6.
5. **Attach the art.** 22 × `set_item_image`, passing each source card's existing R2
   `image_url`. The platform reports `already_on_cdn` (the URLs were already on recursive.eco's
   CDN) and links them onto the new cards.
6. **Cast & verify.** `cast(count=3)` rendered a live reading; `get_grammar` confirmed all 24
   cards carry full sections and 22 carry images.

## The fix — get_grammar wasn't returning section text

This use case was **impossible on day one**: `get_grammar` returned each item's
`section_labels` (just the keys) but **not the section text**, and there was no MCP `get_item`.
So you literally could not read a deck's writing back through the MCP — which means you could
not clone or transplant a deck with the MCP alone.

One-line fix in `recursive-eco` (`GET /api/gpt/grammars/[id]`): return the full `sections`
map alongside `section_labels` (kept for back-compat). Shipped as round 136; verify live by
calling `get_grammar` and confirming `sections` text is present. **Lesson for the course:** if
you're cloning/refracting an existing deck and `get_grammar` only shows you labels, your
platform is on an old build — the read has to return `sections`.

## Three honest gotchas (good teaching moments)

1. **A transient `add_item` failure mid-batch reorders your deck.** One call in a parallel
   batch returned "server isn't responding"; the *next* card took the missing slot, so the
   sequence skipped. There is **no `sort_order` / reorder tool** in the MCP. The only clean fix
   is `delete_item` the mis-numbered card and re-`add_item` in order (new items always append).
   Takeaway: for order-sensitive decks, add sequentially, or verify numbers after each batch.
2. **You can't control section display order.** Whatever key order you send, it comes back
   `Facet, Reflection, Poetic_Entry, Elemental_Play, Existential_Entry, Visual_Contemplation`
   — because Postgres `jsonb` normalizes object keys **by length, then alphabetically**. It's
   consistent and matches the source deck exactly; just don't promise authors a custom order.
3. **Image coverage is only as good as the source roster.** The text deck (24 cards: adds *The
   Void Birthing Light* and *The Star*, drops the imaged deck's junk + *Hubris*) doesn't map
   1:1 to the imaged deck. Result: **22/24 imaged**; 2 cards (*The Void Birthing Light*,
   *Temperance*) had no source art and are left imageless; *The Star* reuses the imaged deck's
   "guiding star" card as a deliberate, noted substitute. Honest gaps beat silent mismatches.

## What it cost to follow

| Thing | Cost |
|---|---|
| recursive.eco account | **Free** |
| The 8 MCP tools (read, create, add, image, cast) | **Free** — it's your own data |
| MCP calls for this build | ~**55**: 4 reads + 1 create + 26 add/delete (24 + 1 re-add + 1 delete) + 22 set_image + 1 cast + 1 verify |
| The AI driving the MCP | a **Claude plan** you already have |
| Image hosting | **$0 extra** — source URLs were already on the CDN (`already_on_cdn`) |
| The platform fix (one-time) | one ~1-line code change + a Vercel build |

## Result

- **Grammar:** *The Ontoject — Illustrated* — `e8c4ca59-7841-4b5d-ad56-584ff52c859d` (tarot, 24 cards)
- **Cast** (Q: *"How do I build by describing it, start to finish, through the MCP?"*):
  **Past — Strength**, **Present — The Spiral**, **Future — The Trickster (reversed)**.
  Read playfully: you already have the *courage to begin* (Strength); the work *spirals* —
  same moves, deeper each pass (The Spiral); and the reversed Trickster warns against losing
  the *play* — don't let the build turn into grim toil. Fitting, given the deck's whole thesis.

---
*Built live against the recursive.eco MCP (`dev.flow.recursive.eco/api/mcp`). Source text:
"The Ontoject: A Tarot of Playful Process"; imagery from "Playful Process: The Path of the
Ontoject." More from the author at [playfulprocess.com](https://www.playfulprocess.com/).*
