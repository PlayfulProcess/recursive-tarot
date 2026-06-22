# Roadmap — Caster·Spread merge, 3-topic Courses, History enrichment

*Author: PlayfulProcess. Drafted 2026-06-21 from a long vision session. This is the spine
Claude builds toward, phase by phase, mostly autonomously. Each phase ships to `dev` (live on
tarot.recursive.eco) via its own squash-merged PR; `python scripts/check_all.py` must pass first.*

## North star
The tarot site has three jobs, and the UI should make each obvious: **learn** (Courses),
**set an intention & cast** (the Caster), and **contribute** (GitHub → recursive.eco). The
philosophy work (Kant / Linehan / Morality-is-an-ecosystem) is not decoration — it's the
*posture* you adopt before you draw, surfaced as voices on the Caster and as the Intention-Setting
course. Everything stays public-domain, static-first, contributable.

---

## Phase 1 — Merge the Caster and the Spread Builder  *(IN PROGRESS)*
One page (`viewers/caster.html`) does it all.
- **Spread dropdown** of well-known spreads from `viewers/spreads.json`: Structures·Process·Possibilities (house default), Single Card, Past·Present·Future, Five-Card Cross, **Celtic Cross** (10), plus **Custom**. Each spread carries per-position `x/y` so the board is recognisable (the cross looks like a cross).
- **Deck dropdown** (chronological — done) and **Cast** draw one card per position onto a **board** laid out by `x/y`.
- **Drag to rearrange** positions (pointer events; touch-friendly). **Custom** lets you add/edit/delete (or jump to the full Spread Builder).
- **Voices carousel** (intention) stays at the top (done; reads `voices.json`).
- **Save**: Download `.json` (cast + spread) · **Contribute to GitHub** (opens a new-file/PR flow for `spreads/`) · link to the *How to Contribute* course · keep the *Open in recursive.eco Journal* CTA.
- Retire/redirect `spread-builder.html` to the merged Caster's Custom mode (keep the file as the advanced designer, linked from the Caster).

## Phase 2 — Collapse Courses into 3 topics (with hyperlinkable subsections)
Today there are 6 flat courses. Re-home them under **three** topics, each a landing course whose
`##` sections are deep-linkable (`course-viewer.html?course=<topic>#<anchor>`):
1. **History** — the history of tarot (`history-of-tarot`), enriched per Phase 6.
2. **Intention Setting** — everything that is neither history nor technical (Phase 3).
3. **How to Contribute** — `build-a-tarot-deck-with-claude` + the new GitHub-contribution guide (Phase 4).
Keep the existing course slugs working (redirects/anchors) so nothing breaks. Update `site-header.js`
COURSES to the 3 topics (with sub-links), and the course-viewer TOC to support `#anchor` deep links
(it already builds anchors from headings — verify deep-scroll on load).

## Phase 3 — Intention Setting content
The home for the author's *why*. Spine = the existing **Tarot & the Crack** essay: *I was promised
things by tarot, was disappointed, and still find it valuable — through different lenses.* Then the
lens subsections: **Kant** (the law), **Linehan** (the relating), **Morality is an Ecosystem** (the
ground), with the shared **intention/voices**. The Caster's voice carousel deep-links each voice to
its subsection here (e.g. `?course=intention-setting#kant`). Update `voices.json` links accordingly.

## Phase 4 — "How to Contribute" course (+ screenshots)
A short course on contributing through GitHub: a **deck**, a **spread** (the new `recursive-tarot-spread`
JSON), or **another course** (`.mdx` + a `site-header.js` COURSES line). Walk the real steps:
fork / edit-on-web / add file / commit / open PR; then how it reaches recursive.eco (publish + `_eco_ids`).
Record the steps as **screenshots** (capture the GitHub "Add file" / PR UI via the browser) and embed
them. The Caster's *Contribute to GitHub* button links here.

## Phase 5 — "Edit card / View deck" component on cards
Every card (in `cards.html`, and ideally on the Caster board) gets a small affordance that opens
**recursive.eco** for that exact card/deck — `View deck` → `flow.recursive.eco/?deckId=<uuid>` and
`Edit card` → the deck's editor deep-link with the card's `source_item_id`. Resolve the deck UUID via
`tarot/_eco_ids.json` (Phase-done resolver `resolveDeckFlowId`). Gracefully hide/degrade for decks not
in `_eco_ids._public_now`.

## Phase 6 — Enrich the History of Tarot course (explain the dimensions)
Newcomers don't know the scaffolding. Add sections that explain:
- **The three Ways** (the Tree-of-Tarot genealogy): **Roots** (Milan c.1440s) → **the Southern Way**
  (Bologna & Florence), **the Eastern Way** (Ferrara), **the Western Way** (Milan → Marseille), then
  **the Occult Reframing** (France: Court de Gébelin → Lévi → Papus → Golden Dawn → Waite) and
  **Sui Generis & Relatives** (Sola Busca, Mantegna, modern derivatives).
- **Why "A/B/C orders"** — Dummett's regional trump-ordering theory (A = South/Bologna-Florence,
  B = East/Ferrara, C = West/Milan), which is *why* we catalogue the "Ways" the way we do
  (`_collection.json` `branches`).
- **Why a Tree of Life** — the genealogy metaphor: an object that kept its picture while its meaning
  was rewritten; lineages, not a single trunk. Link the live **Tree** (`genealogy-tree.html`) and
  **Emergence Explorer** (`explorer.html`) and explain its **dimensions** (century, suit, arcana, order,
  function, lineage) — "every grouping is an emergence."

---

## Cross-cutting (already shipped)
- Chronological deck dropdowns (cards + caster). · Deck-aware "Get a Reading" (`?src=` → `_eco_ids` →
  `?deckId=`). · Real auth detection (`window.recursiveAuth`, the `.recursive.eco` session).

## Conventions / guardrails
- Static-first, no backend on tarot (auth-widget only *reads* the shared session). PD/CC-BY-SA only.
- Work on a branch off `dev`; `check_all.py` green; squash-merge; delete branch (no sprawl).
- Author = PlayfulProcess (never a real name). AI disclosed where used.
- Contribution model: edit JSON/MDX on GitHub → PR → merge → (for decks) publish on recursive.eco + add to `_eco_ids.json`.

## Build order
1 (Caster merge) → 6 (History enrichment, self-contained content) → 2 (Course IA) → 3 (Intention content) → 5 (Edit/View component) → 4 (Contribute course + screenshots). Phases 2 & 3 are coupled (do together).
