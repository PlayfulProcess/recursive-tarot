# Oracle Receive-a-Cast — spec + plan

**Status:** PLAN ONLY. Nothing in the recursive.eco (flow) repo is changed by this doc.
This is the contract the tarot repo already emits, and what the app would need to
build to receive it. Written Jul 1 2026.

## The problem

The Caster and the Spread Studio (`viewers/caster.html`, `viewers/caster-studio.html`)
already **build a spread, draw cards into it, and hand the whole reading to
recursive.eco** — the "Send to recursive.eco oracle" button. But nothing on the
flow side reads the payload yet, so today the link just opens the app's home. The
send is "wired but unreceived."

Two distinct hand-offs exist; keep them separate:

| Link | Meaning | Status |
|---|---|---|
| `flow.recursive.eco/play?id=<grammar-uuid>` | "open this deck, let me cast fresh in the app" | works (deck loads) |
| `flow.recursive.eco/?d=<base64url cast>` | "here is a spread I already cast — interpret it" | **needs building** |

This doc is about the second one.

## What the tarot side sends (the contract)

`syncJson()` builds a cast object and appends it to the link as
`?d=<base64url>` where the payload is
`btoa(unescape(encodeURIComponent(JSON.stringify(cast))))` with `+/=` → `-_` and
stripped padding (URL-safe base64). Decode with the inverse. Shape (`_version: 2`):

```jsonc
{
  "_type": "recursive-tarot-cast",
  "_version": 2,
  "_source": "https://tarot.recursive.eco/viewers/caster-studio.html",
  "spread": "Structures · Process · Possibilities",   // human name
  "spread_id": "spp",                                  // preset id, or "custom"
  "deck": "All Decks (cross-deck)",                    // human label
  "cast_at": "2026-07-01T02:00:00.000Z",
  "question": "What is this situation made of?",       // or null
  "positions": [                                        // the spread layout
    { "n": 1, "label": "Structures", "meaning": "What's already built…", "x": 0.22, "y": 0.5 }
  ],
  "axes": {                                             // OPTIONAL (added Jul 2026) — omitted entirely when unused
    "cols": [ { "label": "Structures", "meaning": "what is built" } ],
    "rows": [ { "label": "Perceived",  "meaning": "" } ]
  },
  "cards": [                                            // one per position, in order
    {
      "position": "Structures",
      "prompt": "What's already built…",
      "name": "The Tower",
      "deck": "Tarot de Marseille (Conver)",
      "arcana": "major",
      "number": 16,
      "reversed": false,
      "image_url": "https://pub-…r2.dev/grammar-illustrations/…jpg",
      "source_deck": "tarot-de-marseille-conver",       // repo slug
      "source_item_id": "major-16-la-maison-dieu"        // item id within that grammar
    }
  ]
}
```

`positions[i]` and `cards[i]` are index-aligned. Every card carries
`source_deck` + `source_item_id`, so the app can resolve it to a real grammar item
(via `tarot/_eco_ids.json`: slug → grammar UUID) for provenance and deep-links.

## What flow would need to build (the oracle receiver)

A route/handler (call it the **cast receiver**) that:

1. **Reads `?d=`**, URL-safe-base64-decodes to the cast JSON, and validates
   `_type === "recursive-tarot-cast"` + `_version`. Fail soft to the home if absent.
2. **Resolves cards** — for each `cards[i]`, map `source_deck` → grammar UUID
   (`_eco_ids`) and `source_item_id` → the item, to attach provenance / Oracle-card
   rendering. Fall back to `image_url` + `name` if the grammar isn't imported.
3. **Renders the spread** — lay the `positions` out by their `x/y` fractions (same
   board the tarot Caster draws), each showing its drawn card, label, and prompt.
4. **Interprets with AI** — run the oracle over `{question, positions, cards}` using
   the reader's own wallet/credits (the same assistant the app already bills), voiced
   by the chosen orientation. This is the value the app adds over the static page.
5. **Journals it** — persist the cast + interpretation as a Journal entry the reader
   can return to (Oracle cards with provenance).

Nothing above requires the tarot repo to change again — the payload is stable
(`_version` bump if the shape ever changes).

## Three ways to host it — pick one (design question, not decided here)

1. **Extend the existing tarot Caster/oracle in flow.** Smallest change: teach the
   current tarot reading flow to accept a pre-made cast via `?d=` in addition to
   casting fresh. Good if the app already has a tarot-cast renderer.

2. **A dedicated receiver route** (`/oracle/receive` or `/play?d=`). A thin,
   self-contained page that only does decode → render → interpret → journal. Cleanest
   separation; least risk to existing flows.

3. **A per-channel "caster app" (the bigger idea).** Generalise: every repo/channel
   registers its own **caster app** — a small renderer+interpreter that knows how to
   read *its* cast payload (tarot spreads, story beats, kids-story picks, an I-Ching
   throw). The channel system imports the repo's caster the way it already imports the
   repo's grammars. The `_type` field is the discriminator that routes a payload to
   the right caster. This is the "every repo can bring its own apps as casters" vision:
   - `recursive-tarot` → tarot spread caster (this payload)
   - `recursive-recording` / story repos → a **story caster**
   - `recursive-kids-stories-club` → a kids caster
   - I-Ching / astrology grammars → their own throw/chart casters

   Recommended end-state, but heaviest. A pragmatic path: build option 2 first
   (get tarot casts interpreting), then refactor it into the channel-app shape (3)
   once a second repo needs its own caster.

## Suggested next step

Implement **option 2** on flow (decode `?d=` → render → interpret with the reader's
wallet → journal), keeping the `_type`/`_version` discriminator so it can later become
the first entry in a channel-app registry (option 3). The tarot side is ready and will
not need changes.

---

## Appendix — the SPREAD contract (layout only) and its `axes` extension

Distinct from the cast payload above: a **spread** is the layout with no drawn cards.
It is the wire format shared by the flow assistant's `create_spread` tool, the
`?spread=<base64url>` handoff, the `eco-spread` postMessage, and the Studio's
Export/Import. Written and read in `viewers/caster-studio.html`
(`currentSpreadContract()` / `loadSpreadContract()`).

```jsonc
{
  "v": 1,
  "name": "Nature's Negotiation",          // REQUIRED — the spread's name, see below
  "description": "…",                       // optional, tolerated extra
  "positions": [
    { "label": "Held", "meaning": "What is already built here.", "x": 0.25, "y": 0.25 }
  ],
  "axes": {                                 // OPTIONAL — aggregate row/column headers
    "cols": [ { "label": "Structures", "meaning": "what is built" },
              { "label": "Process",    "meaning": "what moves" },
              { "label": "Possibilities" } ],
    "rows": [ { "label": "Perceived" }, { "label": "Self" }, { "label": "Perceiver" } ]
  }
}
```

**`name` is load-bearing.** The Studio shows it in a always-visible, editable *Spread
name* field and in the spread dropdown, and every downstream writer (export filename,
cast JSON `spread`, Contribute) reads it from there. A spread that arrives without a
name shows up as an anonymous "Custom", which is exactly the confusion this field was
added to end (Jul 2026).

### `axes` — declare a row/column meaning ONCE

For grid spreads, `axes` lets the *axis* carry the meaning so the position names can
stay short. A 3×3 "Structures/Process/Possibilities × Perceived/Self/Perceiver" needs
`axes.cols` + `axes.rows` and nine one-word position labels, instead of repeating both
axis names inside all nine position names.

- Entries may be plain strings (`["Structures","Process","Possibilities"]`) or objects
  `{ label, meaning? }`. The flat `col_labels` / `row_labels` arrays are accepted as
  aliases on read.
- Column headers render across the top of the board, row headers down the left. Their
  positions are derived by clustering the positions' own x (or y) values, so they line
  up with the actual grid; if the layout isn't a grid the headers space out evenly.
- **Backward compatible in both directions:** the key is omitted entirely when unused,
  and a spread without `axes` renders exactly as it always has.

### TODO on the flow side (not doable from this repo)

1. **`create_spread` should accept `axes`.** The tool schema
   (`lib/ai-pkg/capability-registry.ts`) currently takes only `name` + `positions[]
   {label, meaning}`. Adding an optional `axes: { rows[], cols[] }` (labels + optional
   meanings) would let the assistant build grid spreads the way a person describes
   them, and `spread-codec.ts` already tolerates unknown extras on the wire.
2. **There is no way for the assistant to edit a spread by name.** There is no
   `list_spreads` / `get_spread` / `update_spread` tool, the chat route never reads
   `preferences.spreads`, and the saved names are not in the system prompt — so
   "edit my Nature's Negotiation spread" makes the model call `create_spread` again and
   append a duplicate. The only name-keyed update path is the client-side
   `importSpread()` reached via `?importSpread=`.
