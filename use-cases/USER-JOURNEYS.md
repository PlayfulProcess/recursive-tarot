# User journeys — recursive-tarot × recursive.eco × MCP

**Status:** planning (June 2026). Companion to `docs/DESIGN-two-wings-provenance.md`
(+ its REVIEW + v2) and `docs/DESIGN-framework-extraction.md`.
**Purpose:** turn the provenance/two-wings debate from an internal taxonomy
argument into **acceptance criteria** — what each kind of person should be able
to do, through whichever door they arrive by, as a *user* and/or a *contributor*.

The model these journeys assume (v2 agreed conclusion):
**one library, two peer bands** — *Evidence* (`provenance:record`, dated +
attributed artifacts) and *Living tradition* (`provenance:living`, interpretation
and new making) — with **apparatus** (`provenance:reference`: books, people, the
genealogy) in neither. Boolean `draft` = early/incomplete, never a proxy for
"interpretive / non-Western." Peer presentation (equal-weight bands, a framing
line *above both*) is core, not deferred; only the rank-coded defaults
(below-the-line / collapsed / hidden) are held back.

---

## Personas × entry channels

| Persona | Arrives via | Wants | How the model serves them |
|---|---|---|---|
| **Lover / curious visitor** | search → a card; static tarot site; Library | read a card, draw, beauty + trust | honest badge ("artifact, Milan c.1450" vs "living, 2026"); no homework |
| **Historian / skeptic** | Library tarot channel; tree/timeline | dated+attributed record, genealogy, no mysticism-as-history | Band A held visibly apart; descent views are record-only *by definition*; sources cited |
| **Practitioner** | Library; a Living deck's Cast link | living tradition honored + sourced, not debunked | Band B is an **equal peer**, not a footnote; cultural sourcing in the blurb; `draft`≠"lesser" |
| **Light contributor** | in-app (Rung 1) or GitHub (Rung 2) | fix one wrong line | propose → owner merges; provenance owner-controlled |
| **Deck-maker** | Claude + MCP (Rung 5); Claude.ai/Desktop (3–4) | build / import / illustrate / publish a deck | `import`→`set_item_images`→`set_grammar_visibility`; lands in Band B |
| **Maintainer (owner)** | GitHub + MCP | review/merge, publish, keep the record clean | gated publish (complete→public, stub→private, never auto-community) |

---

## The journeys (entry → need → how served → current gap)

### J1 · Lover reads a card and draws (no account)
Search → a card page on the static site → scene/symbol + **provenance badge** →
"Cast / Draw" on recursive.eco → optionally sign up.
*Gap:* badge UI unbuilt; card pages live on the static site, Cast on
recursive.eco — the hop works via `_eco_ids.json`.

### J2 · Historian walks the record
Library tarot channel → **filter to The Record** → genealogy / timeline (record
only) → a deck page → a `books-of-tarot` citation → external full text.
*Serves:* the meta `DECKS` allowlist already keeps Living decks out of the
descent views, so interpretation can never masquerade as evidence.
*Gap:* a Library **provenance facet** (reuse `HashtagFilter`) doesn't exist; the
`provenance` field is in the repo but **not reliably in the DB yet** (see
"Integration reality").

### J3 · Practitioner meets a living deck
Library → **Band B (Living)** as a peer → reads 36 Tattvas / Ontoject as living
tradition, *sourced not debunked* (Śaiva sourcing in the blurb) → Cast.
*Gap:* the two Living decks are imported to the repo but **private in the DB**;
peer-band presentation unbuilt; `draft` must never render as a demotion ribbon
under a collapse.

### J4 · Light contributor fixes a date
(a) in-app Rung 1 (fork/edit → owner merges) **or** (b) GitHub Rung 2 (edit
`grammar.json` → PR). Provenance is owner-controlled, so an edit can't flip it.
*Gap:* none structural — works today.

### J5 · Deck-maker builds a living deck via MCP (no repo fork)
`get_grammar`/`import` → own library → `update_items` + `set_item_images`
(`commons_image_search` / `generate_item_image`) → `set_grammar_visibility` →
appears in Band B.
*Gap:* publish is a manual step; no idempotent slug→deckId identity (DB has dup
rows); true *in-place* community editing needs the small MCP build (Model B —
`join_grammar_as_editor` + pending-review writes).

### J6 · Maintainer merges, and the channel stays in step
PR merged to the canonical branch (**now `main`**) → webhook reindexes the DB →
channel reflects it.
*Gap (the big one, measured this session):* see below — the webhook fires but
coverage + content propagation are incomplete.

---

## Integration reality (measured 2026-06-21, after dev→main merge)

- **Branch model is now fixed:** `dev` → `main` merged; `main` (the webhook's
  default branch) carries all live work. Going forward, treat **`main` = the
  published/release branch**; keep working on `dev`; the dev→main merge is the
  publish event.
- **The webhook IS installed and fires:** `visconti-sforza-tarot`'s DB row was
  re-touched **7 s after** the merge to `main` (nothing manual touched it), while
  grammars without the backlink were not — so the GitHub-App reindex is wired.
- **But auto-sync is only partial today, two reasons:**
  1. **Only 2 / 32 repo grammars carry `_recursive_eco_url`** (the back-link the
     webhook reads to find the DB row). The other 30 are skipped
     ("no-documentId"). → needs an **eco-backlink stamp pass** (like
     `stamp_canonical_repo.py`, deriving each id from `_eco_ids.json`).
  2. **Even for the resolvable grammar, the new top-level `provenance` field did
     not land in the DB.** The row updated, but provenance is still absent — so
     repo→DB *content* propagation isn't confirmed end-to-end. Chase before
     relying on it (ownership-guard path match / deep-merge semantics).
- **Net:** repo→DB sync is **not yet reliable**. Until (1) every grammar is
  stamped and (2) a known field change is confirmed to propagate, the safe path
  for getting repo state live is still the **MCP** (publish + metadata), done by
  the owner.

---

## What the journeys turn into (build order)

1. **Stamp all grammars with `_recursive_eco_url`** (from `_eco_ids.json`) so the
   webhook can resolve them — unblocks J6.
2. **Confirm content propagation** end-to-end (provenance field → DB) — unblocks
   J2/J3 filtering.
3. **Live-sync `provenance` → DB** via MCP in the meantime (owner pass).
4. **Library provenance facet + peer-band presentation + badges** (recursive-eco
   build) — J1/J2/J3.
5. **Publish the 2 Living decks** to Band B once peer presentation exists — J3.
6. **Idempotent identity + gated auto-publish; Model B (in-place community edit
   via MCP)** — J5/J6.

Each item is gated by an explicit acceptance test (the "how served" line of its
journey), so "done" is observable, not asserted.
