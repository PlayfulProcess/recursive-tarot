# Astro & I Ching content plan — complete grammars, honest history

Two sibling repos, two different jobs. **recursive-astrology** needs *completeness*: every
tradition it hosts should carry the full working vocabulary of that tradition — all the
signs, planets, houses, aspects, and whatever else that school actually reads with.
**recursive-iching** needs *perspective*: the repo as a historical, editorial account of
how the book and the traditions around it developed — the same scholarship-first stance
as the tarot repo, including curated video playlists with real specialists.

Both inherit the tarot repo's proven machinery wholesale: research dossiers with
adversarial verification → build scripts → `check_all` gate → grammar mirrors →
`_eco_ids.json` → channels page. Nothing new to invent; two repos to fill.

Neither repo is in this session's scope — step 0 for each is adding it to a session and
auditing what actually exists before trusting any assumption below.

---

## Part 1 — Astrology: complete grammars per tradition

### The completeness principle

A tradition's grammar is complete when a practitioner of that tradition finds nothing
load-bearing missing — and finds nothing smuggled in from a *different* tradition. That
second half matters as much as the first: whole-sign houses don't belong in a modern
psychological deck, and Uranus doesn't belong in a Hellenistic one. Same rule as the
tarot voices: **each tradition speaks faithfully in its own terms**, disagreement lives
in the long-form course, and the one hard floor everywhere is autonomy-preserving
language (a chart describes patterns to relate to, never a fate to obey).

### What "complete" means, tradition by tradition

**Western traditional / Hellenistic** (one grammar set):
- 12 signs · the **7 classical planets** (Sun→Saturn, no outers) · 12 **whole-sign
  houses** with their traditional topics and joys · the classical **aspects** (conjunction,
  sextile, square, trine, opposition — as sign-based configurations) · the **lunar nodes**
  · **sect** (day/night) · essential **dignities** (domicile, exaltation, triplicity,
  detriment, fall). Dignities are reference data — a table item, the legitimate use of
  tables.

**Modern / psychological** (a separate grammar set, not a layer on the first):
- 12 signs · **10 planets** (through Pluto; Chiron flagged as a common-but-contested
  addition, stated as such) · 12 **quadrant houses** (Placidus as the common default,
  said plainly as a convention, not a truth) · 5 major aspects with orbs · nodes ·
  angles (ASC/MC as chart points). Voice rules apply: a lens drawn from a living
  teacher's school is named for the school and says "inspired by."

**Jyotiṣa (Vedic) and Chinese astrology** — flagged as future wings, not started until
each has a dossier and (ideally) a practitioner-reader; a shallow nod would violate the
faithfulness rule worse than absence does.

Each item carries the standard sections adapted from tarot's table: `Scene` (what the
symbol/glyph depicts), `Symbol` (what it means *in that tradition's own terms*),
`Research note` (sourced history: where this house meaning actually comes from, with
citations), `Tradition Note` (placement in the tradition's programme).

### How the work runs (the tarot method, verbatim)

1. **Audit** what recursive-astrology already has (courses exist — "The Right Size" —
   and a grammar-driven course viewer; the deck inventory is the unknown).
2. **Research first**: one dossier per tradition in `research/` with the ✔︎/○/◆
   confidence convention. The history of house systems and the sign/constellation
   distinction are the two places pop-astrology most needs the honest treatment —
   equivalent to tarot's Egyptian-origin myth.
3. **Build scripts, not hand-edits**: `build_<tradition>_grammar.py` generating
   `grammars/<slug>/grammar.json` from the dossiers (the people-grammar pattern), so the
   dossier stays the source of truth.
4. **Images**: public-domain plates via `commons_image_search` — Urania's Mirror cards
   (1824, PD), medieval zodiac miniatures (Très Riches Heures), Alfonso X manuscripts —
   license string stored per item, imageless over wrong, resized never cropped.
5. **Gate + publish**: port `check_all.py`, seed `_eco_ids.json` via the MCP
   (`list_grammars`), port `channels.html` (config → channel `astrology`), publish
   via `set_grammar_visibility` when each set is genuinely complete.

**Order:** Hellenistic/traditional first (it's the historical root and the modern set
constantly references it), then modern/psychological, then the cross-links (each sign
item pill-links its planets/houses via the one cross-link pattern — no new link fields).

---

## Part 2 — I Ching: a historical, editorial repo

### The stance

Exactly the tarot repo's move, transposed: where tarot's spine is *"a game that acquired
meanings"*, the I Ching's is *"a divination manual that acquired a philosophy"* — and
both histories are usually told backwards by their traditions. The repo's job is the
documented story, stage by stage, each stage a grammar or course chapter with sourced
dossiers, legends clearly labeled as legends.

### The historical spine (each stage = a chapter, most also a grammar)

1. **Shang oracle bones** (c. 1200 BCE) — divination by heat-cracks, the ancestor
   practice; already dossiered in tarot's `research/why-tarot-works/REPORT.md` §4.
2. **The Zhouyi core** (Western Zhou) — the 64 hexagrams with omen texts: a working
   diviner's manual, not yet philosophy. The Fuxi/King Wen/Confucius attributions
   presented as the tradition's own origin legend — honored *as* legend, exactly like
   tarot's Egyptian myth (modern scholarship: Shaughnessy, Rutt, Redmond).
3. **The Ten Wings & canonization** (Warring States → Han) — the commentaries that turned
   a manual into a classic; trigram correlations and Han correlative cosmology.
4. **Wang Bi → Neo-Confucian readings** (Zhu Xi's "originally a book of divination" —
   the tradition's own internal honesty moment, a gift to this project's thesis).
5. **Westward** — Jesuit translations, **Leibniz and the binary reading** (flagged:
   resonance, not influence, on the binary system's invention), Legge, then
   **Wilhelm/Baynes + Jung's foreword** — the edition that made the Western I Ching,
   and the direct bridge to this project's psychology essays.
6. **The modern book** — counterculture adoption, contemporary scholarly translations,
   the I Ching as world literature.

### The two wings, ported

- **Record**: `people-of-iching` (King Wen *as figure of legend*, Confucius *as
  attributed editor*, Wang Bi, Zhu Xi, Legge, Wilhelm, Jung…) and `books-of-iching`
  (the translation genealogy as a deck — each major edition one item, with what it
  changed). Both from `research/people/*.md` dossiers via the people-grammar builder.
- **Living**: the casting practices (yarrow-stalk and three-coin as *documented
  protocols* with their different probabilities — a genuinely delightful Research note),
  held under the same shared intention: read to know yourself; relate to the hexagram,
  never obey it.

### The video playlists ("Watch the history" with specialists)

Port tarot's watchlist pattern (the Play page's "Further watching" JSON + the one-line
Claude contribute prompt already documented in Ways to Contribute):

- **Format**: a `watchlist.json` of appropriately-licensed talks/lectures, each entry:
  URL, speaker + credential, one-sentence description *framed as an account of the
  history*, license/embeddability check.
- **Who counts as a specialist**: academic sinologists and historians of the text
  (lecture-circuit and university-channel material by scholars of early China and of
  the book's reception) — the credential is stated on the card; popular practitioners
  can appear only clearly labeled as the Living wing, not as history.
- **Sequencing**: playlist order follows the historical spine above, so watching top to
  bottom *is* the course. Same contribute prompt pattern: paste a URL, Claude verifies
  license, writes the one-liner, slots it, opens the PR.

### Order of work

1. Add repo, audit, port the toolchain (check_all, validate-grammar with the
   grammar.json-only matcher fix from PR #38, channels.html → channel `iching`).
2. Research dossiers for stages 1–3 (the pre-history and core text — where the
   legend-vs-scholarship line does the most work).
3. History course (the spine as one MDX course, tarot's history course as the template).
4. People + books grammars from the dossiers.
5. Watchlist page seeded with a first verified playlist.
6. Stages 4–6 dossiers + the casting-practice grammar; publish and open the channel.
