# Recursive Tarot — Future Plan

This repo is the **free, public, GitHub-Pages home** of the tarot grammars
(`tarot.recursive.eco`). The static viewers in `viewers/` are backend-free and
"committed to drift": good things get promoted to recursive.eco later, but the
data and the self-contained viewers live **here** first.

---

## Parked: live integration with recursive.eco (the hyperlinked grammars)

**Goal.** Each card on the static site can *also* open live in the recursive.eco
app — the full experience (oracle, AI reading, fork). The static deep-link
mechanism is already proven (see below); the only missing ingredient is that the
grammars must exist in Supabase with stable UUIDs.

**Status (Jun 2026).** Static deep-links are DONE and live. Live integration is
**parked** until we choose the import path.

### What already works (no backend)
- `viewers/cards.html` honors `?item=<id>` — opening a card writes it to the URL
  (shareable), and loading with it auto-opens that card.
- On the fat meta (`all-decks-many-lenses`), every card carries
  `metadata.source_deck` (repo slug) + `metadata.source_item_id` (card id in that
  deck). The modal shows **"Open in <deck> deck →"** which loads
  `cards.html?src=../tarot/<slug>/grammar.json&item=<card-id>`. All 811 source
  cards resolve. This is the same `grammar-viewer.html` mechanism recursive.eco
  uses in production (CardDetailModal → `getTarotViewerUrl` → `?item=`), so the
  static site is a faithful rehearsal of the live path.

### The live path (two options)

**Prerequisites for either:** each imported deck must be `is_public = true`, and
the import must preserve `document_data.items[].id` exactly (the `?item=` join
needs `source_item_id` to still match). Log in / own as **pp@playfulprocess.com**.

1. **UI import (manual, ~13 decks).** Import each deck via the recursive.eco
   Create flow, publish public, then **capture each deck's UUID** and build a
   `slug → UUID` map. Pros: no scripting. Cons: **not idempotent** — re-importing
   a deck mints a NEW UUID and breaks any hardcoded links; you must re-capture.
2. **Script import (idempotent).** Stamp a **deterministic UUIDv5** (namespace +
   deck slug) into each repo grammar locally, then `upsert` into Supabase keyed on
   that id. Pros: reproducible, repo stays the source of truth, links never rot,
   no read-back. Cons: one script to write. **Recommended.**

Then: add an "Open live in recursive.eco" link to each static card pointing at
`recursive.eco/pages/grammar-viewer.html?type=tarot&id=<uuid>&item=<card-id>`,
using the `slug → UUID` map.

### ⚠️ UI round-trip fragility (learned the hard way, Jun 2026)
The recursive.eco "Merge edit" write-back **drops custom top-level grammar fields**
it doesn't know about. A UI round-trip on Visconti-Sforza silently stripped:
`lineages`, `roots`, `shelves`, `worldview`, `_grammar_commons`, `_github_source_url`
(restored from git `cf4f242`). Items, images, sections, and L1 metadata survived.
**If you import/edit a deck via the UI, re-check these top-level fields against the
repo afterward and restore any that were dropped.** The script path avoids this
entirely.

---

## Viewers

- `viewers/cards.html` — card grid + hierarchy sidebar + per-card deep-links.
- `viewers/tree-viewer.html` — faceted level-rows tree (L1/L2/L3 by deck/age/rank/…).
- `viewers/genealogy-tree.html` — **NEW radial "Tree of Life."** Renders
  `tarot/tree-of-tarot` as root → 6 scholarly branches → decks, with the actual
  `derives_from` descent overlaid as curved arcs (hover a deck to trace its
  lineage upstream). Click → detail panel + "Open <deck> cards." Self-contained
  D3, no backend.
- `viewers/caster.html` — draw 3 cards (one deck or cross-deck) → export JSON for
  recursive.eco Journal.
- `genealogy.html` — Cytoscape force-graph of the genealogy.

### Tree-format ideas not yet built
- **Chronological phylogeny**: place decks on a horizontal time axis (parse
  `metadata.when` → year) with `derives_from` edges — shows descent *and*
  chronology at once. `deck-italian-trionfi` is referenced as an ancestor by 6
  decks but isn't yet a node; add it (or a synthetic "trionfi root") so those
  descent arcs render.
- **Archetype axis** (cross-deck): one card (e.g. Death) across all decks, joined
  on the stamped `metadata.archetype` controlled vocabulary. Engine is general;
  tarot is the first dictionary.
