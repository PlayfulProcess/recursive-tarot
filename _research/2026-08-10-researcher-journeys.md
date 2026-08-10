# Researcher journeys — testing the Explorer against real tarot scholarship

*2026-08-10. Read-only research pass. Prompted by Fernando's north star for the Emergence
Explorer ("something scholars or artists could use to compare and inspire themselves") and two
verbatim asks: "Can you come up with what artist or historians would want to investigate and see
if they can navigate towards that?" and "Maybe we can create a course... test the lineages
hypothesis iconographically." This file is Part 1: six concrete research questions, each
navigated against the live tool and the underlying data. Part 2 (the course seed) is the
companion file, `2026-08-10-course-seed-iconographic-lineages.md`.*

## Method

I cannot click. What follows is not a guess — for each question I traced the exact code path in
`viewers/explorer.html` and `viewers/dimension-engine.js` (the pivot engine), cross-checked
against `scripts/build_meta_grammar.py` (which generates `tarot/all-decks-many-lenses/grammar.json`,
the file the default Explorer view loads), and then **queried the actual generated JSON** to see
what a real click would actually render — same data the live site serves (spot-checked against
`https://tarot.recursive.eco/tarot/_collection.json`, which matches the local repo exactly:
`c-order` deck_slugs = `["tarot-de-marseille-conver", "tarot-de-besancon"]`, `roots` =
`["visconti-sforza-tarot", "cary-yale-visconti-tarot", "noblet-tarot", "cary-sheet",
"rosenwald-sheet"]`, verbatim). Where I say "row 8 shows X," that is read directly off the
generated grammar, not inferred.

One fact governs everything below: **the default landing view (Trump × Deck) is built from
exactly 13 decks** — `scripts/build_meta_grammar.py`'s `DECKS` dict, verified by extracting every
distinct `deck` value with `role: "trump"` from the meta-grammar: Visconti-Sforza, Cary-Yale
Visconti, 'Charles VI' (Ferrara), Minchiate, Tarocchino di Bologna, Tarot de Marseille (Conver),
Tarot de Besançon, Court de Gébelin, Etteilla I/II/III, Oswald Wirth, Golden Dawn (Book T). Every
other deck in the collection — **Sola Busca, Mantegna, Rider-Waite-Smith, Papus, the Cary Sheet,
Rosenwald Sheet, Noblet, Viéville, Belgian, Paris-Anonymous, d'Este, Ganjifa, Mamluk, Ma Diao,
Petit Lenormand**, and every "living"/"community"/"contemporary" deck — **is invisible to the
Trump × Deck wall and to every preset button**, because those buttons need `trump_number` /
`role` / `order`, fields that only exist inside this one generated file, computed only for these
13 decks. A researcher reaches anything outside that set only through the "✦ Decks ▾" multi-select,
which loads raw per-deck `grammar.json` files with none of that derived scaffolding. This single
fact is the spine of several verdicts below.

## The six verdicts, at a glance

| # | Question (researcher's own words) | Verdict |
|---|---|---|
| 1 | Do Dummett's three trump-orders (A/B/C) show up as trustworthy, distinct families? | **PARTIALLY** — the labeled preset is broken on the default view; even the manual workaround can silently misplace a card |
| 2 | Can I see the Golden Dawn's Strength/Justice swap against the Marseille standard? | **PARTIALLY** — the comparison itself is easy; the fact that makes it interesting is invisible |
| 3 | Do Bologna's four un-ranked Papi and Cary-Yale's three added Virtues show up as the honest exception they are? | **PARTIALLY** — found, but the row conflates real history with a data bug |
| 4 | Does Minchiate's expansion past the standard 22 read as visibly "extra," not silently lost? | **NAVIGABLE TODAY** (with one caveat proven by finding #1) |
| 5 | Does the 1781–1909 "occult turn" read as a functional break, not just a date range? | **NAVIGABLE TODAY** |
| 6 | Can I compare Sola Busca's uniquely-named trumps and scenic minors against the standard decks? | **NOT SUPPORTED** for the headline comparison; **PARTIALLY** for a manual workaround |

---

## 1. "Do Dummett's three trump-orders (A, B, C) actually separate into distinguishable regional
families here — and can I trust where a card lands?"

This is the first thing a Dummett-school historian would try: *A. Game of Tarot* (1980) established
that the surviving early decks number their trumps in three regional patterns, disagreeing mainly
about where to slot the three Virtues. The site's own history course frames this as "the single
cleanest piece of evidence that tarot was a game that acquired meaning."

**Attempt.** The Explorer ships a preset for exactly this: **"Lineage ▸ Deck"** (`data-r="branch,deck"`).
On the default landing page (the meta-grammar, no `?decks=` param), I traced what happens when it's
clicked: the preset code filters `data-r` against `avail`, the set of fields the *currently loaded*
grammar actually has. The meta-grammar's cards carry `order` (A/B/C/occult, from `CLASS` in the build
script) but **no `branch` field at all** — `branch` (roots/a-order/b-order/c-order/occult/sui-generis/
ancestors) is only inherited when loading decks via the multi-select, from `_collection.json`. So
`avail.has('branch')` is false, the preset's own filter silently drops it, and you're left with
`rows=['deck']`, no columns, no grouping — a flat list, nothing resembling "Lineage." No error, no
disabled state on the button; it just doesn't do what its label promises, on the very view most
first-time visitors land on.

The real path exists, just not behind that button: drag the **`order`** chip (which *is* present,
A/B/C/occult, 4 values) into Rows, and `deck` into Columns. `inferHierarchy` even nests them into
one visual chain in the tray (`order ▸ deck`), which is a nice unadvertised affordance. Doing this
does separate the 13 decks into four real families.

But then a second problem, found by checking Minchiate's own data against what the pivot shows:
Minchiate's raw grammar already carries a hand-researched `trump_number` for its four "Papa" cards
— Papa One→1, **Papa Two→5**, Papa Three→4, Papa Four→4 (a real Florentine A-order clustering,
matching the Bolognese dossier's note that "the three Virtues sit clustered in the middle of the
sequence"). The meta-builder ignores that field and recomputes its own from the raw catalog
`number` field instead (`m.get("number")`), giving Papa Two `trump_number = 2`. So in the generated
meta-grammar, **"Papa Two (the Grand Duke)" sits in row 2 — The Magician's row — not row 5**, where
the deck's own metadata says it belongs. This is exactly the kind of card an art historian testing
the A-order clustering hypothesis would be looking at, and the tool silently mis-shelves it.

**Verdict: PARTIALLY.** The one-click path is mislabeled/non-functional on the default view; the
working manual path (drag `order` → Rows) exists but isn't discoverable without reading the code,
and even it inherits a real placement bug for at least one card. Smallest fix: (a) have the preset
fall back to `order` when `branch` isn't available, and (b) make `build_meta_grammar.py` prefer a
source item's own `metadata.trump_number` over the raw `number` fallback when present.

---

## 2. "The Golden Dawn/Rider-Waite-Smith famously swapped Strength and Justice — VIII and XI —
relative to the Marseille standard. Can I see that swap?"

This is the single most-cited case study in trump-order history, and it's already narrated (hedged
appropriately) in this repo's own Golden Dawn course.

**Attempt.** Verified directly in the source decks: Tarot de Marseille (Conver) prints **"8 — La
Justice"** and **"11 — La Force" (Strength)** — the historical default. Golden Dawn (Book T) — whose
images are the actual RWS scans — carries **"8 — Strength"** and **"11 — Justice"** in its own
metadata: the deliberate occult-era reversal (moving Strength to VIII so the trump sequence tracks
the zodiac from the Emperor onward). The default Trump × Deck wall (no clicks needed — this *is*
the landing page) puts every deck's Strength card in row 8 and every Justice card in row 11,
because `build_meta_grammar.py` assigns `trump_number` by matching the card's **name** to a
canonical archetype list, not by trusting each deck's own printed digit. So row 8 genuinely shows
"the Strength archetype" side by side across all 13 decks — Marseille's *La Force* card sits there
next to Golden Dawn's *Strength* card, which is a real, useful comparison.

The trap: nothing in the row, the card, or its detail panel tells you that the numeral printed on
each of those two cards disagrees. The Explorer's own `number` field (the same value it derives
for `trump_number`) is *already* the canonicalized/renamed number — the deck's actual printed
Roman numeral is nowhere surfaced. The detail panel's field list (`level, deck, source_deck,
century, order, branch, suit, rank, function, print quality`) does not include `number` at all. So
a researcher looking at row 8 has no way, from inside the Explorer, to learn that Marseille's card
sitting there is inscribed **XI** while Golden Dawn's is inscribed **VIII** — the exact fact that
makes this the textbook example. You'd have to click through the "Open in [deck] →" pill to the
source deck and read the roman numeral off the card image itself.

**Verdict: PARTIALLY.** The archetype-level comparison is **NAVIGABLE TODAY**: it's the default
view, no clicks required, scroll to rows 8 and 11. The numeral-swap fact itself — the actual
historical event — is **NOT SUPPORTED**: nothing in the UI states or preserves each deck's own
printed number. Smallest fix: add the deck's raw `metadata.number` as a small label on each card
pill (e.g. a corner badge "printed: XI") and/or add `number` to the detail panel's field list.

---

## 3. "Which trumps refuse a single fixed slot altogether — Bologna's four interchangeable Papi
(later censored into the four Moors by papal edict in 1725) and Cary-Yale's three added
theological Virtues (Faith, Hope, Charity)? Does the tool show that refusal honestly?"

**Attempt.** The Trump × Deck wall sorts rows numerically with one deliberate, documented exception:
`smartCmp` in `dimension-engine.js` always sorts the "—" (no-value) bucket **last**, with a code
comment explaining exactly why — "Bologna's four equal-ranking Papi carry no trump number; that is
the deck, not a gap." That's good design: the missing-value row is honestly labeled rather than
silently dropped (`dashLabel` renders it as "— (no trump_number)").

Scrolling to that row and reading its actual contents: for **Tarocchino di Bologna** it holds
*Papa (Moor) I–IV* — correct, these are the genuinely rank-less Papi (the deck's own item names
already reflect the 1725 edict that turned the four Popes into four Moors, per the research
dossier's account of that episode). But the same row also holds **"Love"** and **"The Old Man
(Time)"** — two cards that are *not* rank-less by design; they simply failed to match the
canonical-name regex (the list only recognizes "hermit"/"il tempo," not the English gloss "The Old
Man (Time)"; only "lovers," not "Love"). For **Cary-Yale Visconti** the row correctly holds *Faith*,
*Hope*, *Charity* — nothing miscategorized there.

So the row is real and findable, but it mixes a genuine historical fact (Bologna's Papi are
by-design interchangeable) with an unrelated data bug (two mistranslated card names), with no way
inside the Explorer to tell which is which — the cell just shows five or six pills together, all
equally "no trump number."

**Verdict: PARTIALLY.** Navigable to *find the phenomenon exists*: it's the bottom row of the
default Trump × Deck view, one scroll. Not navigable to *trust what you're looking at* without
independent knowledge — a researcher who doesn't already know Bolognese history would have no way
to separate the two genuine Papi-related decks' honest gaps from Bologna's two accidental
misses. Smallest fix: widen the English-name patterns in `major_from_name` (add "love," "the old
man," "time") so the dash row holds only the cards that are *actually* unranked by history, not by
translation gap.

---

## 4. "Minchiate expands the standard 22 trumps to a 97-card deck — zodiac signs, elements, extra
virtues. Does that expansion show up as visibly *extra*, or does it get folded invisibly into the
standard sequence?"

**Attempt.** Checked directly: Minchiate's cards populate `trump_number` 0, 1, 2, 4, 5, 7, 8, 10–21
(the standard range, gappy — see finding #1 above on why some of those gaps and one misplacement
exist) **and then 22 through 35** — Earth, Air, Libra, Virgo, Scorpio, Aries, Capricorn, Sagittarius,
Cancer, Pisces, Aquarius, Leo, Taurus, Gemini. `smartCmp` sorts numerically, so these land, correctly,
as a visible tail *after* row 21 in the Trump × Deck wall — every other deck's column reads empty
("·") for rows 22–35, which is itself the honest signal: *only Minchiate goes here.* No dedicated
UI language calls this out ("Minchiate's extension" or similar), but the shape is legible on sight:
the table visibly runs 14 rows past where every other column stops.

**Verdict: NAVIGABLE TODAY.** Default landing page, scroll past row 21 — the extension is there and
correctly isolated to Minchiate's column. The caveat is finding #1's, not new to this question: a
couple of Minchiate's standard-range trumps (the "Papa" cluster) land at the wrong standard-range
row, so *this* headline shape (the 14-row zodiac tail) is trustworthy, but a full 97-card structural
audit of Minchiate against the standard 22 is not, for the same reason as #1.

---

## 5. "Does the 1781–1909 occult reinterpretation read as a genuine functional break in how the
cards were used — game, then origin-myth, then purpose-built divination, then esoteric system — or
just as a run of later dates?"

**Attempt.** `build_meta_grammar.py`'s `CLASS` dict tags every one of the 13 decks with a documented
`function`: **game** (Visconti-Sforza, Cary-Yale, Charles VI, Minchiate, Tarocchino, Marseille,
Besançon), **origin-myth** (Court de Gébelin, 1781 — the invented Egyptian claim), **divination**
(the three Etteilla decks, 1788–1865 — purpose-built cartomancy), **esoteric** (Oswald Wirth, Golden
Dawn — the correspondence systems). This maps almost exactly onto the site's own history-course
narrative of the divination question, but as a filterable field rather than prose.

From the default landing page: click the **✕** on the `trump_number` chip in Rows to remove it,
drag the **`century`** chip into Rows, drag the **`function`** chip into Columns (which replaces
`deck`). Two drags. (Optional: also clear the `role: trump` filter pill so pip/court cards count
too — with it left on, the comparison still works, just restricted to trumps.) The resulting table
puts "game" cards almost entirely in the 15th–18th-century rows and "origin-myth"/"divination"/
"esoteric" cards almost entirely in the 18th–19th/20th-century rows — the functional break tracks
the chronological one cleanly, because the underlying `CLASS` classification was hand-curated to
match documented use, not guessed from dates.

**Verdict: NAVIGABLE TODAY.** No preset button exists for this specific pivot, but the two fields
it needs are both present and well-populated, and reaching it is two drags from the default view —
well inside what a first-time visitor would find by exploring the drag targets, if not by
one-click discovery.

---

## 6. "Sola Busca (1491) is tarot's strangest deck — Roman/mythic trump names instead of the usual
cast, and the first tarot with fully illustrated pip cards, which several historians think Pamela
Colman Smith studied (via British Museum photographs, 1907–08) before drawing the Rider-Waite-Smith
minors. Can I compare Sola Busca's cards against the standard decks to weigh that resemblance?"

**Attempt.** Sola Busca is **not one of the 13 decks in the meta-grammar's `DECKS` dict**, and it's
also absent from the separate `ANCESTORS` list (Mamluk, the Cary Sheet, the Rosenwald Sheet, Noblet,
Ganjifa) that at least gets surfaced on the genealogy timeline. It is simply not present anywhere in
`tarot/all-decks-many-lenses/grammar.json` — no card, no deck node. So the default Trump × Deck wall,
every preset button, and every field the meta-grammar derives (`trump_number`, `role`, `order`,
`function`) are unreachable for it: **Sola Busca cannot appear as a column in the comparison wall at
all, under any pivot.**

The only path is the "✦ Decks ▾" multi-select — tick Sola Busca and, say, Golden Dawn (Book T, whose
images *are* the RWS scans), click Load. This loads both decks' raw `grammar.json` files directly,
bypassing the meta-grammar entirely, so none of `trump_number`/`role`/`order` exist here either —
only whatever raw fields each deck's own authors happened to use. Checked directly: Sola Busca's
minors carry `metadata.suit: "Batons"` (its actual period-accurate suit name); Golden Dawn's carry
`metadata.suit: "Wands"`. `dimension-engine.js`'s `flatten()` copies these verbatim with no
normalization (that normalization, `suit_norm()`, exists only inside the meta-builder, never applied
to raw multi-select loads). So a Suit × Rank pivot built this way would put Sola Busca's Batons cards
and Golden Dawn's Wands cards in **separate, non-adjacent columns** — exactly the side-by-side
comparison the researcher wants, broken by an un-normalized label, not by missing data. (A raw
`number` field does exist on both decks' items, so a manual `number` × `deck` pivot is possible and
would at least align the *trumps* by position — with the caveat from #1 and #2 that "position" here
means each deck's own printed sequence, not a cross-checked archetype identity, since neither deck
went through the meta-builder's name-canonicalization.)

**Verdict: NOT SUPPORTED** for the headline ask (Sola Busca inside the Trump × Deck wall, or any
preset) — smallest fix: add `sola-busca-tarot` to `DECKS` in `build_meta_grammar.py` (its trumps are
numbered 0–21 with `arcana: "major"` already, so the pipeline would very likely need only suit-name
handling for the minors, which `suit_norm()` already covers via the `bastoni|baton` pattern —
"Batons" would normalize to "Wands" automatically once the deck enters the builder). **PARTIALLY**
for the manual multi-select workaround, which reaches the deck but drops suit-name alignment on the
floor without telling you it did.

---

## Top navigation gaps, ranked by how much they block real research

1. **Sola Busca (and every non-meta deck) is invisible to the entire comparison-wall mechanism.**
   This blocks not just Q6 but *any* question that wants to set a sui-generis, ancestor, or
   post-1781-non-CLASS deck (Rider-Waite-Smith itself, Papus, the Cary Sheet, Noblet, Viéville…)
   against the 13-deck core. It's a hard wall, not a rough edge, and it's the single biggest reason
   the tool undersells its own collection — the repo holds far more relevant material than the
   default view can ever show.
2. **The row/column position in the meta-grammar can silently disagree with a deck's own
   hand-researched placement** (finding #1, Minchiate's Papa Two) and **never states a deck's own
   printed number once it's been canonicalized** (finding #2, the Strength/Justice swap). Both are
   "the tool shows you an answer that looks authoritative but quietly isn't the full picture" —
   more dangerous than an obvious gap, because nothing signals that anything was normalized away.
3. **The "Lineage ▸ Deck" preset silently does the wrong thing on the default view instead of
   failing loudly or falling back.** Lower-ranked than 1–2 because a working manual path exists
   (drag `order` → Rows) — but it's exactly the button a first-time visitor would reach for to ask
   the Dummett-order question, and it quietly gives them nothing resembling what it promises.

## Files

- This file: `_research/2026-08-10-researcher-journeys.md`
- Companion: `_research/2026-08-10-course-seed-iconographic-lineages.md`
