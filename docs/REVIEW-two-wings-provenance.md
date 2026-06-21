# Review — "Two Wings: provenance as the organizing principle"

**Reviewer:** Claude (Opus 4.8), 2026-06-20. Companion to
[`DESIGN-two-wings-provenance.md`](DESIGN-two-wings-provenance.md).
**Reviewer context:** just made `books-of-tarot` + `people-of-tarot` live and
community-open on recursive.eco and audited the 28-grammar collection — so this
is grounded in the real data layer.

## 1. Does "two wings by kind, not rank" hold up?

The **principle is sound** — provenance is the one value both camps share, and
making it the spine (not a hide-the-other toggle) is right. Three wobbles:

- **The binary is coarser than what you already have.** `all-decks-many-lenses`
  already classifies every deck on `function: game | divination | esoteric |
  origin-myth`, plus `order / tier / era / ancestry`. That is *more*
  historian-friendly than Record/Living. The binary flattens distinctions you've
  already drawn (a 1450 painted Visconti artifact vs a 1909 mass-market RWS deck
  both become "Record").
- **Historian (Dummett/Depaulis) objection:** "The Record" conflates *primary
  artifact* (a surviving 15th-c. card = evidence) with *published modern product*
  (RWS-1909 — a dated artifact but also a self-interpreting occult publication).
  Keep the occult decks (Etteilla 1789, Wirth 1889, Court de Gébelin 1781, RWS
  1909) in Record **but** keep `function: divination|esoteric` so they're not
  mistaken for game-era evidence. The binary alone hides that.
- **Practitioner (Wen) demotion:** the doc says "kind, not rank," but the UX
  defaults say rank — Living is *below a divider, collapsed by default,
  default-hidden on scholarly surfaces*, under a manifesto opening "*the cards
  stop being evidence*." Below + collapsed + hidden = subordinate, whatever the
  sentence says. And `draft` on the **36 Tattvas** (Śaiva-sourced) risks reading
  as the exact cultural flattening Wen warns of. Decouple "draft = early/incomplete"
  from anything cultural; make the bands *peer* bands, not default+appendix.

## 2. The four decisions — recommendations

- **(a) RWS/Thoth in The Record? → Yes**, but keep the `function: esoteric` nuance
  so they aren't confused with game-era artifacts.
- **(b) Segmented vs bands? → Collapsible bands, no global hard mode** (agree with
  the doc), but make them *peer* bands, not default+appendix.
- **(c) Dotted off-record genealogy leaf in v1? → Defer (reconsider entirely).**
  "Greyed/dotted/quarantined" is the single most demotion-coded element; drop the
  quarantine framing if it ever ships.
- **(d) Where do drafts surface? → Hidden from default lists; visible via a
  "show drafts" pill + always-ribboned on their own page** — with the caveat that
  `draft` must mean only "early," never a stand-in for "culturally interpretive."

## 3. Feasibility (from the live data layer)

- ✅ **`_collection.json` is safe.** `refresh_collection.py` only rewrites a fixed
  derived set; new keys (`provenance`, `draft`) are preserved.
- ✅ **Record-only views are already protected.** `build_meta_grammar.py` selects
  decks from a hardcoded `DECKS` allowlist, so importing a Living deck into
  `tarot/` can't pollute the genealogy/timeline unless explicitly added.
- ⚠️ **Generated grammars can't be hand-tagged.** `all-decks-many-lenses`,
  `people-of-tarot`, `tree-of-tarot` are rewritten by their build scripts. Their
  provenance must come from the generator or live only in `_collection.json`.
- ⚠️ **Name collision.** Deck grammars already use **item-level
  `status: "surviving"|"lost"`** (whether a card survives). The doc's grammar-level
  `status: published|draft` is a different scope, same word — a footgun.
  **Resolved:** use a boolean **`draft: true`** at grammar level (absent =
  published); leave item-level `status` alone.
- ⚠️ **`build_tarot_collection.py` clobbers.** It rebuilds `_collection.json` from
  scratch (from the sibling schemas repo) — rare, not in the gate, but would drop
  hand-added provenance. So the **durable home is the grammar.json files**, with
  the collection scripts deriving it.
- 🚩 **The repo has no Living decks yet.** Ontoject Tarot and the 36 Tattvas live
  only in the recursive.eco DB (no `tarot/*` dir, no `_collection` slug). Today the
  split divides nothing in the repo (24 historical decks + 4 reference/meta
  grammars, all Record-side). *Decision taken:* import the two Living decks into the
  repo first, then tag.
- 🚩 **Reference/meta grammars fit no wing.** `books-of-tarot`, `people-of-tarot`,
  `all-decks-many-lenses`, `tree-of-tarot` are apparatus *about* the record.
  Proposed third value **`provenance: "reference"`** rather than forcing them into
  Record.
- 🚩 **Live-sync gap.** Provenance added in the repo will **not** appear on the
  recursive.eco DB copies automatically (separate store; needs an MCP pass).

## 4. Cut / simplify

- **Cut the dotted off-record genealogy leaf** — highest optics risk, least value.
- **Don't invent `made`/`interprets`** — most "made" data already exists (the
  `YEARS` map + deck dossiers + the meta's per-deck `date/era`). Derive, don't
  duplicate.
- **Use boolean `draft`** (avoids the `status` collision).
- **Add `provenance: "reference"`** for apparatus grammars.
- **Reframe scope:** the split's real subjects live on recursive.eco; the repo
  mainly needs to *carry the field*. This is more a channel/DB design than a
  repo-listing-UI build — which shrinks it.

**Net:** ship the *labeling* (provenance field + honest badges/blurbs) — the
low-risk core. Hold the *spatial* moves (below-the-line divider, collapsed band,
quarantine leaf) until felt, because they are what turn "kind" back into "rank."
