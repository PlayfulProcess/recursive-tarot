# Emergences — the cataloguing model

*One mechanism catalogues everything. This doc explains what an **emergence** is,
why it's the only cataloguing primitive in this repo, the contract it depends on,
and what it implies for [recursive.eco](https://recursive.eco).*

Siblings: [`GRAMMAR_FORMAT.md`](GRAMMAR_FORMAT.md) (the field shapes) ·
[`MULTI_LENS_PLAN.md`](MULTI_LENS_PLAN.md) (how an emergence chooses its *renderer*).

---

## 1. The idea in one sentence

An **emergence** is a node whose content is *a pattern over other nodes* — it lists
the members it groups (`composite_of`) and says what that grouping *is* — but it
holds **no leaf data of its own**. Cards are catalogued once, in their decks;
everything else (suits, ranks, eras, orders, "the tree") is an emergence over them.

## 2. One uniform node shape

There is no separate "card type" and "category type." Every item — a single card or
a whole axis — is the same shape:

```jsonc
{
  "id": "string",
  "name": "string",
  "sections": { "What it is": "…" },   // prose; on an emergence, what the pattern means
  "composite_of": ["id", "id", …],     // the members it groups — ABSENT on a leaf
  "category": "axis | rank | lineage | …",
  "render_as": "pill-group | …",       // optional rendering hint (see MULTI_LENS_PLAN)
  "metadata": { … }
}
```

A **leaf** (a card) is just a node with no `composite_of`. An **emergence** is a node
that has one. That's the whole type system. Because the shape is uniform:

- the same viewer, the same "Group by" selector, and the same filter logic work at
  **every depth**;
- emergences nest **recursively** with zero special-casing — cards → suits → decks →
  orders → the whole tree are all the same move applied again. (This is the literal
  meaning of *recursive*.eco.)

## 3. The source-of-truth contract (the part that makes it work)

> **A leaf's authoritative data lives in exactly one place — its deck
> (`tarot/<slug>/grammar.json`). Every emergence merely *references* leaves.
> A projection must never become a second source of truth.**

In this repo:

- **Decks** = the source of truth (a card's text, image, sourced claims, dating).
- **The meta-grammar** (`tarot/all-decks-many-lenses/grammar.json`) = a **generated
  projection** over the decks, rebuilt idempotently by
  [`scripts/build_meta_grammar.py`](scripts/build_meta_grammar.py). To correct a
  card, edit its **deck**; the meta re-derives on the next build. Never hand-edit the
  meta.

The catalogue axes are computed **structurally from real card metadata** — deck,
era, suit, rank, plus a hand-curated `order` (Dummett A/B/C) and `function`
(game/divination/esoteric) per deck. **No keyword-matching decides membership.**
(`keyword-emergence` nodes exist as a *lighter, optional* within-deck theming
mechanism; the meta builder explicitly skips them so they never leak into the
cross-deck structure.)

## 4. Generated vs. authored — same shape, different origin

- **Generated** emergences come from a rule ("group every card by its era"). Cheap,
  always consistent, can't drift. The meta axes are all generated.
- **Authored** emergences are hand-curated `composite_of` ("these twelve cards are a
  spread"). Flexible, manual.

Both are *the same node shape*. A generated view can be snapshotted into an authored
one (and then edited) — a natural promotion path.

## 5. Lenses — an emergence is self-describing

An emergence carries `render_as` / `lens`, so it declares **how it wants to be seen**
(pills, timeline, genealogy graph, tree). This is why the viewer's "Group by"
control needs no per-axis UI code: *the data drives the rendering.* See
[`MULTI_LENS_PLAN.md`](MULTI_LENS_PLAN.md).

## 6. Why this is the whole catalogue (implications)

- **No duplication, no drift.** A card exists once; fixing it fixes every view.
- **Cheap new lenses.** A new way to slice the collection is a new emergence node,
  not new schema or new UI. "By Order (A·B·C)" was just the `order` field grouped.
- **Composability.** Emergences over emergences give arbitrary depth from one rule.
- **Honest provenance.** The projection is clearly secondary; readers know where to
  edit (the deck) vs. where things are merely *shown* (the meta).

### The two costs to budget for

1. **Dangling references** — delete a leaf and an emergence points at nothing. The
   build step should validate referential integrity and warn on orphans.
2. **Over-generality** — "everything is a node" can get too abstract to author
   comfortably. Mitigate with a small set of blessed generated emergences and good
   defaults, so most authors never touch the graph directly.

## 7. Carrying this to recursive.eco

The same spine applies, with one adaptation for a real backend:

> **Normalize at the source, materialize at the edge.**

- **Author normalized.** A leaf is a row/document; an emergence is a node that stores
  `composite_of: [leaf_ids]` + its own `name`/`sections`/`lens` — **not** the leaf
  content. In Supabase this is a self-referencing node table resolved by a recursive
  CTE (or kept as id-referencing JSONB documents).
- **Materialize for reads.** A static viewer can't cheaply resolve a graph across many
  files, which is exactly why *this* repo's meta-builder copies card data into the
  meta — that copy is a **materialized cache**, not a second truth. recursive.eco
  should do the DB version: keep references as the source of truth, run a
  build/resolve step that emits read-optimized projections on write. You get
  single-source-of-truth **and** fast reads.
- **Reuse the uniform node + lens model**, so the same renderer serves tree, timeline,
  graph, and pills from the node's own hint.

The one discipline that makes or breaks it, in either repo: **never let a projection
become a second place to edit the truth.**

---

*This model is already proven here: the decks are the truth, the meta is a generated
projection, and the viewer's lenses are driven by the emergence nodes themselves.*
