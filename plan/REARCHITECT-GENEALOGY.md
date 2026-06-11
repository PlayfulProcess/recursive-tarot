# Re-architect cataloguing & genealogy — keywords in, projections out

*Design doc (no code yet). Companion to `EMERGENCES.md` (the model),
`MULTI_LENS_PLAN.md` (the lenses), and `plan/HANDOFF-rearchitect-genealogy.md`
(the brief + live drift findings). Once built, this doc is the contract for
the tag vocabulary, the generator, and what every surface reads.*

---

## 0. The problem, restated precisely

The repo already has ONE self-healing pipeline:

```
tarot/<slug>/grammar.json  ──build_meta_grammar.py──►  all-decks-many-lenses  ──►  Cards viewer ✅
```

…and FOUR side-channels that drift because a human must remember them:

| Surface | Reads today | Why it drifts |
|---|---|---|
| Genealogy tree (`viewers/genealogy-tree.html`) | `tarot/tree-of-tarot/grammar.json` | hand-authored nodes + `derives_from`; advertises unbuilt decks (Soprafino, Lombardy), misses built ones (Viéville, Paris, Ma Diao) |
| Timeline (`viewers/timeline.html`) | `tarot/tree-of-tarot/grammar.json` | same file, same drift |
| Caster (`viewers/caster.html`) | meta's `_decks` | `_decks` comes from the `DECKS`/`ANCESTORS` **dicts hardcoded inside `build_meta_grammar.py`** — 13 + 5 entries while the repo has ~26 deck folders |
| Shop (`pages/shop.html`, `pages/print-viewer.html`) | `print-products.json` (manual) | 8 products; 12+ decks missing |
| Collection (`tarot/_collection.json`) | written by `build_tarot_collection.py` | a one-time **migration** script that reads the *sibling schemas repo*; the 6 ancestor decks built directly here never entered it |

**Root cause:** per-deck facts (era, order, function, editorial, ancestry,
parentage) live in *scripts and side files*, not in the decks. Anything not in
the deck can't be regenerated from the deck.

**The fix in one sentence:** move every per-deck fact into the deck's own
`grammar.json` as a small namespaced tag block, make ONE generator that globs
`tarot/*/grammar.json` and emits *every* catalogue surface (meta, tree-of-tarot,
collection, shop feed) as projections, and let the existing viewers keep their
URLs — they just start reading generated files.

```
                       ┌─ tarot/all-decks-many-lenses/grammar.json  → Cards, Caster
tarot/<slug>/          │
 grammar.json          ├─ tarot/tree-of-tarot/grammar.json (GENERATED) → Genealogy, Timeline
 metadata.catalog ──►  │
 (the only truth)      ├─ tarot/_collection.json                   → loader.js, deck picker
        +              │
 print/products-       └─ print-products.json (GENERATED join)     → Shop, print viewer
 overrides.json
 (commerce facts only)
```

Key elegance: `genealogy-tree.html` and `timeline.html` already default to
`../tarot/tree-of-tarot/grammar.json`. We don't repoint them — we **demote
tree-of-tarot from authored to generated**. Zero viewer changes for those two
surfaces. The caster already reads `_decks`; it heals the moment `_decks` is
derived from the glob instead of the dict.

---

## 1. The tag vocabulary — `metadata.catalog` on every deck grammar

One namespaced block at the **grammar root** (not per card). Namespacing under
`catalog` avoids colliding with the ad-hoc `metadata` some new decks already
carry (e.g. Viéville's free-text `order: "Eastern/Belgian-leaning"` — which is
*prose*, not a tag, and stays where it is).

```jsonc
"metadata": {
  "catalog": {
    // ── identity ────────────────────────────────────────────────
    "kind": "tarot",            // tarot | ancestor | cousin | non-tarot | planned | meta
    "status": "built",          // built | planned | image-blocked

    // ── time & place (timeline lens) ────────────────────────────
    "year": 1451,               // integer point-estimate; positions the node
    "year_label": "c. 1451",    // display string, hedged — never parsed
    "place": "Milan",

    // ── classification (pill/genealogy lenses) ──────────────────
    "order": "C",               // "A" | "B" | "C" | "occult" | null (Dummett)
    "order_disputed": false,    //  + order_note when true (Charles VI)
    "function": "game",         // game | origin-myth | divination | esoteric

    // ── relations (genealogy DAG) ────────────────────────────────
    "derives_from": [],         // parent slugs; [] = root. SOLID edges.
    "derivation_note": null,    // hedge text when an edge is debated
    "related_to": [],           // cousins / influences. DASHED edges.
                                // e.g. ganjifa → related_to: ["mamluk-deck"]

    // ── projection membership ────────────────────────────────────
    "in_card_pool": true,       // joins arcana/suit/rank tree + caster pool
                                // (false for ancestors, non-tarot, meta)

    // ── editorial (moves OUT of build_meta_grammar.py's DECKS dict)
    "editorial": {
      "maker": "Bonifacio Bembo workshop (attrib.)",
      "patron": "House of Visconti–Sforza, Milan",
      "context": "Hand-painted ducal luxury deck, among the oldest surviving tarot",
      "print": "Hand-painted, gold leaf & tempera",
      "orientation": "Game (trionfi); no record of divinatory use this early"
    },

    // ── era bucket (By Age axis) ─────────────────────────────────
    "era": "15th c · Renaissance Italy",
    "era_sort": 1
  }
}
```

Rules:

1. **Slugs are the foreign keys.** `derives_from` / `related_to` reference
   directory names under `tarot/`. The generator validates every reference
   resolves; a dangling slug **fails the build** (not a warning — drift is the
   disease this design exists to cure).
2. **`year` is a point estimate for layout; `year_label` is the truth shown to
   humans.** Hedging lives in the label ("16th–18th c"), never in the integer.
3. **Two edge types, deliberately.** `derives_from` is *direct parentage* (the
   genealogy DAG proper). `related_to` is *cousin/influence* (Ganjifa beside
   Mamluk; Sola Busca's influence on RWS minors; Ma Diao illustrating the
   Chinese money-card form). Collapsing these into one list is how genealogies
   lie — the dashed/solid distinction is the house "hedge debated claims" style
   expressed structurally.
4. **Debated facts carry their dispute inline** (`order_disputed` +
   `order_note`, `derivation_note`). Renderers show a ⚖/～ marker and the note.
   The data never asserts more confidence than the research files do.
5. **Card-level tags don't change.** Cards keep `metadata.suit/number/arcana`;
   the existing name-normalizers in the builder keep doing the cross-language
   matching. This design only moves *deck-level* facts.

### Planned / unbuilt decks become stub grammars

The old tree advertised Soprafino and Lombardy with nothing behind them. The
generated tree can only show what exists — so *make intent exist*: a planned
deck gets a **stub grammar** (`tarot/<slug>/grammar.json` with
`catalog.kind/status: "planned"`, a description, `derives_from`, and an empty
`items: []`). The genealogy renders it as a ghost node ("planned"); the card
pool, caster, collection and shop simply skip `status != "built"`. When the
deck is actually built it gains items and flips status — same file, no second
list. (Brera-Brambilla, currently image-blocked, gets `status:
"image-blocked"` — shown as ghost with that note.)

The `tarot/test/` folder gets `kind: "meta"` or is deleted; the generator
excludes `kind: meta` from every public projection.

---

## 2. The generator — one script, five projections

Replace the pair (`build_meta_grammar.py` + the dead `build_tarot_collection.py`)
with **`scripts/build_catalog.py`**, which is *data-free*: it contains rules,
not deck lists.

```
PHASE 0  Discover     glob tarot/*/grammar.json
PHASE 1  Validate     catalog block present & enums legal; derives_from/related_to
                      resolve; year integer; DAG is acyclic; in_card_pool decks
                      have items. Errors fail CI; warnings print.
PHASE 2  Normalize    per-deck record: slug, label, year, order, function,
                      ancestry(kind), edges, editorial, counts, cover image
PHASE 3  Emit
   3a  tarot/all-decks-many-lenses/grammar.json   (cards + axes, as today,
       but DECKS/CLASS/ANCESTORS dicts come from PHASE 2, and _decks gains
       derives_from / related_to / status per entry)
   3b  tarot/tree-of-tarot/grammar.json           (GENERATED genealogy:
       L1 deck nodes — name, sections from the deck's own description +
       catalog facts, image, derives_from edges, ghost flag for planned;
       L2 branch emergences computed by grouping `order`/`kind`;
       L3 root. Stamped _generated/_do_not_hand_edit like the meta.)
   3c  tarot/_collection.json                     (branches computed from
       order/kind; grammar list from the glob — the 6 missing ancestor
       decks appear automatically; no sibling-repo dependency)
   3d  print-products.json                        (generated JOIN — §4)
   3e  validation report to stdout (counts per projection, dangling refs,
       decks missing print overrides)
```

Idempotent, runs in the existing `build-meta.yml` workflow; the commit step
widens from one file to the four generated artifacts. The hand-authored
editorial prose currently inside `tree-of-tarot`'s item sections (good text!)
is migrated once into each deck's `description` / `catalog.editorial` during
the data pass, then the file is overwritten forever after.

**Migration discipline:** the first generated `tree-of-tarot` should be
diffed against the authored one — every node that disappears must be accounted
for (planned-deck stub created, or consciously dropped) before merging.

---

## 3. The lens contract (unchanged in spirit, now total)

From `MULTI_LENS_PLAN.md`, made binding for every axis the generator emits:

| Axis (emergence node) | `lens` | Renderer |
|---|---|---|
| By Deck | `genealogy` | genealogy-tree (deck-level nodes, drill to cards) |
| By Age | `timeline` | timeline.html (uses `year`, `era` buckets) |
| By Order (A·B·C) | `genealogy` | same renderer, lanes by order |
| By Rank / By Function / By Keyword | `pills` | cards.html pill bar |
| The Tarot (arcana→suit→rank) | `tree` | tree-viewer |

The contract the renderers can now rely on: **every deck node reachable from
an axis carries `slug`, `year`, `order`, `function`, `status`,
`derives_from[]`, `related_to[]`** (via the meta's `_decks` and the generated
tree's item metadata). The genealogy renderer draws `derives_from` solid,
`related_to` dashed, `*_disputed` with a marker, `status != built` as ghosts.
That's the whole interface — any future surface (a radial tree, a map) reads
the same record and needs no new data.

---

## 4. The shop — generated where derivable, manual only where the fact is manual

A product URL at The Game Crafter is a *real-world* fact no generator can
derive. Everything else about the shop currently in `print-products.json`
(which decks exist, card counts, bleed-readiness) **is** derivable — decks
already carry a stamped `print_readiness` block.

So split along that line:

- **`print/products-overrides.json`** (hand-maintained, tiny): `slug →
  { product_url, status_override?, back_image?, note? }`. Only commerce facts.
- **`print-products.json`** (GENERATED): for every `status: built` deck, join
  `print_readiness` (→ `ready_full_bleed` / `ready_bordered` / `web_res`) with
  its override. Decks with no override render as "not yet in shop" instead of
  silently not existing — absence becomes visible, which is the point.

`pages/shop.html` and `print-viewer.html` keep reading `print-products.json`
unchanged.

---

## 5. Before / after — every surface

| Surface | Today | After |
|---|---|---|
| Cards / meta | generated ✅ | generated, deck list from glob (no dict) |
| Genealogy tree | authored `tree-of-tarot` ❌ | same URL, file now generated from `derives_from` |
| Timeline | authored `tree-of-tarot` ❌ | same URL, generated; `year` from catalog |
| Caster | `_decks` ← hardcoded dict ❌ | `_decks` ← glob; all `in_card_pool` decks appear |
| Shop | manual products file ❌ | generated join; overrides only for store URLs |
| `_collection.json` | dead migration script ❌ | emitted by the same generator each build |

One pipeline, five projections, no side-channel a human must remember.

---

## 6. The data pass (the judgment-heavy step — spec, not yet executed)

Stamp `metadata.catalog` on all ~26 deck folders. Proposed values — the
genealogy edges follow the handoff's starter map, with the two debated points
hedged structurally, and Este added as the missing B-order root:

| slug | kind | year | order | function | derives_from | related_to / notes |
|---|---|---|---|---|---|---|
| madiao-money-cards | cousin | ~1400 | – | game | — | `related_to: [mamluk-deck]` — illustrates the Chinese money-card form; a cousin of the transmission, not a documented direct parent (hedge per handoff) |
| mamluk-deck | ancestor | 1375* | – | game | — | the 4-suit pack Europe copied; `year_label` notes the surviving Topkapı deck is c. 1500 |
| ganjifa | cousin | 1550 | – | game | — | `related_to: [mamluk-deck]` |
| visconti-sforza-tarot | tarot | 1451 | C | game | mamluk-deck | |
| cary-yale-visconti-tarot | tarot | 1442 | C | game | mamluk-deck | |
| brera-brambilla *(stub)* | planned/image-blocked | 1445 | C | game | mamluk-deck | ghost node |
| este-tarot | tarot | 1450 | B | game | mamluk-deck | Ferrara root |
| charles-vi-tarot | tarot | 1475 | **B, `order_disputed: true`** | game | mamluk-deck | `order_note`: B (Ferrara) per traditional attribution; recent scholarship argues Florentine A-order. Edge kept generic (to the common trionfi root), not forced through Este. |
| minchiate-florence-tarot | tarot | 1550 | A | game | rosenwald-sheet *(or mamluk-deck if too strong — see open Q1)* | |
| tarocchino-bologna | tarot | 1650 | A | game | mamluk-deck | A-order root line |
| rosenwald-sheet | ancestor | 1500 | A | game | mamluk-deck | Florentine sheet |
| cary-sheet | ancestor | 1500 | C | game | visconti-sforza-tarot | earliest Marseille pattern; `derivation_note` — pattern continuity, not documented workshop descent |
| noblet-tarot | tarot | 1650 | C | game | cary-sheet | oldest complete TdM |
| vieville-tarot | tarot | 1650 | C | game | cary-sheet | Eastern-leaning sibling |
| paris-anonymous-tarot | tarot | 1625 | C | game | cary-sheet | |
| tarot-de-marseille-conver | tarot | 1760 | C | game | noblet-tarot | the printed standard |
| tarot-de-besancon | tarot | 1800 | C | game | tarot-de-marseille-conver | |
| belgian-tarot | tarot | 1780 | C | game | vieville-tarot | Flemish/Eastern branch |
| court-de-gebelin-tarot | tarot | 1781 | occult | origin-myth | tarot-de-marseille-conver | the occult turn |
| etteilla-i-livre-de-thot | tarot | 1788 | occult | divination | court-de-gebelin-tarot | |
| etteilla-ii-egyptian | tarot | 1840 | occult | divination | etteilla-i-livre-de-thot | |
| etteilla-iii-oracle-des-dames | tarot | 1865 | occult | divination | etteilla-i-livre-de-thot | |
| oswald-wirth-tarot | tarot | 1889 | occult | esoteric | court-de-gebelin-tarot | `derivation_note`: via Éliphas Lévi |
| golden-dawn-book-t-tarot | tarot | 1888 | occult | esoteric | court-de-gebelin-tarot | `related_to: [oswald-wirth-tarot, sola-busca-tarot]`; note: parallel English line, not Wirth's child — hedged |
| sola-busca-tarot | tarot (sui generis) | 1491 | – | game | — | `related_to: [golden-dawn-book-t-tarot]` influence on RWS minors |
| mantegna-tarocchi | non-tarot | 1465 | – | game | — | NOT a tarot; excluded from card pool, shown dashed-adjacent in genealogy |
| soprafino / lombardy *(stubs, if intent stands)* | planned | 1835 / 1810 | C | game | tarot-de-marseille-conver | ghost nodes |

This table is the **proposal to verify against `research/*.mdx` during the
data pass**, not settled history. The two flagged-in-handoff judgment calls
are encoded as: Charles VI = `order_disputed`, Ma Diao = `related_to` (cousin)
rather than a `derives_from` ancestor.

---

## 7. Mapping to recursive-eco (the long-term half)

Same spine, Supabase dialect — **normalize at source, materialize for reads**:

1. **Tags at source.** `metadata.catalog` lives inside
   `user_documents.document_data` exactly as in this repo — the vocabulary IS
   the schema; no new tables. (Matches the established inline-JSONB-over-
   relational preference.) `derives_from` references other documents by id or
   slug; for user grammars it doubles as fork/lineage provenance.
2. **Generate on write, not on read.** This repo generates at build time
   because GitHub Pages is static; eco generates at *save* time: a resolve
   step (edge function or queued job) recomputes the affected collection's
   projection document(s) — the same meta/tree shapes, stored as generated
   `user_documents` flagged `_generated: true` and never user-editable. A
   recursive CTE over `derives_from` builds the DAG server-side when needed.
3. **Hot facets get promoted, lazily.** If filtering on `year`/`order` ever
   needs an index: `GENERATED ALWAYS AS (document_data->'metadata'->'catalog'->>'year') STORED`
   — flexible JSONB and an index, no migration of the authoring shape.
4. **Lenses port as-is.** The axis node + `render_as`/`lens` contract is
   already viewer-agnostic; eco's viewers read the same generated projections.
   Folksonomy fits the same pipe: user keywords are just more tags in,
   keyword-emergences out.
5. **The one discipline carries over verbatim:** a projection is never a
   second place to edit the truth.

(Per house rules: eco-side docs commit locally only; this repo pushes freely.)

---

## 8. Build order (each step independently shippable)

1. **Stub + stamp** — write `metadata.catalog` on all deck grammars (the §6
   table, verified against `research/`); create planned-deck stubs. Pure data,
   no behavior change. *The judgment-heavy step; everything after is mechanical.*
2. **`build_catalog.py` phase 1–3a** — port `build_meta_grammar.py` to read
   catalog blocks instead of its dicts; assert the emitted meta is
   functionally identical for the 13 existing decks, then let the glob add the
   rest. Caster heals here for free.
3. **3b generate `tree-of-tarot`** — diff against the authored file; migrate
   any orphaned prose into deck descriptions; commit the generated version.
   Genealogy + timeline heal with zero viewer edits.
4. **3c collection / 3d shop join** — retire `build_tarot_collection.py`;
   add `print/products-overrides.json`.
5. **CI** — widen `build-meta.yml` to run the new script and commit all four
   artifacts; add the validation gate (dangling slug / cycle = red build).

## 9. Open questions (resolve during the data pass)

1. **Minchiate's parent** — Rosenwald-sheet edge vs. a generic A-order root:
   the sheet *evidences* the Florentine pattern but a direct parent claim may
   overreach. Default to root + `related_to: [rosenwald-sheet]` if unsure.
2. **Charles VI edge target** — with `order_disputed`, should its
   `derives_from` point at mamluk-deck (neutral) or este-tarot (commits to
   Ferrara)? Proposed: neutral root + note, so the disputed *order* tag is the
   only place the B-claim lives.
3. **Soprafino / Lombardy** — still wanted? If yes → stubs; if no → they
   simply vanish from the generated tree (correctly).
4. **`tarot/test/`** — delete, or keep with `kind: "meta"` exclusion?
5. **Multi-parent decks** — `derives_from` is an array and the DAG supports
   it; the first genealogy renderer may draw only the primary (index 0) edge
   solid and the rest thin. Decide when a real case appears.
