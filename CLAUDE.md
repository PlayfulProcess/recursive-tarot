# CLAUDE.md — recursive-tarot

## The spine: voices & the one intention

1. **The creed is the spine.** The project turns on `viewers/voices.json` → `shared_intention`: *"Read to know yourself, not to surrender yourself… relate to the card; never obey it."* The history, the why-it-works lenses, the two wings, the courses, and the Caster all exist to serve that one creed.
2. **Gate, not fate — and let each voice speak as itself.** The `shared_intention` creed is the container shown above all voices; under it, present each tradition *faithfully, in its own terms* — a voice's `how` should sound like the Golden Dawn (or Kant, or Jung), not like us editorializing about it. Render any *disagreement* with a tradition in the long form (its **course**), never in the short **intention**. The one hard floor everywhere: stay autonomy-preserving — never state a card as prediction or as something to obey. Honor the tradition's authentic practice (the Golden Dawn's pathworking genuinely *is* gate-not-fate); keep the critique in the course. **Name a school, not a living person:** voices drawn from a living teacher are titled by their tradition (DBT, Non-Dual Tantra, Post-Activism, Hospicing Modernity) and say "inspired by" — only dead, eponymous figures (Kant, Jung) carry their own name. `voices.json` → `shared_intention.interpretation_note` holds the standing disclaimer that every voice is a faithful-but-still-interpretation, never the person's words or endorsement.
3. **Consolidate, don't multiply.** Prefer turning a new idea into something we already have — a **voice** (`voices.json`), a **deck**, a **source** (`books-of-tarot` / `people-of-tarot`), or a **journey** (the four doors: Player · Historian · Practitioner · Contributor) — over a parallel structure. The Golden Dawn is the worked example: it became a *voice* + a short pathworking course, not a separate sub-site.
4. **Voice vs Source (the two wings).** A tradition's *reading stance* is the **Living/practice** layer (voices, courses, the Golden Dawn Path); its *people, books, and decks* are the **Record/evidence** layer (`docs/DESIGN-two-wings-provenance.md`). Keep them in their own places and cross-link with the one pill pattern below — never let a practice claim masquerade as a historical one.

## Reflective practice, not a habit (Sep 26 2026)

From the tarot hope-or-habit study (`recursive-eco/docs/future_plan/STUDY-tarot-hope-or-habit-2026-09-26.md`):
- **The deck never calls.** No daily card, streak, badge, push or re-engagement message about readings. Events a person opts into (a monthly table) are not readings and are fine.
- **Re-casting is never silent.** Caster Studio shows the session's draw count from the second draw on (`#castCount`, sessionStorage only, used for nothing else).
- **Practice words, not delivery words.** Buttons say "Lay the cards" / "Draw & reflect", never "Get a Reading".
- **Say the true thing at the draw.** The Oracle Ribbon (`viewers/oracle-ribbon.js`) carries the framing at the moment of the cast; keep its evidence line accurate. Barnum/Forer is about accepting *personality descriptions*, not predictions or advice; the blind tests (Blackmore 1983, about ten people per experiment, one experiment significant on reanalysis; Ivtzan & French 2004) are about recognizing one's own reading, and are small.
- **Tarot stays off kids surfaces**; AI readings are adults-only (that gate lives in recursive.eco, not here).

## Theme & colour — ONE source (`theme.css`)

- **All colour lives in `theme.css`** (a single `:root` of tokens), linked by every page and viewer.
  **Never redeclare colour tokens locally** and never add a `@media(prefers-color-scheme:dark)` block —
  that's what caused the recurring light-on-light bugs (each page had its own divergent palette).
- **Light only.** Backgrounds are always light, text always dark enough to read on them. No dark stages
  (video players / game tables are light too). Token names are unified but legacy aliases resolve:
  `--panel`=`--surface`, `--muted`=`--mut`, `--accent`=`--gold`, `--ink-strong`/`--fg`/`--text`=`--ink`.
- To change a colour, edit `theme.css` once. To re-apply the consolidation if a new file drifts:
  `python scripts/apply_theme.py` (links theme.css, strips local colour tokens + dark blocks).
- Bump `style.css?v=N` when style.css changes; `theme.css?v=N` likewise.

## Core architecture

- Grammar files live in `tarot/<slug>/grammar.json`, in grammar format v2 (Oct 2026, recursive.eco
  `docs/architecture/model-track/FORMAT-V2-NODES.md`): the array is `nodes`, a node's children are `parts`,
  links are `ref_grammar_id` / `ref_node_id`, `node_type`, a named pick is `category: "selection"`, and there is
  no stored `level` (depth is computed from `parts`). Generators, checks and viewers read and write only these names.
- Never hand-edit `tarot/all-decks-many-lenses/grammar.json` or `tarot/people-of-tarot/grammar.json` — both are generated.
- Always run `python scripts/check_all.py` before committing. Must end "all checks passed" with `dangling=0`.
- After any grammar edit: `python scripts/build_meta_grammar.py` (rebuilds meta + people). Then check_all again.
- **ONE branch: `main`. Site, app-sync and Pages all live there** (reconciled Jul 30 2026; verify with `gh api repos/PlayfulProcess/recursive-tarot/pages`):
  - **GitHub Pages serves `main` in deploy-from-branch mode** — `build_type: "legacy"`, `source: {branch: "main", path: "/"}`, custom domain `tarot.recursive.eco`. GitHub publishes the branch itself on every push; there is **no** Pages deploy job in Actions, and `actions/deploy-pages` would fail against a legacy-configured site. Root **`.nojekyll` must stay** — it's what stops the Pages build running Jekyll over the site.
  - `.github/workflows/build-meta.yml` only rebuilds and commits the meta-grammar. **Never re-add `pages: write` / `deploy-pages` to it** unless Pages is first switched to `build_type: "workflow"`.
  - **`main` is also the repo's default branch and the recursive.eco sync source** (`recursive-eco.json` → `default_branch: main`). So one push to `main` updates the live site *and* what the app pulls. No more double-applying a change to two branches.
  - `claude/website-content-cards-plan-xwn8lj` was the old Pages branch. It is **retired** — merged into `main` on Jul 30 2026 (real merge commit) and left in place, unpushed-to. Don't work from it. `dev` is likewise retired and its `origin/dev` ref is stale *and* divergent; don't work from it either.
  - CI lands `chore: rebuild meta-grammar [skip ci]` commits on `main`; always `git pull --rebase` before pushing.

## recursive.eco integration (the GitHub boundary)

This repo is the open half; **recursive.eco** is the private app. They share the grammar JSON format
and pass grammars across GitHub. Full reference: **[docs/RECURSIVE-ECO-INTEGRATION.md](docs/RECURSIVE-ECO-INTEGRATION.md)**. The essentials:
- The app **reads from `main`** (`raw.githubusercontent.com/PlayfulProcess/recursive-tarot/main/tarot/<slug>/grammar.json`) and **writes back to `main`** via `app/recursive-eco` sync PRs ("Resolve all drifts"). Since Jul 30 2026 `main` is *both* the app's source of truth and the live static site (see above), so one landing serves both. Work on a feature branch and merge to `main`, reconciling (never discarding) the App's write-backs that land there.
- **Slug ↔ app UUID:** `tarot/_eco_ids.json`.
- Sync **must not drop repo-only fields** (`_grammar_commons` licence — on *all* grammars — `_image_usage`, `lineages`, cross-link pills, Research notes) and **must skip `_generated: true` grammars** (meta, people). The courses are not generated since Oct 23 2026: each is a grammar in `tarot/<id>-course/` (and `tarot/how-to-contribute`), read in recursive.eco Play, Continuous; the site links there through `courses-play.js`, and `pages/course-viewer.html` only forwards old links. The doc has the full ownership model + the merge-onto-repo write-back fix.

## The one cross-link pattern (DO NOT INVENT ANOTHER)

The viewer renders a pill link automatically when an item has:
```json
{
  "metadata": {
    "source_deck": "<slug>",
    "source_node_id": "<node-id>",
    "deck": "<human label>"
  }
}
```
The pill reads: **"Open in [deck] →"**. This is the ONLY cross-grammar navigation mechanism. Use it for everything — meta → deck, deck → people, deck → related grammar. Never add a new link field.

Examples:
- Meta grammar item → source deck: `source_deck: "visconti-sforza-tarot"`, `source_node_id: "major-00-il-matto"`, `deck: "Visconti-Sforza"`
- Individual deck item → people: `source_deck: "people-of-tarot"`, `source_node_id: "person-bonifacio-bembo"`, `deck: "People & Institutions"`

The pill suppresses itself if the current page URL already contains `/<slug>/`, so it never shows a circular link.

## People grammar

- Source of truth: `research/people/*.md` dossiers. Edit those, then run `python scripts/build_people_grammar.py`.
- Do NOT hand-edit `tarot/people-of-tarot/grammar.json`.
- To link a deck item to a person: add `source_deck / source_node_id / deck` to that item's `metadata` (same pattern as above).

## Sections used across grammars

| Section | Meaning |
|---------|---------|
| ~~`Scene`~~ | **Retired Oct 4 2026.** AI vision descriptions, archived in `tarot/_archive/ai-scenes-2026-10-04/`. Don't write new ones: where a tradition wrote its cards down (Book T, Waite, Etteilla), the card carries that tradition's own text |
| `Symbol` | Semiotic note: what the visual elements mean in the tradition they come from |
| `Research note` | Sourced historical claims with `[@citation]` keys |
| `Figure` | Named figure on the card (courts, named trumps) |
| `Tradition Note` | Contextual note placing the card in its historical programme |

## Image pattern

All deck images are on R2 at:
`https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/<deck-folder>/<filename>`

**No AI-written card descriptions under a tradition's name** (PlayfulProcess, Oct 4 2026). The
Scene sections once written by viewing images with vision were found unreliable and archived
(`tarot/_archive/ai-scenes-2026-10-04/README.md`). Where a tradition wrote its cards down, render
its own text, from public-domain printings (Book T as printed in *The Equinox* I(8), 1912; Waite's
*Pictorial Key*, 1911). Vision may only propose candidates, labelled "machine description,
unchecked", for a person to approve. Decks no tradition fully held (Sola Busca) may carry new
meaning, labelled as ours.

**Thumbnails are always resized, never cropped.** Card images must show the whole card — use
`object-fit:contain` (letterboxed on a neutral background), never `object-fit:cover`. A clipped
card hides the very iconography the thumbnail exists to show. Applies to every card thumbnail:
play tiles, course strips/detail, game cards, deck covers, viewers.

## Image usage across the site (render the most of the library)

Card images appear in site chrome (Home / Play / Historian / Contribute / games). Show the deck's
**range** — keep images **unique within a page**, and avoid reusing the same image across sibling
pages (especially **Home ↔ About ↔ Play**). After editing any page's imagery, run
`python scripts/audit_image_usage.py`: it writes a top-level `_image_usage` onto each deck's
grammar.json (the deck's images + the pages they feed) and regenerates `docs/plan/IMAGE-USAGE.md`, which
flags every cross-page repeat. Keep it up to date — it's how we spread unique cards and render the
most of the library. (Prefer the Star / courts / Empress over yet another Visconti World.)

## Course images — one home, one convention

Course figures/screenshots live in **`pages/courses/images/`** — the single canonical location.
A course grammar links them by full address, `https://tarot.recursive.eco/pages/courses/images/<name>.ext`
(Play is another site, so a relative path does not reach them); a diagram goes beside its grammar,
`tarot/<slug>-course/diagrams/`. Don't scatter course
images elsewhere (the old `course/img/` folder was consolidated here Jun 23 2026). Card art still
comes from R2 (see the Image pattern above); this folder is only for course-authored figures.

## Scripts cheat-sheet

| Script | What it does |
|--------|-------------|
| `scripts/build_meta_grammar.py` | Rebuild all-decks-many-lenses + people grammars |
| `scripts/build_people_grammar.py` | Rebuild people-of-tarot from research/people/*.md |
| `scripts/enrich_cards_from_research.py` | Add Research notes from research/cards/*.md (idempotent) |
| `scripts/refresh_collection.py` | Sync _collection.json from grammars |
| `scripts/normalize_book_t_sections.py` | Idempotent Book T section normaliser; `--check` asserts nothing was lost |
| `scripts/import_wirth_1927.py` | Writes Wirth's own words (*Le Tarot des imagiers du Moyen Âge*, Paris 1927, French + page + this site's translation) onto the 22 Wirth cards from `research/sources/wirth-imagiers-1927.json`; `--check` |
| `scripts/import_book_t_1912.py` | Writes Book T's own 1912 text (*The Equinox* I(8)) onto the 78 Golden Dawn cards from `research/sources/book-t-equinox-1912.txt`; `--check`; `--verify-scan` compares with the 1912 scan's OCR |
| `scripts/link_glossary.py` | The glossary link layer: first mention of a glossary term per section links to `pages/glossary.html#term`, "Path NN" to `pages/tree-of-life.html?path=NN`, in the Golden Dawn deck's editorial sections and the GD course chapters (never inside Book T's quoted text). Entries live in `tarot/glossary-of-tarot/grammar.json` (hand-edited). Re-run after editing either; `--check` runs in check_all |
| `scripts/build_book_t_page.py` | Writes `pages/book-t.html`, the whole 1912 Book T as a reading page (printed page numbers, card pictures, glossary + card + Path links, Crowley's notes set as notes), from `research/sources/book-t-equinox-1912.txt` + `scripts/book_t_page_template.html`. Corrections to the transcription are listed in its `FIXES`, each with the scan page. **Generated, never hand-edit**; `--check` runs in check_all, so a glossary or deck edit may need a re-run |
| `scripts/build_book_t_deck.py` | Writes `tarot/book-t/grammar.json`, Book T's own deck: its 78 cards in Book T's order (the list "The Titles of the Symbols"), named by Book T's titles, the 1912 text on each, **no pictures** (empty `image_url` slots PlayfulProcess fills over time; a re-run keeps every picture and any section it doesn't own). `metadata.number` is Book T's list number 1-78, never repeated in a name. Since Oct 20 2026 (elemental dignities): `metadata.element` on all 78 (courts read by their suit's element; Keys by attribution, planets by the table in `KEY_ELEMENT_OF`, our choice), Book T's ill-dignified sentences set apart in the section `If ill dignified`, and `metadata.reading_rule: "elemental-dignities"` on the deck, which recursive.eco reads. `--check` runs in check_all |
| `scripts/build_book_t_iconography.py` | Book T's third picture set (Oct 19 2026): composes the glyphs in `tarot/book-t/glyphs/` (7 planets, 12 signs, 4 elements + Spirit, 22 Hebrew letters; drawn for this site, CC BY-SA, see its README) onto each card from the card's own metadata, where Book T's sentence places them (decan planet and sign above and below the central symbol, in Book T's order; the Keys' letter in the centre), and writes `tarot/book-t/iconography/<id>.svg` + one `metadata.illustrations` entry per card, `edition: "Book T deck, iconography"` (the set name Play's Pictures choice and the 1912 page's switch read). **Generated**: edit a glyph or the script, re-run, then `build_book_t_page.py`. `--check` runs in check_all |
| `scripts/build_book_t_full_imagery.py` | Book T's fourth picture set (Oct 20 2026), the full imagery: everything Book T's text describes for each card (the hands issuing from clouds, the suit symbols counted and posed as the text says, roses, lotuses, flames, waters, the courts' figures, beasts and crests; the Keys as symbolic figures from their titles, since Book T gives them meanings only), composed from the parts in `tarot/book-t/parts/` (118, drawn for this site, CC BY-SA, see its README) and the glyphs, by a spec per card in `tarot/book-t/full-imagery/compositions.json` (the Book T sentence it follows + its layers; nothing card-specific in the script). Writes `tarot/book-t/full-imagery/<id>.svg` + `metadata.illustrations` `edition: "Book T deck, full imagery"`; the 1912 page's switch button **Full imagery**. **Generated**: edit a part or a spec, re-run, then `build_book_t_page.py`. `--check` runs in check_all; `--png DIR` renders PNGs + contact sheets to look at |
| `scripts/build_book_t_linocut.py` | Book T's fifth picture set (Oct 20 2026), the **linocut**: the full imagery's compositions (same `compositions.json`, so the same things in the same places) printed as a relief print: black on warm paper with one ink per card (Fire vermilion, Water deep blue, Air ochre, Earth olive, Keys gold), a carved arch, dog-tooth border and black title cartouche, gouge patterns and the press/grain filters (SVG only, no images). Prints each part from its carved block in `tarot/book-t/parts-linocut/` (see its README) when there is one, else pulls the full imagery's part into the inks. Writes `tarot/book-t/linocut/<id>.svg` + `metadata.illustrations` `edition: "Book T deck, linocut"`; the 1912 page's button **Linocut**. **Generated**: edit a block or a spec, re-run, then `build_book_t_page.py` and `build_card_pages.py`. `--check` runs in check_all; `--png DIR` renders PNGs (slow: the filters) |
| `scripts/build_book_t_painted_symbols.py` | Book T's sixth picture set (Oct 20 2026), **painted with its symbols**, and since Oct 21 2026 **Book T's official picture** (her words: "let's make these cards the official ones"): the script puts its entry first in `metadata.illustrations` with `is_primary` and sets the node's `image_url` to it, so the 1912 page (default switch), `book-t/*.html`, the card viewer and the app all show it; the other five sets stay selectable. Fit to the 1912 text: `docs/research/BOOK-T-PAINTED-CHECK-2026-10-21.md`. each card's painting (the first `illustrations` entry naming a painting or the composite) whole in a window, framed by the iconography's glyphs in gold on a band coloured from the painting's own edges (top: the planet, or what Book T names first, the element of the element, the attribution; the card's letter left, the suit's element right; bottom: the sign, the court's degrees via `text_degree`, the Hebrew letter; then the title). The painting is **embedded** as a 600 px JPEG data URI, because an SVG shown with `<img>` never loads an external file; `data-painting` records its URL and a re-run reuses the embedded JPEG while that URL is unchanged (so `--check` is offline; a changed painting is fetched with curl). Writes `tarot/book-t/painted-symbols/<id>.svg` + `metadata.illustrations` `edition: "Book T deck, painted with its symbols"`; the 1912 page's button **Painted + symbols**. **Generated**: re-run after a painting changes, then `build_book_t_page.py` and `build_card_pages.py`. `--check` runs in check_all; `--png DIR` renders PNGs |
| `scripts/record_golden_dawn_path.mjs` | Optional (Oct 21 2026): records `pages/golden-dawn-path.html` (the Tree of Life animated: the Lightning Flash down, the Path of the Serpent up, each Key's painted+symbols card brought forward, all read from `tarot/book-t/grammar.json`) as PNG stills (`--stills`, one per step) or a movie (`--movie`, frames by the page's own `GDPath.render(t)`, then ffmpeg). No npm packages: drives local Chrome/Edge over DevTools. Serve the repo first (`python -m http.server 8765`); frames go to the system temp folder. By hand: `?frame=N&embed=1` (one step's still), `?t=4.5`, `?mode=descent`, `?aspect=portrait` (9:16) |
| `scripts/check_all.py` | Pre-commit gate |
| `scripts/build_search_index.py` | Writes `search-index.json` (the header's quick-jump search: cards, decks, chapters). **Generated, never hand-edit**; check_all and the build-meta workflow rebuild it. See `docs/QUICK-JUMP-SEARCH.md` |
| `scripts/build_card_pages.py` | Writes `card/<card>.html` (one page per Rider-Waite-Smith card: Waite's 1911 text, his upright/reversed meanings for the minors, and Book T 1912 in its own section), the list `tarot-card-meanings.html`, `sitemap.xml` and `data/sitemap-lastmod.json`, for search engines (Oct 14 2026). **Generated, never hand-edit**; re-run after editing `rider-waite-smith-pictorial-key` or `golden-dawn-book-t-tarot`, or a page listed in its `STATIC_PAGES` (that one only warns). `--check` runs in check_all. **Since Oct 20 2026 it also writes** `book-t/<card>.html` (all 78 Book T cards from `tarot/book-t`), `book-t/decans.html`, `book-t/index.html`, `deck/<slug>.html` + `deck/index.html` (one page per historical deck grammar) and `spreads.html` (Waite's own Celtic Cross and trump meanings, from `research/sources/waite-pictorial-key-part-iii.md`, which also fill the 22 trump card pages). These folders sit **outside `tarot/`** on purpose: recursive.eco reads only `recursive-eco.json` and `tarot/*/grammar.json` (its webhook treats anything under `tarot/` as grammar). Deck-page images follow `docs/rights/image-ledger.json` card by card (Commons PD/CC0 or CC BY-SA, a holder's open-access scan (d'Este, Yale), or a copy its holder files as public domain (`public-domain`: Charles VI's 1844 lithographs, Liège); never BnF/Gallica scans or facsimile scans; a card with no picture links to `metadata.holder_url`, as all of Visconti-Sforza does since Oct 20 2026), so re-run `audit_image_rights.py` and then this script after an image change. A Book T picture or deck edit makes these pages stale: re-run it |
| `scripts/build_sources_grammar.py` | Writes `tarot/sources/grammar.json` (where each deck's pictures are held, their quality, rights as published, one plain property-rights line; selections by deck, holder and rights), `docs/rights/IMAGE-FLAGS.md` (every shown image that is non-commercial-only, a facsimile scan or unsourced, with free alternatives) and the "Where the pictures come from" line in each deck's description (Book T's lives in `build_book_t_deck.py`), from `research/sources/image-sources.json` (Oct 20 2026). **Generated**; `--check` runs in check_all. Images only where a source's own statement says PD/CC0/CC BY |
| `scripts/audit_image_rights.py` | Asks Commons what every card image is (licence, credit); writes `docs/rights/IMAGE-LEDGER.md`. Re-run after any image change. The site says **open**, never "public-domain library": see `docs/rights/RIGHTS-AUDIT-2026-10-04.md` |

**`scripts/archive/` is history, not tooling.** The one-shot generators that first built each
deck live there (moved Jul 27 2026). Their output is canonical in `tarot/<slug>/grammar.json`
and has been hand-edited since — **re-running one would overwrite current content with months-old
seed data.** To change a deck, edit its `grammar.json`. See `scripts/archive/README.md`.

## Cross-grammar embeds — always framed

An item that carries the `source_deck`/`source_node_id` cross-link (above) also gets the OTHER
grammar's content resolved into its detail view (`viewers/reference-resolve.js`). That embed is
**always framed** — a bounded, collapsed `<details>` box that names the relationship ("Featured
card from Golden Dawn Tarot", "About Pamela Colman Smith") and says whose content it is. Never
render resolved content in the host's own section markup: that's what made a card's
Scene/Symbol read as part of a person's biography, and a person's biography read as part of all
78 Golden Dawn cards. The one exception is the aggregator (meta) grammar — its items are pointer
stubs, so there the box opens expanded. `RefResolve.renderEmbed()` is the single implementation
for `cards.html`, `tree-viewer.html` and `caster-studio.html`; change it there, not per viewer.
