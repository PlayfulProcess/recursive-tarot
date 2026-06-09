# Multi-Lens Emergences — Plan

*One catalogue, many lenses. Each axis is an emergence pattern over the same items,
and each axis declares **how it renders** via `render_as`. The viewer shows a
lens-picker; choosing a lens swaps the renderer, not the data.*

Status: **partially built.**
- ✅ **Phase 1** — `lens` stamped on all 5 meta axes (By Deck/Lineage→`genealogy`, By Age→`timeline`, By Rank/Function→`pills`).
- ✅ **Phase 2** — numeric `metadata.year` stamped on all 768 meta cards (queryable).
- ✅ **Timeline renderer** — `viewers/timeline.html`, the Phase-3 build-first proof (decks on a year axis + descent edges), live & verified. Added to the shared header.
- ⏳ **Remaining** — the unified lens *dispatcher* (pick an axis in `cards.html` → swap renderer) and Phase 4 (cross-lens deep-linking). The timeline is standalone for now.

---

## 1. The idea in one sentence

Items are catalogued **once** (their intrinsic data). An **axis** is an emergence
node grouping those items a particular way, and its `render_as` field picks the
visualization. Switching lens = switching renderer over the same items.

## 2. What already exists (the foundation)

The meta (`tarot/all-decks-many-lenses`) already carries axis nodes:

```
axis-deck     (By Deck)     render_as: pill-group
axis-age      (By Age)      render_as: pill-group
axis-number   (By Rank)     render_as: pill-group
axis-lineage  (By Lineage)  render_as: pill-group
axis-function (By Function) render_as: pill-group
axis-keyword  (By Keyword)  render_as: pill-group   ← swept across all decks this session
```

Today every axis renders the same way (pills). This plan lets each axis pick a
different renderer.

## 3. The `render_as` vocabulary (proposed extension)

`render_as` lives on a grouping/axis node and is read at render time. It is
**additive, reversible, and `absent = default` (render as item).**

| `render_as` | Renders as | Renderer status |
|---|---|---|
| `pill` / `pill-group` | compact filter chips | ✅ exists (`cards.html`) |
| `item` | a full node/card | ✅ exists (default) |
| `tree` | level tree (arcana → suit → number) | ✅ exists (`tree-viewer.html`) |
| `genealogy` | the descent DAG | ✅ exists (`genealogy.html` / `genealogy-tree.html`) |
| `timeline` | x-axis = time, buckets per era | ❌ **new renderer** |
| `grid` | the card grid | ✅ exists (`cards.html`) |

Intended axis → renderer wiring:

```
By Arcana / metastructure → tree
By Age                    → timeline
By Deck                   → genealogy
By Keyword / By Rank      → pills
(default)                 → grid
```

## 4. Switching a category's lens *in session*

Because `render_as` is **one field read at render time**, moving a category from
pill to item (or to tree/timeline/genealogy) is a single, non-destructive,
reversible edit.

- **Data model: ready now.**
- **Interactive toggle: a small UI piece** — a per-category "render as ▾" control
  (pill / item / tree / timeline / genealogy). The viewers currently *read*
  `render_as` but don't expose a control to *flip* it live. Once added, switching a
  category's lens mid-session re-renders with no rebuild.

## 5. Queryability guarantee (why lenses don't cost queryability)

Membership lives in two places, and the item half is the source of truth:

1. **On the item** — `metadata.suit/rank/arcana/number/element/year`, `keywords[]`,
   `category`. Fully queryable directly (JS `items.filter(...)`; Supabase
   `jsonb_array_elements(... )->'metadata'->>'suit'`). This is how Marseille/Sola
   Busca cards were pulled by suit.
2. **On the emergence node** — `composite_of` (the parent's child list). Derived
   *from* the item data above; invert once into a `card → [emergences]` reverse
   index if needed.

Emergences are a **render layer over queryable item data**, never a replacement.
Adding lenses adds *more* stamped, queryable fields (e.g. `metadata.year`), never
fewer. Hot facets can later be promoted to a Postgres `GENERATED ... STORED`
indexed column — flexible JSONB *and* an index.

## 6. Two real challenges (and how to handle them)

1. **Level mismatch — genealogy is deck-level, cards are card-level.** "By Deck →
   genealogy" arranges the axis's *metacategories* (decks) by ancestry
   (`derives_from` in `tree-of-tarot`), with cards as the drill-down. The renderer
   must know it's drawing group-nodes, not leaves; clicking a deck drills to cards.

2. **Timeline needs clean numeric years.** Cards carry `metadata.when` as prose
   ("Milan, c. 1451"). Stamp a parsed integer `metadata.year` so the timeline is
   exact, not regex-at-render. Model years as **point-in-time buckets**; make
   *cumulative* ("everything that existed by year T") a **toggle in the timeline
   renderer**, NOT baked into `composite_of` (cumulative nesting would explode
   membership and duplicate every card into every later year). Same data, two view
   modes.

## 7. Phased plan (each phase independently shippable)

- **Phase 1 — Formalize the lens contract (data + docs, no UI).** Extend the
  `render_as` vocabulary; stamp the right renderer on each existing axis
  (By Deck→genealogy, By Age→timeline, By Arcana→tree, By Keyword→pills). Document
  in `GRAMMAR_FORMAT.md`. Existing viewers keep working.
- **Phase 2 — Stamp the auxiliary data renderers need.** `metadata.year` (integer)
  on decks/cards parsed from `when`/era (feeds timeline). Make `axis-deck`
  metacategories reachable to `derives_from` ancestry (feeds genealogy).
- **Phase 3 — Lens dispatcher + the timeline renderer.** One "Lenses" view (extend
  `cards.html`) with a lens-picker (axes become tabs). On select, read the axis's
  `render_as` and dispatch to a renderer module. Reuse tree / genealogy / pill-bar
  as modules; build the **one new piece — the timeline renderer** (year buckets on
  an x-axis, cumulative toggle, click a bucket → its cards).
- **Phase 4 — Shared deep-linking across lenses.** `?lens=timeline&item=…` so a card
  stays selected as you switch lenses and the lens choice is shareable.

## 8. Build-first recommendation

A thin proof: wire the existing **By Age** axis to a minimal **timeline renderer**
in `cards.html` (era buckets already exist). It's the one genuinely new capability,
it's small, and it proves the "axis declares its renderer → view morphs" contract
end-to-end. If the timeline lands, By Deck→genealogy and By Arcana→tree are mostly
*pointing existing renderers at an axis*. Keep cumulative-year a **render toggle,
not a data structure**, or membership explodes.

---

*Companion to `GRAMMAR_FORMAT.md` (the emergence/`composite_of`/`render_as` schema)
and `FUTURE_PLAN.md`.*
