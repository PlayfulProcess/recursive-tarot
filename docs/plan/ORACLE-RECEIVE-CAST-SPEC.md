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
| `flow.recursive.eco/cast?d=<base64url cast>` | "here is a spread I already cast — interpret it" | **partially built** (see update) |

> **UPDATE (Jul 2 2026):** the app already has a receiver at **`/cast?d=`**
> (`apps/flow/src/app/cast/page.tsx`): it decodes the payload, renders the card grid
> with position labels + reversal rotation, lazy-fetches Scene/Symbol from the repo's
> raw grammar.json, and offers "Save deck to library". The Spread Caster now targets
> `/cast?d=` (was `/?d=`, which the home page ignores). Still missing on the app side:
> the AI oracle reading over the actual payload (`/api/ai/cast-reading` exists but
> hardcodes the 3-card Structures/Process/Possibilities spread — it must read
> `question` + `positions[]` + `cards[]` from the cast) and journal-saving the cast +
> interpretation. Everything below remains the contract for that work.

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
