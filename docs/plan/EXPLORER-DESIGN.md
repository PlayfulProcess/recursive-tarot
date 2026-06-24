# Emergence Explorer — pivot/dashboard design (June 11 2026)

*Goal: a Power-BI / pivot-table-style preview — drag fields into **Rows / Columns /
Filters** boxes and watch emergences form, superposing any fields regardless of
whether they came from metadata, keywords, or emergence membership. Long-term: one
shared engine behind ALL the previews.*

---

## 0. The key design insight

A BI pivot aggregates numbers (sums, averages). Here the "measure" is **the cards
themselves** — so a cell is a *stack of card thumbnails with a count*, not a sum.
That one change makes the pivot a *gallery generator*: every cell IS an emergence
(a pattern over the same cards), which is exactly the EMERGENCES.md model. The
"Counts" mode (heatmap) recovers the classic BI view when you want analytics.

**The data model is a star schema hiding in plain sight:**
- **Facts** = leaf items (cards) — anything without `composite_of`.
- **Dimensions** = auto-discovered from three sources, treated identically
  ("superposition independent of being keywords or not"):
  1. `metadata.*` scalar fields → deck, year (auto-bucketed to `century`), suit,
     rank, arcana, order, function, `print.quality`…
  2. `keywords` → namespaced `ns:value` keywords become field `ns ·kw`
     (e.g. `arcana:the-fool`); plain keywords become a multi-value `keyword` field.
  3. **Emergence membership** → reverse index of every `composite_of` becomes a
     multi-value `emergence` field (a card "is in" By Age · 1760, Aces, …).
- Multi-value dimensions are first-class: a card may appear in several groups
  (stated in the UI; counts are per-group, not a partition).
- Field discovery is **automatic** (any field with 2–64 distinct values becomes a
  draggable chip) — so the explorer works unchanged on ANY grammar, including
  future user-created ones in recursive.eco.

## 1. Alternative A — custom "Emergence Explorer" ✅ BUILT (v1 live)

`viewers/explorer.html` — zero dependencies, self-contained, house dark style.
- Chips tray (auto-discovered fields) + three drop zones: **Rows** (multi → nested
  grouping), **Columns** (single, v1), **Filters** (click chip → value-picker
  popover with search/All/None).
- Cells render up to 6 thumbnails + `+k` count, hover-zoom, click → lightbox.
  **∑ Counts** toggle = violet heatmap.
- Spec serialises into the URL hash → shareable/bookmarkable pivots.
- Deck picker reads `_collection.json`; `?src=` works like the other viewers.
- Default view on the meta: rows=`century` × cols=`suit`.

Why this first: cells-as-card-stacks is the whole point, and no off-the-shelf
pivot renders image-stack cells well; 600 lines bought exactly the interaction we
want with no jQuery/WASM tax.

## 2. Alternative B — PivotTable.js (fallback if A's UX feels weak)

[pivottable.js](https://pivottable.js.org) (MIT, jQuery): the classic drag-drop
pivot UI. Pros: battle-tested drag/drop, dozens of renderers (heatmaps, charts via
Plotly). Cons: jQuery dependency; image-stack cells need a custom renderer anyway;
dated look needs a dark-theme pass. Adoption path: feed it the SAME flattened
records from `flatten()` (keep our extraction layer), write one custom
`cardStackRenderer`. ~1 session.

## 3. Alternative C — FINOS Perspective (the heavy "real BI" option)

[Perspective](https://perspective.finos.org) (Apache-2.0, WASM columnar engine):
true Power-BI-grade — group-by/split-by/filter/sort/expressions, d3fc charts,
streaming. Pros: the most powerful analytics; gorgeous. Cons: ~3–5 MB WASM,
numeric-centric (datagrid won't show card thumbnails in cells), config UX is its
own design language. Best role: **a "Stats" tab for analytics**, not the gallery
pivot. Only reach for it if we want serious charting over the collection.

**Inspiration (not dependencies):** Vega-Lite/Voyager (shelf-building UX:
drag field → encoding shelf), Observable Plot (faceting = our rows×cols),
Metabase's filter-pill pattern.

## 4. One infrastructure for all previews (phase 2)

Extract the v1 engine into `viewers/explorer-core.js` with three pure functions:
```
flatten(grammar)        → records   (3-source field extraction, shared)
discoverFields(records) → fields    (auto chips)
query(records, spec)    → tree      (spec = {rows, cols, filters})
```
Then each existing preview becomes **a renderer over the same spec**:
- `cards.html` Group-by = `{rows:[axis]}` with the grid renderer (replaces its
  bespoke filter plumbing).
- `timeline.html` = `{rows:['year']}` + timeline renderer.
- `genealogy` = `derives_from` edge renderer (after the tag re-architecture in
  `HANDOFF-rearchitect-genealogy.md` — same "keywords in, emergences out" spine).
- The caster's deck filter = `{filters:{deck:[…]}}`.
This is the same engine recursive.eco can run server-side over Supabase rows.

## 5. Risks / known v1 limits
- Columns zone takes ONE field (nested column headers postponed).
- Multi-value dims duplicate cards across groups (by design; labelled).
- HTML5 drag-drop is desktop-first; mobile uses tap-to-add (chip click → Rows).
  A pointer-events rewrite is a polish task.
- 900-card meta renders fine; >5k records would need virtualised cells (later).
