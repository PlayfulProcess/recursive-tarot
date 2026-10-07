# Coherence pass, Oct 7 2026: the seams left for PlayfulProcess

Branch `sources/oct7`. The mechanical joins are already made in the branch (names, dates, terms,
counts, stale statuses: see the commit "Coherence, mechanical joins only"). What is below touches
your prose, a tradition's words, or a choice only you can make, so nothing here was changed.

Each row: where, the seam, the smallest fix I would suggest. Line numbers are from this branch.

## 1. Your prose: the same argument or opening twice

| # | Where | Seam | Smallest fix |
|---|---|---|---|
| 1 | `course/kant-and-the-tarot.mdx:130–150` and `course/morality-is-an-ecosystem.mdx:11` | Kant's "Where I part ways" now makes the whole emergence case (Hayek, starlings, Gottman, is/ought). Morality then opens "the essay the Kant course promised and then postponed" and repeats it. Both are chapters of `reading-the-cards.mdx`, so a reader meets it twice. | Either cut Kant's section back to its pointer (`:132`), or change Morality's first sentence so it no longer says "postponed". |
| 2 | `marsha-linehan-reads-the-tarot.mdx:15`, `hospicing-modernity-reads-the-tarot.mdx:15`, `non-dual-tantra-reads-the-tarot.mdx:15`, `jung-reads-the-tarot.mdx:15` | Every voice course opens "This is the … voice in a series". Read back to back in `reading-the-cards`, the formula shows. | Vary or drop the opener in two of them. |
| 3 | `intention-setting.mdx:11` and `tarot-and-the-crack.mdx:12` | Two consecutive chapters open "I came to tarot…" / "I came to the cards…". | Change one opening. |
| 4 | `history-of-tarot.mdx:19`, `tarot-today.mdx:15` and `:54`, `tarot-and-the-crack.mdx:16`, `intention-setting.mdx:59`, `divination-traditions.mdx:93`, `index.html:271` | "Tarot began as a 1440s card game" is retold at every entry point. | Trim only where chapters sit next to each other in `reading-the-cards`. |
| 5 | `course/games-of-the-tarot.mdx:22` and `course/booklets/games-of-the-tarot.mdx:22` | Two copies drift: "purpose-built divinatory decks" against "come from genuine divinatory traditions". The booklet (used by the Shop) lacks "Keep digging". | Choose one wording; copy it over. |

## 2. Your prose: dates and claims that disagree with the repo

| # | Where | Seam | Smallest fix |
|---|---|---|---|
| 6 | `course/kant-and-the-tarot.mdx:4`, `:15` | "Etteilla's first fortune-telling decks (1785–91)". The repo has method books 1783–85 and the deck 1788–89 (`research/10a`, `people/etteilla.md`). Your overlap with Kant rests on 1785. | "Etteilla's method books (1783–85) and first fortune-telling deck (1788–89)". |
| 7 | `course/history-of-tarot.mdx:35` | Trumps "half a century later" than the 1370s gives the 1420s; the same page says 1440s at `:19` and `:47`. | "about seventy years later". |
| 8 | `course/_courses.json:7`, `index.html:205` | "Six centuries, from a 1440s card game to the occult reinvention of 1781" (1440s to 1781 is about 340 years). | "…from a 1440s card game, through the occult reinvention of 1781, to today". |
| 9 | `course/history-of-tarot.mdx:49` | Ma Diao as "the oldest card game anyone can still deal". The dossier (`research/decks/madiao-money-cards.md`) corrected this: late Ming, not older than European cards. The same page hedges at `:31`. | "one of the oldest card games whose rules survive". |
| 10 | `course/tarot-today.mdx:60` | Pamela Colman Smith gave the pips "their first fully illustrated scenes". The Sola Busca did it in 1491 (the home page and the tree say so). | "fully illustrated scenes for a deck everyone could buy". |
| 11 | `course/tarot-and-the-crack.mdx:22` | Court de Gébelin "the Swiss pastor". The dossier: Huguenot pastor, birthplace Nîmes or Geneva disputed. | "the Huguenot pastor and scholar". |
| 12 | `history-of-tarot.mdx:49`, `kant-and-the-tarot.mdx:51` | "public-domain decks" for the library. The site says "open" (the images are a mix, see `docs/rights/IMAGE-LEDGER.md`). | "open decks". |
| 13 | `kant-and-the-tarot.mdx:51` | Tarocchino "six-hundred-year-old" (the game dates from c. 1500, about 525 years). | "five-hundred-year-old". |
| 14 | `course/history-of-tarot.mdx:74` | "behind all of them, the Ancestors — Ma Diao, Mamluk, Ganjifa", while describing the Tree of Tarot. The tree has no ancestor nodes (nor Viéville, Paris, the Cary and Rosenwald sheets). | Add the nodes (plan item 5; each line of descent is a claim, so it needs your judgement), or reword the line. |
| 15 | `course/how-tarot-works.mdx:33`, `:92` | Blind tests: "could not reliably pick their own reading", without the caveat `why-a-reading-feels-personal.mdx:39` and CLAUDE.md give (one experiment significant on reanalysis). | Add the clause, or point to the other course. |
| 16 | The history essay embed, from `scripts/build_meta_grammar.py` | "Etteilla builds a cartomancy system from scratch"; `people/etteilla.md:41–46` says his 1770 piquet manual already held the machinery. | "Etteilla carries his card-reading system over to the tarot". |

## 3. Choices only you can make (data and names)

| # | Where | Seam | Options |
|---|---|---|---|
| 17 | Waite's *Pictorial Key* | "(1910)" in `history-of-tarot.mdx:13,15`, `walking-the-golden-dawn-path.mdx:81,99,117`, `pages/sources.html:50`; "(1911)" in the RWS grammar and `books-of-tarot`. The illustrated edition is dated 1911, the unillustrated *Key to the Tarot* 1910. | One label everywhere: "1911", or "1910; illustrated ed. 1911". |
| 18 | Golden Dawn date | Tree "London, 1888"; grammar "1888 · RWS 1909"; `research/12`: order founded 1888, Book T manuscript 1890s; `people/golden-dawn.md`: c. 1891. | "London, c. 1891 (order founded 1888)", or keep 1888 as the order's date. |
| 19 | "Charles VI" | The deck's own metadata says Florence (BnF), but its `common_name` and the meta label say "(Ferrara)", the tree keeps it under the B-order (Ferrara) branch, and the course lists it under Order B (`history-of-tarot.mdx:64`). The editorial note of Jun 13 left the branch "pending a tree review". | Keep B-order with "Ferrara or Florence" (as now), or move it; then make the label "'Charles VI'". |
| 20 | Tarocchino date | Tree "16th c.→" (the game); deck grammar and meta "17th c." (the pack). | "c. 1500+ (this pack 17th c.)", or one of the two. |
| 21 | Ma Diao | The grammar name says "(the Deep Root)" and its date "14th–15th c."; the dossier corrected it to a late-Ming game. | Drop "(the Deep Root)"; date "late Ming (16th–17th c.)". |
| 22 | Anecdotes' lineage | The tree descends it from the Rider-Waite-Smith; the deck's own description and the meta say it descends from the Marseille (its suits are Batons and Coins). | Pick one line of descent. |
| 23 | Home page "Crystal ball" stop | Placed at "1781"; the courses date fortune-telling with the deck to the 1780s (Etteilla). | "1780s", or keep 1781 as the year the idea began. |
| 24 | "Contemporary Decks" branch | New in this branch, with two lines of text I wrote (`tree-of-tarot`, `branch-contemporary`). | Your wording. |
| 25 | Tree years | Each node now has a number for placing it. Broad labels use a century's midpoint ("16th c." = 1550), Lévi 1855 (*Dogme et rituel* 1854–56), "20th–21st c." = 1950. | Change any number in `tarot/tree-of-tarot/grammar.json`; the label (`when`) is what readers see. |
| 26 | Where each deck's date lives | Still three places: the tree, `build_meta_grammar.py`, `refresh_collection.py` (`YEARS`). Charles VI and Anecdotes now agree in all three; the others still differ in places (Minchiate 1550 / 1506, Besançon 1750 / 1800, Golden Dawn 1888 / 1909). | Route (a): the scripts read the tree's year. Route (b): the June `catalog` plan. From the plan in `recursive-eco/docs/future_plan/PLAN-tarot-and-genealogy-timeline-previews-2026-10-07.md`. |
| 27 | The view's name | It is now "Tree of Tarot" everywhere. The plan suggested "Genealogy", but `genealogy.html` already uses that word until it is folded in (plan item 3). | Keep, or rename once `genealogy.html` is archived. |

## 4. Sources found but not added

| Source | Why not |
|---|---|
| Matarese, "Ludus Triumphorum", DiGRA 2025, [dl.digra.org](https://dl.digra.org/index.php/dl/article/view/2437) | Free, but no licence stated; dates tarot "presumably around 1410-1420", against the repo's 1440s. Worth a look as a counter-voice. |
| Auger, "Women Tarot Artists Inspired by the Golden Dawn", *Mythlore* 40(1), 2021, CC BY-NC-ND, [dc.swosu.edu](https://dc.swosu.edu/mythlore/vol40/iss1/16/) | A review essay, not history; could go on Pamela Colman Smith's page. |
| Juliette Wood, "Secret Traditions in the Modern Tarot", [juliettewood.com](http://www.juliettewood.com/papers/Tarot.pdf) | On the author's site; publication venue not found. |
| Olsen, *Carte da Trionfi*, PhD, Pennsylvania 1994 | Only the abstract is confirmed free. |
| IPCS pattern sheets beyond PS001 ([index](https://www.i-p-c-s.org/wp/italian-suited-tarot-pattern-sheets/)) | Bolognese and Belgian sheets are already cited; the Milanese, Piedmontese, Swiss and Besançon sheets could join their decks. |
| Pratesi's other free papers on naibi.net (Florence 1376/77; Ferrara's Lollio poem) | For the origins and Ferrara pages, once their original venues are confirmed. |

Free full text of Dummett's own books and of the Mamluk studies (Mayer 1939; Dummett and Abu-Deeb
1973) was not found; copies on Scribd or archive.org look unauthorised and were left out.
