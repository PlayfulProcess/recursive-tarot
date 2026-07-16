# Changelog

Newest first. One bullet per shipped thing.

## Jul 16 2026

- **Spread Caster (`viewers/caster-studio.html`): split "Clear all", added spread send/receive
  with recursive.eco, and embedded the shared assistant.** Three builder-requested changes plus
  the assistant embed:
  - **Split "Clear all" into two buttons.** New **Clear casting** drops the drawn cards but KEEPS
    the spread (layout, positions, labels, meanings) so you can re-cast into the same shape;
    **Clear all** keeps its old behaviour (wipes everything, layout included). Same ghost-button
    styling.
  - **Send / receive spreads ↔ recursive.eco (the pinned spread contract).** New paper-plane
    **Send to recursive.eco** icon next to Export/Import encodes the current spread as the pinned
    wire format — `base64url(JSON)` of `{ v:1, name, positions:[{label, meaning?, x?, y?}] }`,
    x/y as 0–1 canvas fractions, capped at 15 positions — and opens
    `https://flow.recursive.eco/?importSpread=<enc>` in a new tab, where the app saves it into the
    user's My Spreads. The `?spread=<base64url contract>` receiver (how the app's "Fine-tune in the
    builder" links arrive) now decodes and loads onto the canvas + into the editors ready for
    fine-tuning; it's tolerant of missing `v`/`name`/`meaning`/`x`/`y` and preserves unknown extra
    fields.
  - **Existing file import/export kept — tolerant reader, strict writer.** The file Import still
    reads the legacy `{_type,_version,positions:[{n,…}]}` shape (and full readings with cards);
    the file Export now emits the contract shape (`{v:1,name,positions:[{label,meaning,x,y}]}`,
    plus a tolerated `description` for presets), so everything written from here going forward is
    contract-shaped.
  - **Embedded the ONE recursive.eco assistant on the page.** Added the shared sparkle-star
    launcher (`assistant.js` → the flow `/assistant` collapsible sidebar) to the Caster, and
    upgraded `assistant.js` so a page can declare its embed context via
    `<body data-assistant-context="…">` — the Caster passes `context=spread-builder` so the flow
    side knows where it's hosted (other pages that include `assistant.js` are unchanged). The page
    listens for `{ type:'eco-spread', spread:<contract obj> }` postMessages from the flow origin
    (origin-checked) and loads the AI-built spread onto the board live — no navigation, no reload.
    ONE `loadSpreadContract()` loader backs both the `?spread=` URL receiver and the postMessage
    channel. Site-wide rollout of the assistant to every open-site page (via a shared include) is
    the noted follow-up — deferred here to avoid double-mounting on the ~9 pages that already carry
    `assistant.js`.
  - **Verified** in headless Chromium (served over `python3 -m http.server`): 3-position spread →
    Cast fills all 3 → Clear casting keeps the 3 positions with cards gone → Clear all empties the
    board; reload with `?spread=<sample>` renders the positions/labels (incl. a position with no
    meaning + an unknown extra field, both tolerated); Send to recursive.eco opens the exact
    `flow.recursive.eco/?importSpread=` URL decoding back to the contract; an `eco-spread`
    postMessage from `https://flow.recursive.eco` loads 4 positions live while the same message
    from a wrong origin is ignored. The shared launcher's star FAB itself couldn't be exercised in
    the sandbox (no route to `recursive.eco/js/assistant-launcher.js`) — that half is wired by
    reading the existing pattern, not live-tested here.

## Jul 12 2026

- **Fixed: the AI assistant button was completely invisible on `viewers/cards.html` and
  `viewers/tree-viewer.html`.** Builder reported "ai icons in tarot are not uniform" from a
  screenshot; investigation found the real bug was worse than a style mismatch — both
  pages' `#assistant-toggle` button carried an inline `style="display:none;"` with no JS
  anywhere in either file that ever removed it, so the button never rendered at all (only
  `pages/course-viewer.html`'s matching button was visible). Removed the dead `display:none`
  from both. While in there: (1) their `.assistant-toggle` `box-shadow` was still the old
  amber/gold `rgba(154,115,34,0.4)` left over from *before* the Jul 7 2026 purple→plum
  recolor (commit `8bda0dc`) — `course-viewer.html` got the matching plum shadow
  (`rgba(95,42,76,0.45)`) in that commit but the other two were missed; brought them in
  line. (2) None of the three manual buttons/panels had the Jul 9 2026 z-index fix that
  `assistant.js`'s shared shell got (`.rec-assistant-shell` forced to `2147483000` because
  this site's sticky `site-header.js` is `z-index:50` and auto-reveals on scroll-up,
  painting over anything lower) — the three manual `.assistant-toggle` /
  `.assistant-frame-container` rules were still `z-index:40`, so the same header-covers-panel
  bug could hit them. Bumped all three to `2147483000` to match. Net effect: all three
  manual-iframe pages now render an identical, always-visible plum sparkle FAB (same glyph,
  size, color, position, stacking) — internally consistent with each other. Did **not**
  attempt to pixel-match the shared `assistant.js` pattern's actual FAB (the flow app's
  `AssistantRail`: a transparent purple-ring circle with a context-specific glyph overlay,
  confirmed by reading `apps/flow/src/components/shared/AssistantRail.tsx` +
  `icons.tsx` in the private app repo) — that pattern lives inside a cross-origin iframe on
  the shared-script pages (can't be restyled from here regardless), and recoloring these
  three back toward the app's purple would undo the Jul 7 2026 builder-approved plum
  recolor (chosen specifically to stop a gold+neon-violet clash). Flagging this as a
  deliberate scope call, not an oversight — the shape family (four-point sparkle) already
  matches; only the ring-vs-solid-fill treatment and the purple-vs-plum hue differ, and
  changing those needs a real design proposal + green light, not a quiet fix.
  Verified locally: served the repo over `python3 -m http.server`, screenshotted all three
  fixed pages plus two `assistant.js` pages (`index.html`, `deck.html`) via headless
  Chromium at desktop (1280×900) and mobile (390×844) widths. Confirmed the button now
  appears (previously blank) on `cards.html`/`tree-viewer.html`, matches `course-viewer.html`
  pixel-for-pixel, and sits clear of the header at both widths. Could **not** verify parity
  against the actual shared-script FAB — this sandbox has no route to `recursive.eco`, so
  `assistant-launcher.js` never loads and `index.html`/`deck.html` show no assistant icon at
  all in the screenshots (expected sandbox limitation, not a site bug).
- **New sitewide `assistant.js` — the ONE shared recursive.eco assistant sidebar, finally
  on this repo too.** This is the pattern source that `recursive-astrology/assistant.js`
  was modeled on (its header comment says so), but recursive-tarot itself never had the
  equivalent file — this repo instead had two older, page-specific patterns. `assistant.js`
  loads the shared shell (`https://recursive.eco/js/assistant-launcher.js`), which iframes
  the flow app's `/assistant` embed — the exact same star FAB and tabbed sidebar (Chat ·
  Tarot · I Ching · Astro · Story) every recursive.eco page mounts, with auth carrying
  because tarot.recursive.eco is a `.recursive.eco` subdomain. Included on `index.html`,
  `deck.html`, `genealogy.html`, `pages/course.html`, and `pages/print-viewer.html`
  (following astro's placement pattern: right after the `site-footer.js` include). Carries
  over astro's Jul 9 2026 z-index fix (`.rec-assistant-shell` forced above this site's own
  sticky `site-header.js`, which shares the identical z-index:50/auto-hide-reveal pattern).
- **Retired the hand-rolled `viewers/course-assistant.js` chat widget** (own shadow-DOM UI,
  own direct `fetch()` to `flow.recursive.eco/api/ai/chat`, in-memory-only conversation —
  no persistence, no personality picker, no tabs, gold/cream theme instead of the platform
  purple). `viewers/grammar-course.html` now includes the shared `assistant.js` instead
  (dropped the `<script src="course-assistant.js?v=2">` include, added `../assistant.js`
  next to its `site-footer.js` include). Confirmed zero remaining references to
  `course-assistant.js` anywhere in the repo and deleted the file.
- **Not touched (functional, lower priority):** `viewers/cards.html`, `viewers/tree-viewer.html`,
  and `pages/course-viewer.html` already reach the real assistant via their own inline
  `iframe.src = getFlowBaseUrl() + '/assistant?grammar_id=...&context=...'` construction —
  these pass real per-page context (`study`/`tree`/`cards`) the generic script doesn't
  replicate. Left as a follow-up candidate, not consolidated this round.

## Jul 11 2026

- **Meta-deck source-card resolution ported to the tarot site's own viewers** (new
  `viewers/reference-resolve.js`, edits to `viewers/cards.html`,
  `viewers/caster-studio.html`, `viewers/tree-viewer.html`). Mirrors the private app's
  `ref_document_id`/`ref_item_id` resolution (built for the "All Decks, Many Lenses"
  meta-grammar): a card that carries `metadata.source_deck` + `metadata.source_item_id`
  now renders its OWN content (e.g. the "Origin" provenance blurb) PLUS an additive
  "From &lt;source deck&gt;" panel with the source card's own keywords/sections, resolved
  by fetching that deck's `tarot/<slug>/grammar.json` directly from the repo — no backend,
  no Supabase call, fully static. Applied to the card-detail modal (`cards.html`, the
  default viewer for the meta deck), the Spread Caster's drawn-card detail
  (`caster-studio.html`), and the tree node detail (`tree-viewer.html`). Verified all 768
  meta-deck card items resolve cleanly (0 dangling `source_deck`/`source_item_id`
  references) and exercised the resolver's fetch/cache/error paths against the real served
  repo data.

- **Docs consolidation: `GRAMMAR_FORMAT.md` re-synced from the canonical
  `recursive.eco-schemas` copy, and standardized as a mirror.** The canonical
  `recursive.eco-schemas/GRAMMAR_FORMAT.md` gained three previously-undocumented,
  already-shipped fields: `ref_item_id` (a reference item pointing at one specific
  item inside another grammar, not the whole document — the "All Decks, Many
  Lenses" tarot meta-grammar pattern), `performance.words` (per-word karaoke
  timing for audio-narration grammars), and `_category_roles`/`_section_roles`
  (custom astrology category/section-name mapping). This repo's copy is now
  byte-synced to that extended version and carries a standardized header note:
  *"Mirrored copy — canonical version lives in recursive.eco-schemas; if they
  differ, that one wins."* Also updated the `GRAMMAR_FORMAT.md` row in the docs
  map above and the `HOW-TO-WRITE-A-COURSE.md` guidance (identical across
  tarot/astrology/starter) to tell future course-writers to link to
  `GRAMMAR_FORMAT.md` for field shapes instead of restating them inline.

## Jul 8 2026

- **`course/how-tarot-works.mdx` restructured: new opening thesis + Tolkien functions
  reordered Recovery → Escape → Fantasy → Consolation.** Builder's direction: the course
  should open with an inspiring, objective summary of the whole argument before diving in,
  and Tolkien's gifts should be walked through in the order they actually happen in a
  reading — Recovery (see the structure again, from a different angle), then Escape (a
  lens to sit with the present through, not a distraction from it), then Fantasy (the
  imagination's move — new possibilities), with Consolation landing naturally after all
  three, unchanged. Added a new "The whole argument, in miniature" section right after the
  existing opening paragraph (two paragraphs: the thesis in miniature, then how the course
  plays it out — Tolkien's functions as the map, then psychology, then the honest science,
  ending at the beholder's light). Reordered/reframed the Recovery/Escape/Fantasy paragraphs
  in "Tolkien: what fiction is for" with an honest note that Tolkien's own essay names them
  in a different order (Fantasy, Recovery, Escape) — all existing verified quotes/citations
  (Murray et al. on Recovery, the prisoner/deserter framing for Escape, the eucatastrophe for
  Consolation) kept intact; only connective prose changed. Added one closing paragraph
  introducing "my favorite three-card spread" (position 1 Recovery, 2 Escape, 3 Fantasy)
  linking to the new spread grammar below. Mythopoeia, the science sections, and the closing
  were **not** touched, per instruction.
- **New spread grammar `tarot/tolkien-three/grammar.json`** — "Tolkien's Three — Recovery,
  Escape, Fantasy," a 3-position tarot spread built on the course's reordered Tolkien
  framing. Shape modeled on `casting-big-three` from the sibling `recursive-astrology` repo
  (items carry `position` + a `casting` block), adapted for tarot: `grammar_type: "sequence"`
  (both repos share the same `GRAMMAR_FORMAT.md` enum), `casting.draw: "random"` (unlike the
  astrology castings this borrows the shape from, nothing here derives from birth data — any
  tarot deck grammar, shuffled, drawn into the three positions), `allow_reversed: true`. Each
  position item has `sections.Position` (a one-line description) and `sections.Prompt` (the
  exact reflective question from the course: Recovery — "this structure, seen from a
  different angle: what do you actually see, freed from the label?"; Escape — "a lens to sit
  with the present through — not a distraction, a way to stay"; Fantasy — "the imagination's
  move: what new possibility wants to exist?"). Credits *On Fairy-stories* in
  `_grammar_commons.attribution`. Not registered in `tarot/_collection.json` (that registry
  is scoped to the deck genealogy branches only — standalone grammars like
  `how-to-contribute` follow the same pattern of living outside it) or `tarot/_eco_ids.json`
  (populated only after a real Supabase publish, which didn't happen this session).
- **Regenerated the course mirrors after the mdx edit**: ran
  `python3 scripts/course_to_grammar.py how-tarot-works how-tarot-works-course "How the Cards
  Can Work"` (11 lessons, up from 10 — the new opening section is now its own lesson item) and
  `python3 scripts/build_reading_course.py` (rebuilds the collapsed
  `course/reading-the-cards.mdx` from all 12 Book II chapters). Ran `python3
  scripts/check_all.py` — all 56 grammars pass (JSON valid, no dangling `composite_of`,
  people + meta grammars rebuild clean, meta reports `dangling=0`). That run also refreshed
  the `_built_at` timestamp on the auto-generated `tarot/all-decks-many-lenses/grammar.json`
  (routine rebuild artifact, no content change).

## Jul 7 2026 (4)

- **Golden Dawn (Book T) deck becomes an astro voice via item keys** (proving the builder's
  item-key federation design, `docs/DESIGN-oracle-trinity.md` "Refinement" section in the astro
  repo). Added `metadata.planet` / `metadata.sign` / `metadata.element` to all 22
  `major-arcana` items in `tarot/golden-dawn-book-t-tarot/grammar.json`, matching the exact
  canonical Book T astrological attribution already recorded in each card's (pre-existing)
  `metadata.attribution` field: Fool=Air, Magician=Mercury, High Priestess=Moon, Empress=Venus,
  Emperor=Aries, Hierophant=Taurus, Lovers=Gemini, Chariot=Cancer, Strength=Leo, Hermit=Virgo,
  Wheel of Fortune=Jupiter, Justice=Libra, Hanged Man=Water, Death=Scorpio,
  Temperance=Sagittarius, Devil=Capricorn, Tower=Mars, Star=Aquarius, Moon=Pisces, Sun=Sun,
  Judgement=Fire/Spirit, World=Saturn — verified against multiple independent published sources
  (davidcunliffe.com's Golden Dawn correspondence table, already cited in this deck's own
  research notes; corroborated by Mary K. Greer, Angelorum, Biddy Tarot). Values use the exact
  casing recursive.eco's `PLANETS`/`ZODIAC_SIGNS` constants expect (`apps/flow/src/lib/offer/
  unified-grammar-types.ts`), and the three elemental trumps (Fool/Air, Hanged Man/Water,
  Judgement/Fire) get `metadata.element` instead of a planet/sign. Also added a one-line
  "Astrological attribution (Book T)" entry to each card's `sections`. `item.category` was left
  untouched (`major-arcana` — these stay tarot cards, not re-typed as astrology items). Purely
  additive: no other field in the file changed (verified programmatically against the prior
  commit). **Caveat for the app side**: recursive.eco's live astro-voice matcher
  (`astrology.types.ts` `convertUnifiedToInterpretations`, and the `astrology-grammars.ts`
  picker) currently gates on `item.category` being one of `planet/sign/house/graha/rashi/
  nakshatra/aspect/transit` — metadata alone, on a `major-arcana`-categorized item, is not yet
  read by that matcher. The keys added here are the data-side half of the federation design;
  making the astro oracle actually pick them up needs an app-side change (have the matcher also
  honor `metadata.planet/sign/element` regardless of category) — not made here, since this task
  was data-only and instructed not to force a category change.

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
