# Site redesign + course arc — master status (June 2026)

The single anchor for the editorial-redesign + practitioner-course work so nothing is
lost between sessions. All of this is on **`dev`** (Pages serves dev → https://tarot.recursive.eco).
Git identity for pushes: `PlayfulProcess <17236172+PlayfulProcess@users.noreply.github.com>`
(the gmail address is blocked by GitHub email-privacy). Conventions: **light only** (no
dark mode), **Fraunces** (serif) + **Inter** (sans), **never crop card art** (object-contain
on a neutral mat), cache-bust with `style.css?v=N` + `site-header.js?v=N`.

---

## ✅ DONE (this arc)

### Book II — the practitioner course "Reading the Cards" (12 chapters, complete)
- Manifest `books/how-to-read-the-cards/book.json`; individual essays in `course/*.mdx` are
  the source of truth. **Collapsed** into one course `course/reading-the-cards.mdx` via
  `scripts/build_reading_course.py` (run it after editing any chapter); the Courses menu shows
  one "Reading the cards" entry with a collapsible section outline.
- Chapters: `how-tarot-works` (spine; was "why-tarot-works" — renamed so it doesn't assume it
  works for everyone → **"How the Cards Can Work"**), `tarot-and-the-crack`, `intention-setting`,
  `kant-` / `marsha-linehan-` / `morality-is-an-ecosystem` / `jung-` / `non-dual-tantra-` /
  `post-activism-` / `hospicing-modernity-reads-the-tarot`, `walking-the-golden-dawn-path`,
  `divination-traditions`. (Living teachers = school-titled + "inspired by"; Jung named.)
- Research backing in `research/why-tarot-works/` (REPORT + raw deep-research + reverification).

### "Tarot & the Crack" — philosophy enrichment (Jun 22)
- Added 4 sections weaving the author's developed position (drawn from her own book-repo, see
  source map below): **deconflation** (belief in a transcendental realm ≠ the empirically-grounded
  openness to "more than we can perceive"), **the altar + speaking to the invisible** (relationship
  as showing-up/reciprocity, not belief), **the numinous borrows our language** (it can only reach
  us through structures we already have — English, Christian icons, the Tower — so tarot is
  *eligible* as a language for negotiating with the mysterious), **faith + curiosity + the skeptic
  you keep at the table** (Aquinas: divine law changed because the eternal law is unknowable →
  hold the sacred seriously *and* loosely).

### Homepage — editorial-cover redesign (iterated heavily per feedback)
- `index.html`: card-left / text-right hero with the large matted **Visconti World ("Il Mondo")**;
  three doors = **Read the history → `pages/historian.html`** · **Draw a reading → `pages/play.html`**
  · **Contribute**; "Every view" gallery **classified** Card-level (Cards, Caster) vs Grammar-level
  (Explorer, Timeline, Genealogy, Tree of Life); **historical decks + contemporary decks** rendered
  dynamically from `tarot/_collection.json`; **recursive.eco "tree" callout** (reusable: `.ecotree`).
- Fixes folded in: tagline "pill border" was a `.tag` class collision with style.css → renamed
  `.subtitle`; dropped the links footer; never-crop everywhere; "ancient Egyptian" misconception
  corrected (Mamluk Egypt is real; the Thoth occult myth is the 1781 invention).

### New page
- `pages/historian.html` — the Historian path: course banner + lineage views + 25 contained deck thumbs.

### Dark-mode sweep (partial — see queue)
- Fixed: `pages/play.html`, `pages/sources.html` (dark `--panel:#161226` default removed),
  `pages/shop.html` (dark badges + dark `.ghost` "Booklet" button + low-contrast note + uncropped
  covers), `viewers/timeline.html` (invisible white `--ink-strong` in OS dark), `viewers/cards.html`
  (sidebar-thumb uncropped + smallest fonts bumped — partial).

### Typography
- Adopted recursive.eco's **Fraunces** serif site-wide (was Cormorant Garamond + EB Garamond),
  keeping Inter. `font-optical-sizing:auto`. Bumped `style.css?v=3` + `site-header.js?v=25` on 24 pages.

### Video program (`recording/examples/why-tarot-works-sequence.json`)
- Renamed display → "How Does a Tarot Reading Work?". **Enriched from 4 → 7 lenses**: added
  ⑤ ritual & expectancy, ⑥ productive randomness (Oblique Strategies + the lot as bias-refusal),
  ⑦ the long human practice (divination across cultures). New ones are **our concept cards**;
  real video footage slots for lenses 5–7 still need sourcing (see queue).

---

## Metaphor arc — "game → crystal ball → gate" (decided Jun 22)

The way to hold the cards is framed as a 3-station arch (now a coda in `intention-setting.mdx`):
**game** (1440s play) → **crystal ball** (Etteilla's 1780s oracle — read as fate, *obey*) →
**gate, not fate** (autonomy-preserving present; threshold you cross with your will intact;
reflects + lets you imagine). The **palantír** (Tolkien) is the named *failure mode* shared by
the cards AND AI — the seeing-stone that destroys whoever obeys it; the Palantir company is the
misread-of-Tolkien surveillance/AI version. This mirrors recursive.eco's own
`apps/landing/pages/safer-containers.html` ("AI Risks & Safer Containers": sycophancy,
dependency, loss of agency, fluency-mistaken-for-accuracy…). The discipline against fake-news /
the AI oracle = the discipline of gate-not-fate reading. **Open decision:** whether to replace
"mirror" with "gate" site-wide (creed/voices/essays) or keep mirror as anchor + gate as the
resolution. Candidate good-object names considered: window-at-dusk, threshold/gate (front-runner,
ties to "gate, not fate" + GD pathworking + safer-containers' "the refusals are the gates"),
prism, still-pool. STILL TODO: add the palantír (Denethor vs Aragorn) as the failure-mode
illustration in `how-tarot-works.mdx`; apply the gate metaphor where chosen.

## ✅ CLEARED in the autonomous pass (Jun 22)

- **Grammar + gate through-line**: defined "grammar" (linked to recursive.eco) in the hero + the
  ecotree block; retired "mirror" as the headline in `intention-setting` ("the deck as a grammar held
  as a gate, not a fate"); wove the arch (game → crystal ball → gate) into `history-of-tarot`.
- **Palantír passage** added to `how-tarot-works` ("A warning from Tolkien" — Denethor vs Aragorn;
  crystal ball = obeyed palantír, gate = Aragorn's; ties grammar + the AI/safer-containers vow).
- **Four doors** on home (Historian · Practitioner · Player · Contributor); hero CTAs removed; views
  re-classified (card: Cards/Explorer/Lenses/Tree · grammar: Tree of Life/Timeline/Genealogy).
- **`pages/contribute.html`** built (mirrors historian): course banner + ways-in + Claude/MCP callout.
- **`pages/play.html`**: "Play the cards" + a "Games of the Tarot" course banner on top.

## ✅ Dark-mode audit (Chrome-verified, Jun 22)
- **lenses.html** migrated dark → light (was `--bg:#0c0916`).
- **cards.html** light card tiles: `.thumbnail-card` dark charcoal gradient → `#faf8f3` mat; empty
  letterbox `#000` → `#faf8f3`; 'Group: Levels' dropdown `#221b38` → light gold pill. Verified across
  the 900-card grid. (2 truly image-less cards still show a faint placeholder — negligible.)
- **tree-viewer.html**: the login-prompt panel `#16121f` → light.
- **Games** (trionfi/tarocchino/madiao) are already light (light `:root` default; the
  `prefers-color-scheme` block is a redundant no-op). **sequence viewers** use `#000` intentionally
  (video-player context) — leave dark.

## ✅ Icons → SVG library (de-emoji) — DONE (Jun 22)
- Extended `icons.js` (rt-icon) +10: person, play, film, chart, tree, crack, sefirot, crown,
  device, printer. Converted every colored emoji to rt-icons across sources.html, play.html,
  course-viewer.html (QR), explorer.html, print-viewer.html, book/intro.html, and cards.html's
  JS fallbacks. Verified in Chrome/DOM (sources + play badges render SVG; cards.html no console
  errors). KEPT (content/typographic, not "colored emoji"): I Ching trigrams (☰☷…), astrology
  glyphs (♈⛢…), arrows (→↗↓…), geometric glyphs (▸▾✦…), the Alice-karaoke 🐇 (thematic), and one
  course-viewer 📺 in a code comment. Final scan: zero colored emoji on the main pages/viewers.

## ✅ Channel manifest on main (Jun 22)
- `recursive-eco.json` is on **origin/main** (and dev) — verified live at
  raw.githubusercontent.com/.../main/recursive-eco.json. Channel import resolves with default branch.

## ☐ STILL BLOCKED / needs live data or a bigger build
- **Live-iframe or screenshot view thumbnails** (preview screenshot tool hangs; iframes need perf test).
- **recursive.eco tarot-channel contemporary decks** (live API/MCP) + **ontoject cover** is `None` in
  `_collection.json` (so only the 36-Tattvas shows in the contemporary band).
- **Verified embeddable video IDs** for sequence lenses 5–7. **Series preface + about + EPUB build.**

## ☐ QUEUE — homepage IA + path pages (Jun 22, from feedback)

- **Four doors** done: Historian · Practitioner (`?course=reading-the-cards`) · Player (play.html) ·
  Contributor. Hero CTAs removed (were duplicated by the doors). Views gallery re-classified to match
  site-header: **card level** = Cards, Explorer, Lenses, Tree; **grammar level** = Tree of Life,
  Timeline, Genealogy (Caster dropped from gallery — it's the Play door's draw-a-reading tool).
- ☐ **Play page = mirror the Historian page**: a "how to play" course banner on top (source:
  `booklets/games-of-the-tarot.mdx`) + the play content (games + draw-a-reading) below. Make the Play
  door's page match `pages/historian.html`'s outline (course banner → content → decks/games thumbs).
- ☐ **Contribute page** (new, same pattern): the contribute course on top + the recursive.eco **Create**
  page + the Claude/GitHub-MCP course sessions (`build-a-tarot-deck-with-claude`) as thumbnails.
- ☐ **Real view thumbnails**: either screenshots (capture via connected Chrome) OR **live `?embed=1`
  iframes scaled down** (user's idea, "like in the course") — replace the representative card-art thumbs.
- ☐ **Contemporary decks**: list MORE than ontoject — pull the PD decks published in **recursive.eco's
  tarot channel** (live data; needs the platform API / grammar MCP, not just `_collection.json`). Also
  give `thirty-six-tattvas` a cover so it shows.
- **TERMINOLOGY (open):** user leaning toward calling a deck/card a **"grammar"** (recursive.eco's own
  term) — the noun for *what it is* — with **gate, not fate** as the *stance* (how to hold it). Two
  levels, not competing. Hero subtitle already nudged to "a grammar for meaning". Mirror→gate propagation
  + palantír passage still pending.

## ☐ QUEUE (not done — in rough priority)

1. **Icons → clean SVG library (de-emoji).** `icons.js` (`rt-icon`) exists (~15 icons). Extend it
   (mirror, film, play-triangle, document, people, branch…) and replace every colored emoji
   (`▶ 🪞 🎬 ✦ ⌥` …) across ~10 pages with `<rt-icon name="…">`. NOTE: some emojis read as mojibake
   in tooling — do it carefully per-file, not by blind script. User: "colored emojis seem less serious."
2. **Broader dark-mode audit.** Still carrying dark leftovers: `viewers/explorer.html` (dark `rgba`
   zones), `viewers/tree-viewer.html`, `viewers/prototypes/lenses.html`, the game pages
   (`pages/games/*`), the sequence viewers (`viewers/sequence*.html`, `recording/player/`).
3. **cards.html real light-theme pass.** The dark empty-card slots + dense controls; needs visual
   verification (the built-in preview screenshot tool hangs on these pages; use connected Chrome).
4. **Real view screenshots** for the gallery thumbnails. Blocked: capture tool exposes no saved path
   + heavy files. Representative card-art thumbnails kept for now.
5. **Verified video IDs** for video lenses 5–7 (ritual/placebo talk; Brian Eno on Oblique Strategies;
   I Ching / Ifá / casting-lots clips). Must be oEmbed-embeddable — research + verify, don't fabricate.
6. **Contribute home page** (third path, to match Historian).
7. **Series preface + About page**, then **EPUB/PDF build** (pandoc, reuse `book-repo/epub-build`).

---

## Book-repo source map (the author's own prior writing — for course/essay work)

Found via search of `book-repo/`. Use these for future essay enrichment (the author's voice):
- `books/axiom-beneath-the-ground/chapters/ch11-the-invisible-world.md` — "more than we can
  perceive" as the *conservative inference*; cross-cultural consensus; "neither belief nor disbelief."
- `…/ch12-relationship-to-what-cannot-be-seen.md` — reciprocity/showing-up as the grammar of relating
  to the invisible (libations, candle, puja).
- `…/v5/ch01a-interlude-the-cracks.md` + `…/v5/ch06a-where-the-maps-crack.md` — the crack as
  composting / a system's integrity (it admits it is a map).
- `…/v5/ch05a-the-unowned-dimension.md` — better-vs-worse maps; the three-filter epistemology.
- `…/v2-ch03-the-mandala-of-blessings.md` — altar as live practice; skeptics as necessary infrastructure;
  form serves the community (the icon is a pointer, not a vessel).
- `…/v5/ch00a-prelude-first-encounter.md` + `…/v5/ch00b-prelude-lilac-dance.md` — Paradevi/Gaia/
  ayahuasca thread; Krishnamurti/Bohm; līlā.
- `books/fire-before-responsibility-essay/chapters/09-the-hospicing.md` — Andreotti/Akomolafe;
  holding the crack without alarm.

---

## Key files
- `index.html` · `style.css` (tokens + Fraunces) · `site-header.js` (nav + injected webfont + rt-icons)
- `icons.js` (rt-icon SVG library — to extend) · `scripts/build_reading_course.py`
- `course/*.mdx` (chapters) → `course/reading-the-cards.mdx` (generated collapsed course)
- `recording/examples/why-tarot-works-sequence.json` (the video program)
- `tarot/_collection.json` (deck list + `cover_image_url`, drives the home/Historian galleries)
