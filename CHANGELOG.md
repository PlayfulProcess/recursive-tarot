# Changelog

Newest first. One bullet per shipped thing.

## Jul 7 2026

- **Mobile: genealogy graph blank + deck-detail paging.** Two builder-reported phone bugs:
  - **Root cause of the blank genealogy graph (`genealogy.html`)**: the docked `#panel` had a
    fixed `width:330px` with no responsive stacking, so on a 390px phone the `#cy` graph pane was
    squeezed to a ~60px sliver — effectively invisible ("blank white"), independent of whether
    Cytoscape itself loaded. Fixed with a `@media (max-width:720px)` rule that stacks the panel
    *below* the graph and gives `#cy` an explicit `60vh`/`min-height:340px`, plus `cy.resize()` +
    `cy.fit()` on load, `resize`, and `orientationchange` (the classic zero-height-container
    Cytoscape bug, guarded against even though it wasn't the actual trigger here).
  - **Vendored `cytoscape.min.js`** into `public/vendor/` (fetched via `npm pack cytoscape`, MIT,
    v3.34.0) so the graph loads even when the jsdelivr CDN is unreachable — `<script>` tries the
    local copy first, falls back to the CDN via a synchronous `document.write` if it 404s. Added a
    visible in-page error message (`#cy-error`) when neither source loads, so the pane never goes
    silently blank again; the panel/legend degrade to a plain clickable deck list in that case.
  - **Deck-to-deck paging** ("I want to be able to click through the deck") added to three places,
    copying the exact sticky bottom-footer pattern from `viewers/cards.html` (`.modal-nav-footer` /
    `.modal-nav-btn` / `.modal-counter`, ← / "N of M" / →, disabled at the ends): the genealogy
    graph's node-detail panel, the timeline viewer's deck-detail panel (`viewers/timeline.html`),
    and the tree-of-tarot node-detail popup (`viewers/genealogy-tree.html`). Arrow keys page too.
  - **Visible top-right X close**, dark chip + white glyph (matching `cards.html`'s `.modal-close`),
    added/upgraded on `viewers/timeline.html` and `viewers/genealogy-tree.html`'s detail popups —
    the old plain floated `×` was hard to see over light panels.
  - **Bonus mobile fix, same two files**: `.wrap{height:calc(100vh - 52px)}` assumed a 52px
    `<site-header>`, but the real custom element renders ~122px tall — the mismatch made `.wrap`
    (and the sticky footer inside it) overflow past the bottom of the viewport. Replaced the
    hardcoded guess with a `fitWrap()` that measures the real header height and reapplies it on
    resize/orientationchange.

## Jul 6 2026

- **Fixed header dropdowns cropping off the left edge on tablet widths** — `.dd-menu` was
  right-anchored (`right:0`) with only a `max-width:760px` media-query rescue, so a left-side
  trigger (Home, Views) rendered its panel partly off-screen at ~760–950px viewports (iPad
  portrait, split-screen laptops) — the fixed breakpoint simply didn't cover that range.
  Replaced the breakpoint hack with a `positionMenu()` JS calc in `site-header.js` that measures
  the real trigger + panel on every open (hover, focus, and touch-tap) and clamps left/top so
  the panel stays fully on-screen at any width, plus an internal-scroll cap for tall panels and
  a resize/orientation listener. Verified overflow-free from 320px to 1440px.

- **The book ("The Recursive Tarot") — accuracy & rendering pass (Opus session):**
  - **Courses render from the local `course/` directory** — `pages/course-viewer.html` loads the
    in-app `course/*.mdx` as the single source of truth, so the book and its prose live in this repo.
  - **Canonical `minor_key` for the Minor Arcana** — `scripts/add_minor_keys.py` writes a canonical
    key (e.g. `four-of-coins`, `knight-of-cups`) onto every minor item, parity with the majors'
    `trump_key`; maps all suit/court name variants, idempotent, fails loud on intra-deck collisions.
    Applied across 26 decks (548 items → 63 keys = the standard 56 + Cary-Yale's 7 extra female
    courts, kept distinct). The course pip/suit detail now groups by it (court duplication 77 → 56).
  - **"The Numbers"** — `scripts/analyze_numbers.py` reproducibly answers "does a number mean the
    same across suits?" from the grammars (Ace→Kether … Ten→Malkuth, one Sephirah per number, zero
    inconsistencies); `research/synthesis/numbers.json` synthesis + a `data-embed="numbers"` section.
  - **Trump/pip detail rebuilt** — per-deck Scene with image thumbnails + a synthesis overview;
    pips as blocks with a rank-number badge + representative image.
  - **Plates → the Death card across the centuries** (Visconti-Sforza 1451 → Marseille 1760 → RWS
    1909); corrected a wrong caption (Cary-Yale was a standing harvester, not a "mounted archer").
  - **Card strips → responsive grid** (all cards visible at once; 2-col in print) with Explorer-style
    hover-zoom; **left sidebar scrolls independently**; **de-duplicated the Four-Suits intro**.
  - **Home page** features the book (start-here card + history-section link), corrects "26 → 25
    decks", and wires the course links to explicit `?course=` params.
  - **Citations** — Jessica Dore's Tower-as-radical-acceptance reading linked to *Tarot for Change*;
    credential corrected "licensed therapist" → "licensed social worker".
  - Remaining agreed work captured in `plan/BOOK-VIEWER-NEXT.md` (tree/timeline light mode +
    hover-both + no-scroll, plates redesign, section re-ordering, per-deck people, playable game).

## Jun 13 2026

- **Accuracy & research drive (Opus session)** — a long pass to make every deck as historically
  precise as possible and reference every claim:
  - **Research catalogue** (`research/SCHEMA.md` + `bibliography.bib`, ~290 sources): a
    **deck dossier + card-by-card dossier for all ~25 decks** (`research/decks/`, `research/cards/`),
    every load-bearing claim cited `[@key]`, confidence-flagged. Dossiers are the source of truth.
  - **People & Institutions of Tarot** — new grammar `tarot/people-of-tarot/grammar.json`,
    **generated** from **23 people dossiers** (`research/people/`) by `scripts/build_people_grammar.py`
    (5 groups: makers/patrons/occultists/scholars/institutions). Pamela Colman Smith linked to RWS
    pip cards; Mantegna & Gringonneur as debunked attributions. Registered in `_collection.json`.
  - **471 cards enriched** with sourced "Research note" sections (`scripts/enrich_cards_from_research.py`,
    ADD-only/idempotent) — the per-card "what changed vs. its parent" deltas + citations.
  - **Corrections + 5 editorial calls applied** (`plan/CORRECTIONS-to-apply.md`): Etteilla card
    identities (13→Lovers, 21→Chariot, 78→Fool) and **removal of anachronistic RWS pip-symbol
    metadata** from the 3 Etteilla decks; Wirth Hebrew letters; Visconti Judgement→Bembo; Gébelin
    Mellet re-attribution; Viéville+Belgian re-tagged Rouen-Brussels/Belgian (not Marseille);
    Charles VI→Florentine attribution; Paris-Anonymous→Tarot de Paris; Minchiate Papi identities;
    Cary-Yale distinct court archetypes; Noblet→"near-complete".
  - **Mamluk image honesty** — flagged that we hold 7 of ~48 surviving Topkapı cards (shown as
    representatives); full set TODO needs image access.
  - **deck-picker** now **orders decks by year** with the year shown in parentheses
    (`scripts/refresh_collection.py` curates `year`/`year_label`; `viewers/deck-picker.js`).
  - `scripts/check_all.py` gates every change (JSON valid · no dangling refs · meta/people rebuild).
- **P5 step 5: dynamic lane/hub grouping** — Timeline "Lane:" dropdown + genealogy-tree "Hub color:" dropdown; both use `DimensionEngine.discoverFields()` over deck metadata so any discovered field (century, branch, tradition…) drives lane/color; `<view-switcher>` removed from grammar-level pages
- **P5 step 4: dimension chip tray in cards** — multi-deck mode shows draggable DimensionEngine chips above sidebar; drag or click to group cards by any field; `#groupby=field` hash serialized so view-switcher carries the active grouping into explorer (`#{rows:[field]}`)
- **P5 step 3: deck-picker.js + cards multiselect** — shared `DeckPicker.open()` popover; cards.html gets "✦ Decks ▾" button + `?decks=a,b` multi-deck mode; sidebar groups by deck, filter pills become deck pills; `view-switcher.js v=8` carries `decks` param
- **P5 step 2: dimension-engine.js extracted** — pure DOM-free module (`flatten/discoverFields/inferHierarchy/groupBy/passes/vals/smartCmp`); explorer binds thin wrappers, verified identical output
- **P5 step 1: explorer quick wins** — +N badge expands cell in place; multiselect hint; AI balloon logged-out message; Opus session Jun 12
- **Logo: recursive-logo.svg added** — purple Archimedean spiral (copied from flow app) with white circular backdrop in site-header for dark header contrast; `site-header.js?v=10`
- **AI balloon: logged-out prompt** — cards.html + tree-viewer show "Sign in ↗" message instead of blank iframe when user is not authenticated
- **TGC: sampler v6 shipped** — v6 deck E25631D6 (33 cards, Dodal 1701 back) proofed; stale draft decks v2/v3/v4 removed; diagnostic scripts added to `scripts/`

## Jun 12 2026

- **S3: 6 hidden ancestor decks surfaced** — mamluk-deck, ganjifa, sola-busca-tarot, noblet-tarot, cary-sheet, rosenwald-sheet added to `_collection.json`; new "ancestors" branch; collection 20 → 26 decks
- **S4: Explorer wired into homepage** — "⊞ Explorer" card added to the "More ways in" grid on index.html (header + view-switcher already had it)
- **S5: Shop expanded** — vieville-tarot and paris-anonymous-tarot (both 78/78 print-ready, 94%) added to print-products.json as coming-soon entries
- **S6: favicon + og tags** — gold spiral SVG favicon + og:title/description/url on index.html
- **Plan: Fruits of the Tree** — integration ladder doc (L0–L4 tree↔fruit identity/AI/data/commerce) pushed by Fable session
- **POD: print masters re-baked** — vieville 78/78, paris 78/78, este 16/16, mantegna 50/50 print-ready (Gallica/Yale high-res)
- **Explorer: branch colour fix** — Belgian pill colour restored (order→branch→violet fallback)
- **Explorer: emergence pills surface first** — pills label the cell; cards shown behind +N count

## Jun 11 2026

- **Explorer v2** — trace ⬆⬇ relationships, branch-coloured level-gradient pills, deck multiselect
- **Explorer v1** — drag-drop pivot over the full card collection (Emergence Explorer); design doc + delegation plan
- **Header: views vs tools** — nav reorganised into ◫ views group (Cards, Explorer, Tree of Life, Timeline, Tree, Genealogy) + tools group (Caster, Course, Shop, GitHub)
- **Genealogy re-architecture plan** — keyword-in / emergence-out engine; derives_from edge map; Supabase/webhook runtime design (HANDOFF-rearchitect-genealogy.md)
- **Sampler v5** — density content-crop (TIGHT_TRIM) for wide-margin cream-stock decks; always re-process from source
- **DRY: BLEND_FRAME** moved into tgc_card.py — deck-product bakes match the sampler automatically
- **Sampler: frame-blend mode** — corner-sampled bleed for 7 cream-stock decks; eliminates white/black contour seam

## Jun 10 2026

- **Shop: Full Sampler v5 pushed to TGC** (deck ED62C786) — ready to proof
- **R2: 7 card backs rehosted** — stable URLs, no more Commons 429 on backs
- **Sampler: 19 decks covered** + high-res re-pull for Gallica/Yale decks
- **Webhook: Supabase←GitHub live** — grammar changes reindex Supabase automatically
- **Docs: EMERGENCES.md** — cataloguing model (keywords in, emergences out)

## Earlier (Jun 2026)

- Anonymous Parisian Tarot de Marseille (BnF, 17th–18th c.) — 78 cards
- d'Este Tarocchi (Ferrara, c.1450) — 16 cards via Yale Beinecke
- Belgian/Vandenborre Tarot Flamand (Brussels, c.1780) — 22 majors
- Jacques Viéville Tarot (Paris, c.1650) — 78 cards from BnF/Gallica
- Ma Diao Chinese money-suited cards — 12 Skokloster survivors
- Shop page + TGC API upload flow proven
- Course-viewer ported from recursive.eco
- Print-viewer (Grid / Booklet / Memory / Storyboard / Story layouts)
- Caster: Import cast (load exported .json, re-render spread)
- Timeline: proportional time axis + branch lanes
