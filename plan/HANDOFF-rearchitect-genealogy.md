# Handoff — Re-architect cataloguing & genealogy (keyword-driven, cross-repo)

*Paste the prompt below into a fresh Fable or Opus session. The findings + starter
edge-map underneath save the new session the discovery work.*

---

## THE PROMPT (paste this)

> **Re-architect cataloguing & genealogy as generated, keyword-driven projections — for recursive-tarot now, recursive-eco long-term.**
>
> First read, in `recursive-tarot/`: `EMERGENCES.md` (the cataloguing model + the "keywords in, emergences out" section), `scripts/build_meta_grammar.py` (the working generator), `MULTI_LENS_PLAN.md` (lenses), and skim `tarot/_collection.json` + a couple of `tarot/<slug>/grammar.json`.
>
> **Problem:** only the Cards viewer (reads `_collection.json` + the auto-rebuilt meta) reflects the real ~20-deck library. The **genealogy tree, timeline, caster, and shop** read hand-maintained sources (`tarot/tree-of-tarot/grammar.json`, hardcoded deck lists, `print-products.json`) and have drifted — the genealogy advertises *unbuilt* decks (Soprafino, Lombardy) and *misses built* ones (Viéville, Paris, Ma Diao).
>
> **Goal:** one cataloguing architecture where every catalogue surface is a **generated projection that cannot drift**, driven by lightweight **leaf-level keywords/tags** (not hand-maintained `composite_of`), rendered consistently via **shared lenses**, and general enough to also serve recursive-eco's user-created grammars.
>
> **Design direction (refine, don't obey blindly):** *keywords in, emergences out.* Each deck/card carries tags — `order` (A/B/C/occult), `year`, `suit`, `rank`, `function`, and a relational `derives_from` (parent slug). Every axis, including the genealogy DAG, is **computed** from those tags; the genealogy is built from the `derives_from` edges so it always matches the real decks. A small lens set (`render_as`: pill-group / timeline / genealogy-graph / radial-tree) renders each axis identically everywhere.
>
> **Deliverables:**
> 1. `plan/REARCHITECT-GENEALOGY.md` — the shared tag vocabulary, the generation pipeline, the lens contract, and how it maps to recursive-eco's Supabase model (normalize tags at source, materialize projections for reads).
> 2. The prerequisite data pass: add `derives_from` and confirm `order`/`year` on every recursive-tarot deck grammar (**the one judgment-heavy step** — get the genealogy edges historically right; hedge debated ones, e.g. Charles VI's A-vs-B order).
> 3. A generator (extend/replace `build_meta_grammar.py`) that **emits `tree-of-tarot` + timeline data from the deck tags**.
> 4. Repoint timeline, genealogy-tree, caster, and shop at the generated data / `_collection.json`.
>
> **Constraints:** recursive-tarot is a static GitHub Pages site — generate at build time. Deck grammars are the single source of truth; never hand-edit generated files. House style: hedge debated claims, invite correction. Push recursive-tarot freely; recursive-eco docs commit locally only.

---

## Runtime sync — the builder's design (carry into recursive-eco)

The static-site generator (above) keeps recursive-tarot coherent. For **recursive-eco**
the builder wants the *same* idea but live, driven by data not a build step:

```
GitHub main (deck grammars = source of truth)
      │  push webhook
      ▼
Supabase  (decks + leaf tags ingested; the normalized read store)
      │  query (keyword → emergence rules)
      ▼
recursive-eco  (generates By-Order / By-Age / genealogy / timeline views
                AUTONOMOUSLY from Supabase — never hand-maintained)
```

So: **GitHub is the truth, a webhook syncs it into Supabase on every push, and
recursive-eco computes the emergent views from Supabase at request time** (or
materializes them on the webhook). This is the *same* "keywords in, emergences out,
materialize for reads" model — just with Supabase as the materialization layer and a
webhook as the freshness trigger. The tarot decks become one data source feeding it;
user-created grammars in recursive-eco feed the same pipeline. Design the tag schema
and the generation rules so BOTH repos share them.

## Live findings (June 11 2026 — what's stale)

| Surface | Reads | State |
|---|---|---|
| Cards / meta (Group-by, lenses) | `_collection.json` + auto-rebuilt meta | ✅ current |
| Shop | `print-products.json` (manual) | ❌ 8 products; missing 12 decks |
| Timeline | `tree-of-tarot` | ❌ missing Viéville, Paris, Ma Diao |
| Genealogy tree | `tree-of-tarot` | ❌ shows unbuilt (Brera, Soprafino, Lombardy); misses Viéville, Paris, Ma Diao |
| Caster | hard-coded list | ❌ 14 decks; missing the 5 new |

Root cause: one self-updating pipeline (collection → meta → Cards viewer) + several hand-maintained side-channels nobody re-ran.

Also pending: the 6 ancestor decks built but NOT in `_collection.json` (mamluk, ganjifa, sola-busca, noblet, cary-sheet, rosenwald) — surface them in the collection so they appear everywhere.

## Starter `derives_from` edge-map (verify + hedge; the judgment-heavy step)

Ancestry (deep roots, not direct parents): **ma-diao** → (Chinese money-card form) → **mamluk-deck** (the 4-suit pack Europe copied) · **ganjifa** (Islamic cousin).

```
mamluk-deck            -> (none; upstream root)
visconti-sforza        -> mamluk-deck        (Milan, C-order root)
cary-yale-visconti     -> mamluk-deck        (Milan, root, ~1442)
deck:brera-brambilla   -> mamluk-deck        (Milan, root) [UNBUILT - image-blocked]
este-tarot             -> mamluk-deck        (Ferrara, B-order root, c.1450)
charles-vi-tarot       -> ???                (B *or* A order — DEBATED, hedge)
minchiate-florence     -> (Florence, A-order)
tarocchino-bologna     -> (Bologna, A-order)
cary-sheet             -> visconti-sforza    (earliest Marseille pattern, c.1500)
noblet-tarot           -> cary-sheet         (oldest complete TdM, Paris 1650)
vieville-tarot         -> cary-sheet         (Paris ~1650, Eastern-leaning sibling)
paris-anonymous-tarot  -> cary-sheet         (Paris 1600-1650, C-order sibling)
tarot-de-marseille-conver -> noblet-tarot    (the printed standard, 1760)
tarot-de-besancon      -> tarot-de-marseille-conver  (Swiss/Protestant variant)
belgian-tarot          -> vieville-tarot      (Flemish/Eastern branch, c.1780)
court-de-gebelin-tarot -> tarot-de-marseille-conver  (the occult turn, 1781)
etteilla-i-livre-de-thot -> court-de-gebelin-tarot   (first divination deck, 1788)
etteilla-ii / iii      -> etteilla-i-livre-de-thot
oswald-wirth-tarot     -> court-de-gebelin-tarot (via Lévi, 1889)
golden-dawn-book-t     -> oswald-wirth-tarot? / occult line (1888-1909, RWS)
sola-busca-tarot       -> (sui generis, 1491; influenced RWS minors)
mantegna-tarocchi      -> (sui generis; NOT a tarot)
rosenwald-sheet        -> (Florence A-order, c.1500)
```

The two genuinely debated edges to flag, not assert: **Charles VI's order family** (A vs B) and whether **Ma Diao** is a "deep root" vs a true ancestor (it's a cousin/illustration of the form, not a direct line).
