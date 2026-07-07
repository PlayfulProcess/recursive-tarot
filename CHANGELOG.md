# Changelog

Newest first. One bullet per shipped thing.

## Jul 7 2026 (3)

- **Grounded "tarot does not predict" in citable scientific literature**, builder's request
  ("research to base the claim... scientific papers etc."):
  - **New dossier** `research/why-tarot-works/does-tarot-predict.md` — direct controlled tests of
    tarot itself (Blackmore 1983, *JSPR*: subjects couldn't rank their own reading above chance in
    2 of 3 experiments, honestly flagging Markwick's 1988 reanalysis that found the first
    experiment held up; Ivtzan & French 2004 conference proceedings: real vs. random-card control
    readings indistinguishable, including to tarot believers); the Barnum/Forer + cold-reading
    mechanism (Forer 1949; Dickson & Kelly 1985; Hyman 1977); the broader precognition claim tested
    at scale and its collapse (Bem 2011 *Feeling the Future* → failed replication by Ritchie,
    Wiseman & French 2012 *PLoS ONE* and Galak et al. 2012, effect size d=0.04 across 3,289
    subjects); the contested ganzfeld meta-analysis (Milton & Wiseman 1999, with Storm & Ertel's
    2001 dispute noted rather than hidden); the unclaimed Randi Million Dollar Paranormal
    Challenge (retired 2015, zero passes); and, as an adjacent design, Carlson's 1985 *Nature*
    double-blind astrology test (also contested — Ertel 2009 reanalysis flagged). On the "ways it
    can help" side: Hobson et al. 2018 (ritual/anxiety review), Norton & Gino 2014 (ritual/grief,
    cited with an explicit caveat about Gino's separate retracted papers), Moore 1957 (Naskapi
    scapulimancy as randomizer, with its game-conservation hypothesis's later critique noted),
    Levitt 2021 (coin-toss major-life-decisions study), Evans-Pritchard 1937 (Azande poison
    oracle as decision-procedure), Pennebaker & Beall 1986 (expressive writing).
  - **One source found and deliberately excluded**: Brooks et al. 2016 "Don't Stop Believing:
    Rituals Improve Performance by Decreasing Anxiety" — **retracted November 2024** after the
    author team's own data audit found irreconcilable anomalies and they could not produce raw
    data for two studies. Not cited anywhere in the dossier or the course; the ritual/anxiety claim
    is grounded in the independent Hobson et al. 2018 review instead.
  - **Added 18 new entries to `research/bibliography.bib`** (new section, keys `blackmore1983`
    through `nortongino2014`) — every entry independently confirmed to exist (title/authors/venue/
    year + stable link or DOI) before being added, per the file's own header rule. Not written into
    the dossier as `[@key]` — that's the people/decks/cards convention; `why-tarot-works/` uses
    plain inline links, which this dossier follows. The bibkeys exist so the sources land in the
    one master bibliography and are picked up by the generated book's bibliography section.
  - **Wove citations into `course/how-tarot-works.mdx`** — light touch, no restructuring: "The thing
    the cards cannot do" now opens with the Blackmore + Ivtzan/French direct tests before the
    Barnum-Forer bullet list, the Barnum bullet gains the Forer/Dickson-Kelly/Hyman citations and
    names cold reading explicitly, and a new bullet covers the Bem replication collapse + the Randi
    prize. "Some of the ways a reading can help" gains one supporting citation per mechanism:
    re-narration → Pennebaker & Beall; productive randomness → Moore + Levitt; ritual → Hobson et
    al. The "Sources & honesty" footer now points to the new dossier and its excluded-sources note.
  - **Regenerated mirrors**: `scripts/course_to_grammar.py` for `how-tarot-works` and
    `reading-the-cards`, `scripts/build_reading_course.py` (recompiles the anthology from the live
    chapter files), and `scripts/build_meta_grammar.py`. `scripts/check_all.py` passes (55
    grammars, dangling=0).

## Jul 7 2026 (2)

- **Editorial rewrite of "How the Cards Can Work"** (`course/how-tarot-works.mdx`), builder's direction:
  - **Deleted** the "honest engine room of the series" tagline (frontmatter description) and the
    body line "This page is the engine room... runs on the four small machines described here" —
    the course no longer claims to be the sole authoritative account of how tarot works.
  - **Rewrote the opening.** Dropped the "two questions people ask of tarot" frame entirely. New
    frame: life (and the sun) is already mysterious and magical enough; tarot is no more magical
    than life, or art, or human imagination — and that's magic enough — looping straight into "the
    light of the tarot is in the eyes of the beholder" and into Tolkien.
  - **De-enumerated "the four ways it can work."** Renamed "The four reasons a reading can still
    genuinely help" → "Some of the ways a reading can help"; dropped the 1/2/3/4 numbering and the
    "four machines" language throughout (including in "The catch that decides the stance" and
    "Where this leaves us").
  - **Moved Tolkien to the front and expanded to all four functions of fantasy** — Fantasy
    (sub-creation), Recovery, Escape, and Consolation/eucatastrophe (previously only Recovery was
    covered, and only in the closing section). New section order: Tolkien's functions of fiction →
    Mythopoeia/C.S. Lewis → the honest disclaimer (no evidence for prediction) → the psychological
    mechanisms (projection, re-narration, productive randomness, ritual) → the gate-stance catch →
    the palantír warning → anthropological close (divination-traditions pointer) → the closing loop.
  - **New "Mythopoeia" section**: quotes the poem's disenchantment/re-enchantment opening verbatim
    (the "trees are 'trees'" passage — including the word *divination* inside Tolkien's own poem),
    links *[On Fairy-stories](https://coolcalvary.com/wp-content/uploads/2018/10/on-fairy-stories1.pdf)*
    and *[Mythopoeia](https://www.tolkien.ro/text/JRR%20Tolkien%20-%20Mythopoeia.pdf)*, and
    contextualizes the 1931 Addison's Walk conversation with C.S. Lewis and his conversion
    (linking *[The Most Reluctant Convert](https://cslewismovie.com/)*) — framed honestly as
    showing the idea's pedigree, not as a religious claim.
  - **Kept the closing image** ("the light of the tarot is in the eyes of the beholder") as the
    course's close, now explicitly calling back to the new opening so the chapter reads as one loop.
  - Regenerated `tarot/how-tarot-works-course/grammar.json` via `scripts/course_to_grammar.py`.
  - **Fixed a stale path bug in `scripts/build_reading_course.py`** (it pointed at `books/...`
    instead of `course/books/...` after an earlier repo-tidy move the script was never updated
    for) and reran it — this also caught up `course/reading-the-cards.mdx` (the compiled
    practitioner course) with edits made to `intention-setting.mdx` and `kant-and-the-tarot.mdx` in
    earlier sessions that had never been mirrored in, plus this round's how-tarot-works edits.
    Regenerated `tarot/reading-the-cards-course/grammar.json` to match.

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
- **Editorial pass on the voice courses + a mobile course-viewer rendering fix:**
  - **"The Light of Tarot" folded into "How the Cards Can Work"** (`course/how-tarot-works.mdx`) —
    added a closing section, "Sub-creation — why the pictures are enough" (Tolkien's sub-creation
    and Recovery, the Murray/Holmes/Griffin idealization study), ending on "the light of the tarot
    is in the eyes of the beholder." The standalone `course/the-light-of-tarot.mdx` is now a stub
    that points to the merged section (kept only so old links resolve); removed from the site nav
    (`site-header.js`), replaced there with "How the Cards Can Work."
  - **Retitled the two voice courses to open questions** — "Kant Reads the Tarot" → **"How Could
    Kant Read the Tarot?"** and "Marsha Linehan Reads the Tarot" → **"How Could Marsha Linehan
    Read the Tarot?"** (frontmatter, H1, and every cross-reference across `course/*.mdx` and
    `course/books/how-to-read-the-cards/book.json`). File ids/slugs unchanged, so URLs still work.
  - **Kant course** (`course/kant-and-the-tarot.mdx`): pulled the Kant/tarot-divination exact-
    contemporaneity argument (Etteilla 1785–91 vs. the *Groundwork* 1785) to the very front — the
    frontmatter `description` and the opening paragraph now state it plainly as the license for
    the whole imagined encounter, before the Königsberg vignette. Trimmed the repeated "make
    meaning yourself, hold it lightly, hand it on" refrain (appeared near-verbatim twice in the
    closing sections) to a single instance, and closed the course on the same "light of the tarot
    is in the eyes of the beholder" image as the merged how-tarot-works chapter.
  - Regenerated the `_generated` `tarot/*-course/grammar.json` mirrors (`scripts/course_to_grammar.py`)
    for every touched course so they stay in sync with their source `.mdx`.
  - **Fixed: mobile course-viewer Contents drawer let cropped page content show through.**
    `pages/course-viewer.html`'s mobile TOC drawer only dims the page 50% (`.mobile-toc-overlay`);
    the content column behind it doesn't resize when the drawer opens, so the sliver not covered
    by the 80%-wide drawer panel showed legible, mid-word fragments of the hero title and body
    text — read as broken/cropped rather than an intentional dimmed backdrop. Bumped the overlay
    to near-opaque (`rgba(17,24,39,0.98)`) and locked background scroll while the drawer is open.
    Verified pixel-level with Playwright at 390×844 (before/after RGB sampling through the overlay).
    Checked separately for the reported "text clipped at the right edge with the drawer closed" —
    already fixed by the existing `overflow-wrap: anywhere` rules; not reproducible.

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
