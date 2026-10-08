# Future ideas — held for the great simplification

PlayfulProcess, Oct 8 2026: "lets not work on new code of tarot for now, just new content ...
wait for the great simplification". These are her ideas from that day, kept here so they do not
get buried. None is started. Each says what it would touch, so the simplification can decide
where it lives.

Where her words reached this file verbatim they are in quotation marks. The rest were relayed
in a summary, and are marked *(relayed)*: check the wording with her before quoting them.

| | Idea | Date | Status |
|---|---|---|---|
| 1 | Walk every path of the Tree, screen by screen | Oct 8 2026 | held for the great simplification |
| 2 | A reading as a spread on the Tree | Oct 8 2026 | held for the great simplification |
| 3 | A Golden Dawn landing page | Oct 8 2026 | held for the great simplification |
| 4 | Astrology icons on the cards | Oct 8 2026 | held for the great simplification |
| 5 | "Watch: the making of the deck and its artist" as a playlist grammar | Oct 8 2026 | held for the great simplification |
| 6 | Markdown that does not render in the course viewer | Oct 8 2026 | held for the great simplification |
| 7 | The cards viewer repeats numbers | Oct 8 2026 | held for the great simplification |
| 8 | Retire the site's cards viewer for recursive.eco Play's Cards view | Oct 8 2026 | held for the great simplification |

## 1. Walk every path of the Tree, screen by screen

*(relayed)* Walking every path of the Tree of Life as a sequence of screens, the way the I Ching
path walks its hexagrams.

- Touches: `pages/tree-of-life.html` (the map), the Golden Dawn course
  (`course/walking-the-golden-dawn-path.mdx`), the Keys of `tarot/book-t/grammar.json`.
- Could be content first: a sequence grammar of the 22 paths, one item per path, if the
  simplification gives sequences a walk view.

## 2. A reading as a spread on the Tree

*(relayed)* A reading laid out as a spread on the Tree, with the drawn cards listed below it,
offered when someone casts the Golden Dawn / Book T deck.

- Touches: the Caster (`viewers/caster-studio.html`) and the map, which already lights paths from
  `?cards=` (`pages/tree-of-life.html`).
- Keep the site's creed at the cast: a gate, not a fate.

## 3. A Golden Dawn landing page

*(relayed)* A page for the Golden Dawn itself:

- its importance;
- its contradictions: it claimed to invent while claiming ancient authority;
- members burned their own decks, while the Rider-Waite-Smith deck went the other way and became
  the best-known deck;
- thumbnails to all the resources (the decks, Book T, the map, the course, the glossary);
- the glossary as its hero section;
- maybe a second header row inside Golden Dawn content only;
- it must still render on recursive.eco.

Touches: a new page under `pages/`, `pages/glossary.html`, `pages/golden-dawn-decks.html`, the
course chapter "Where the cards went" (`course/golden-dawn-where-the-cards-went.mdx`).

## 4. Astrology icons on the cards

*(relayed)* Astrology icons on the cards, fed from the astrology grammar. For now they would
render what the Golden Dawn itself meant: the sign, planet or element Book T gives each card.

- Data is already there: `metadata.attribution`, `decan`, `planet`, `sign`, `element` on
  `tarot/book-t/grammar.json` and `tarot/golden-dawn-book-t-tarot/grammar.json`.
- The reading page (`pages/book-t.html`) already draws these glyphs as text, never emoji.

## 5. "Watch: the making of the deck and its artist" as a playlist grammar

*(relayed)* The course section "Watch — the making of the deck and its artist"
(`course/walking-the-golden-dawn-path.mdx`) becomes a playlist grammar, iframed in the course.

## 6. Markdown that does not render in the course viewer

*(relayed)* Some markdown does not render in the course viewer (`pages/course-viewer.html`).
Which constructs fail is not yet listed: collect examples before fixing.

## 7. The cards viewer repeats numbers

*(relayed)* The cards viewer shows a card's number twice, as in "11 — 11 — Justice": the number
badge, then a name that already starts with the number.

- On content, Book T's own deck (`tarot/book-t/grammar.json`, Oct 8 2026) keeps the number in
  `metadata.number` only and names each card by its title. Other decks still put the number in
  the name ("11 — Justice").
- The fix belongs to the simplification: either the viewer stops prefixing, or the names drop
  the number, in one pass across the decks.

## 8. Retire the site's cards viewer

*(relayed)* Retire the site's cards viewer (`viewers/cards.html`) in favour of recursive.eco
Play's Cards view.

- Every "Open in [deck]" pill, course link and the reading page link to `viewers/cards.html`
  today: list them before the switch (`grep -rn "cards.html" --include=*.html --include=*.mdx`).
