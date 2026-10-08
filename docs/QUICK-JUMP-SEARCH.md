# Quick-jump search

The search box in the site header (every page with `<site-header>`). Type a card, a deck, a numeral
or a chapter word; the results open in the site's own views. No AI and no server: the browser
matches words against a small static index.

| Piece | What it is |
|---|---|
| `search-index.json` | **Generated. Never hand-edit.** About 2,200 rows: every card of every deck, one row per deck, one "across every deck" row per trump and minor card, the people and books of the sources, every course and every `##`/`###` heading in it, and a few site pages. ~430 KB, ~70 KB gzipped; fetched on first use only. |
| `scripts/build_search_index.py` | Builds it from `tarot/<slug>/grammar.json` and `course/*.mdx`. `--check` exits 1 if the committed file is stale. |
| `quick-jump.js` | The ranking engine (browser and Node). Loaded by the header on first use. |
| `site-header.js` | The box, the results panel (desktop) and the full-width sheet (phone, behind the search icon). |

## It cannot go stale

- `python scripts/check_all.py` rebuilds it (with people + meta), so every commit that follows the
  repo rule carries a fresh index.
- `.github/workflows/build-meta.yml` rebuilds it on every push to `main` that touches `tarot/**` or
  `course/*.mdx`, and commits it with the meta grammar. This covers the recursive.eco sync PRs too.

## Where results open

| Row | Opens |
|---|---|
| Card, person, book | `viewers/cards.html?src=../tarot/<slug>/grammar.json&item=<id>` (the card's own modal) |
| Deck | `viewers/cards.html?src=../tarot/<slug>/grammar.json` |
| Across every deck | `viewers/prototypes/lenses.html?card=<trump_key or minor_key>` (Lenses, the same link the courses use) |
| Course / section | `pages/course-viewer.html?course=<id>#<anchor>`; the anchor is computed the way the course viewer computes heading ids (h2s first, then h3s, `-2` for twins) |

## How it ranks

Each query word scores by where it matches: the row's own name (10), its aliases (9), its deck or
course (5), a weaker relation (3). Matching every word adds 15. Words that name a deck ("golden",
"dawn", "rws") narrow; when a card's own name or aliases carry all the other words, that card sorts
first whatever its deck. So `justice golden dawn` gives the Golden Dawn Justice, then Justice across
every deck (Lenses), then Justice in each deck, then the chapters.

Aliases come from the data: the trump's name as the meta build reads it (`major_from_name`, so
*La Giustizia* and *La Justice* are Justice), its Thoth-era names (Adjustment, Lust, Art, Aeon,
Universe), the deck's own numeral (arabic and roman: Golden Dawn Justice is XI, Marseille's is VIII),
suit and rank words in the decks' languages (Coins = Pentacles = Denari), and short metadata
(Hebrew letter, sign, Golden Dawn title). A named figure that only sits in a trump's numbered place
(Minchiate's Hunchback at 11, Sola Busca's Tulio) is related to that trump, not named as it, so it
ranks below the real Justice cards.

Short words, numbers and roman numerals match whole words only (`xi` is not `xii`); longer words
match the start of a word, so results appear while typing.

Keys: `/` or Ctrl/Cmd+K focuses the box; arrows move; Enter opens (Ctrl/Cmd+Enter in a new tab);
Escape clears, then closes.

## Later: the recursive.eco assistant can use the same index

The assistant does not need a model to find a card. It can call the same index as a tool:

```js
// Node (or a Worker): no AI involved in the search itself
const qj = require('./quick-jump.js');
const idx = qj.prepare(await (await fetch('https://tarot.recursive.eco/search-index.json')).json(),
                       'https://tarot.recursive.eco/');
qj.search(idx, 'justice golden dawn', 10);
// -> [{ kind: 'c', title: '11 — Justice', sub: 'Golden Dawn (Book T)', href: 'https://tarot.recursive.eco/viewers/cards.html?...' }, ...]
```

A `tarot_search(query)` tool built this way costs nothing per call; the model only reads the
returned rows and links. Not built yet: it belongs in recursive-eco, behind the existing assistant
tool list.
