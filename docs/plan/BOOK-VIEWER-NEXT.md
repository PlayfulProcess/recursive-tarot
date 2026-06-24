# Book viewer — agreed improvements (rev. June 15 2026)

> **Update (later same day):** shipped & live on `dev` — embed **light mode** (system-aware +
> forced light in the book), dead **dropdown removed**, tree **hover both directions**,
> **render-in-full** (no inner scroll), timeline **right-crop fixed** + controls legible in light;
> **plates redesign** (Death analysis + iconic gallery); **section re-order** (Decks after Lineage;
> card-detail folded into each suit/major breakdown); **per-deck "Hands Behind the Cards"** (makers +
> "Studied by" scholars in each deck chapter; standalone section removed). The **Numbers** section
> already carries its per-number detail embed. **Still open:** the playable historical game.

Captured from the in-app book review session. Status: ✅ shipped · 🟡 partial · ◻ pending.
The book renders from the **local `course/` files** (canonical as of this session); the viewer
logic lives in `pages/course-viewer.html`, the embeds in `viewers/*.html`, the synthesis prose in
`research/synthesis/*.json`.

## Card strips (`.strip` in course-viewer)
- ✅ Responsive grid (`repeat(auto-fill,minmax(96px,1fr))`) so every card in a row is visible at
  once instead of a horizontal scroll; collapses to 2 columns in `@media print`.
- ✅ Hover-zoom matching Explorer (`transform:scale(1.7); z-index; position:relative`).

## Layout / prose
- ✅ Left sidebar scrolls independently (`max-height:calc(100vh-120px); overflow-y:auto`) so it no
  longer scrolls the whole course.
- ✅ De-duplicated the Four-Suits intro: the mdx keeps the evocative "watch a number transform"
  lead; `suits.json _intro` now carries only the unique Mamluk→Europe→Sola-Busca→RWS descent
  (the "older half / abstract pips counted like wallpaper" line was said twice).

## Embeds — genealogy tree & timeline (`viewers/genealogy-tree.html`, `viewers/timeline.html`)
- 🟡 **Light mode, system-aware** (`prefers-color-scheme: light`) for both. Tree `:root` light
  override + `color-scheme` started. TODO: thread `--bg` into the hardcoded node/text halo strokes
  (`#0f0d17`), axis/gridline/legend/hint colors → vars; repeat for timeline; verify SVG text halos.
- ◻ **Tree hover → both directions.** Today `traceDescent` lights the node, its taxonomic
  ancestors, and the `derives_from` chain *upstream*. Add a *downstream* walk (reverse `derives_from`
  edges) so descendants light up too; the `.derive-link` dim already keys on both endpoints ∈ keep.
- ◻ **Timeline embed:** hide the **Descent toggle**, the **view-switcher** ("view icon"), and the
  **Lane dropdown** in `?embed=1`.
- ◻ **Delete the Lane/Hub dropdown from BOTH viewers entirely.** In practice only `branch` qualifies
  (`DimensionEngine.discoverFields` over tree-of-tarot deck metadata returns just `branch (6)`), so
  the control is a no-op. Hardcode `laneField`/`hubField='branch'`. (Reverses "P5 step 5".)
- ◻ **Render in full, no internal scroll.** In `?embed=1`, post content height to the parent via
  `postMessage`; course-viewer listens and sets the iframe height; drop `.viewer-frame`'s fixed
  520px + internal overflow. Also hide `<site-header>`/`<view-switcher>` chrome in embed mode.

## Plates (`data-embed="plates"`)
- ◻ `.plate` has **no CSS** → raw default figures = the "dislocation". Add layout CSS.
- ◻ Redesign into two parts: (a) the **Death-across-the-centuries** analyzed sequence (Visconti-Sforza
  1451 → Marseille 1760 → RWS 1909 — the skeleton persists, the staging is rebuilt), then (b) a
  curated **iconic-cards gallery** for *diversity + continuity* (e.g. the Fool across Visconti →
  Marseille → RWS; Visconti World; Sola Busca pip 1491; Mantegna; a Mamluk root card). Each links to
  its card in `cards.html`.

## Section structure / ordering (`course/history-of-tarot.mdx`)
- ◻ Move **"The Decks"** to render immediately **after the Lineage** section.
- ◻ **"The Hands Behind the Cards" → per-deck.** Render the people behind each deck *inside that
  deck's chapter* (drawn from `people-of-tarot` links), rather than as one standalone section.
- ◻ Move **"The Cards in Detail"** so the trump detail renders **after the major-arcana breakdown**
  and the suit detail **after each suit breakdown**, instead of one block at the end.
- ◻ Build a **Numbers in Detail** view parallel to trumps-detail / suits-detail (we already have
  `numbers.json`, `_numbers-evidence.json`, and the `numbers` embed — extend to a per-number detail
  with the cross-suit readings linked back to the grammars).

## New feature — play the historical games
- **Research (PD rule sources):** Court de Gébelin, *Le Monde Primitif* vol. VIII (1781) describes
  the game and is public domain. [pagat.com/tarot](https://www.pagat.com/tarot/) (David Parlett) is
  the best free modern rules reference (not PD). Documented variants: **Tarocchino Bologna** (62
  cards), **Minchiate** (97/98), French Tarot.
- ◻ **Proposal:** a backend-free, static page (like the other viewers) where a user can play a
  *simplified* trick-taking trump game — e.g. Tarocchino Bologna or a 22-trump demo — vs. a basic
  AI, rendered with our public-domain deck images. Scope/ruleset TBD with the builder.

## Earlier open follow-up
- ◻ Carry `minor_key` into the meta grammar (`build_meta_grammar.py` metadata whitelist) so
  Explorer/Lenses can group minors canonically (parity with how decks already group by it).
