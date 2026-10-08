# Courses review, Oct 8 2026: what is left for PlayfulProcess

Branch `due/oct8`. Every course page in `course/` was read for factual errors (the anthology
`reading-the-cards.mdx` is built from the chapters, and Case's 1920 booklet is a source text, so
neither was read on its own). Clear factual slips were corrected in the smallest way, keeping your
sentences: the commit "Courses: clear factual corrections only" lists each one. What is below is a
choice, a rewording, or a claim I could not settle, so nothing here was changed.

Line numbers are from this branch. "Unverified" means the reviewer's own knowledge, not a source
read here: check before acting.

## Applied in this branch (for your check)

- `kant-and-the-tarot.mdx:21`: "a working philosopher of fifty-seven ... Etteilla, printing decks
  built to predict, four years after Court de Gébelin" now reads "of about sixty ... Etteilla,
  publishing his method for them two to four years after". Kant was 57 in 1781 and 61 in 1785;
  Etteilla's method books are 1783–85 and his deck 1788–89. This one changes more than a word, so
  look at it first.
- From `COHERENCE-2026-10-07.md`: rows 6–13, 15 and 16 are applied. Rows 1–5, 14 and 17–27 are
  still open there and are not repeated here.

## Decisions, Oct 8 (branch `course/review-decisions`)

PlayfulProcess asked for the 38 items to be decided rather than handed back. Each was checked
against a source and then applied, or dropped with a reason. Only facts were changed in her
sentences; where a fix is applied, the course grammar that mirrors the page
(`tarot/<course>-course/grammar.json`) and the anthology `reading-the-cards.mdx` carry the same
words. The tables further down are the original list, kept as the record.

| # | Decision | Source |
|---|---|---|
| 1 | Applied: "nearly nine hundred miles away" (great-circle distance Königsberg to Paris is about 870 miles; the review's 950 was too high). | Coordinates of the two cities |
| 2 | Applied: "unregulated for five years, and only began to rein in the *bets* with a law signed at the end of 2023. By mid-2024". | Lei nº 14.790, de 29 de dezembro de 2023 (planalto.gov.br) |
| 3 | Applied: "never overcharges an inexperienced customer, not even a child". | Kant, *Groundwork* 4:397 |
| 4 | Applied: 1948 for the class, 1949 for the paper (`why-a-reading-feels-personal`, `how-tarot-works`); `kant-and-the-tarot` already said 1948. | Forer (1949) for the paper; the 1948 class date as in `research/why-tarot-works/REPORT.md:135` |
| 5 | Applied: winners and accident victims "rated their happiness far closer to that of people who had been through neither than anyone expected". | Brickman, Coates and Janoff-Bulman (1978): a comparison with controls, no before-measure |
| 6 | Applied: "about twenty thousand people" in both courses. | `research/why-tarot-works/does-tarot-predict.md:241` (~22,500 tosses) |
| 7 | Applied: "In the original analysis, across the study's three experiments, they did not". | Blackmore (1983); Markwick (1988) as the page already says |
| 8 | Dropped: "disturbed" stays. Hyman's own account of reading palms against the lines says his readings stayed as successful, "to my surprise and horror". | Hyman, "Cold Reading" (1977), as quoted in his TAM workshop manual and in secondary accounts |
| 9 | Applied: the Zeitlyn sentence now links his essay, which says that when divining about an illness one should not ask "Will this person die?". | Zeitlyn, "In Cameroon, truth-telling spiders untangle the future", *Aeon*, 28 July 2025 |
| 10 | Koch applied: "the standard modern guide to the first-millennium texts" (the book's subtitle is *Sources from the First Millennium BCE*). "None copying the others" dropped: the three practices named (Mesopotamian omen texts, Shang plastromancy, the Delphic oracle) are not known to derive from one another; Greek liver-reading is a different practice from Delphi. | Koch (2015), GMTR 7, Ugarit-Verlag |
| 11 | Applied: "Lots and marked staves (Tacitus says *notae*, marks; he does not say runes)". | Tacitus, *Germania* 10 ("notis quibusdam discretos") |
| 12 | Applied: "The **oldest** written layer". | Unwritten scapulimancy predates the Shang inscriptions |
| 13 | Applied: "an Italian court card game of the 1440s". | Pratesi (1989), in `research/bibliography.bib`: early mentions from Ferrara, Bologna and Milan |
| 14 | Applied at both places: "nobody is recorded using it to divine anything for about another three hundred years"; "some three centuries before anyone is recorded using it for divination". | The Bologna sheet of tarocchino meanings, before 1750 (Pratesi 1989; Dummett: first half of the 18th century) |
| 15 | Applied: "who offered no evidence for". | `research/people/court-de-gebelin.md` |
| 16 | Applied: "vinyl revenue crossed a billion dollars in 2021 for the first time since 1986". The "nineteenth consecutive year" for 2025 is consistent with RIAA's count (2021 was the fifteenth). | RIAA 2021 year-end report, as reported by Variety and Billboard, March 2022 |
| 17 | Dropped: the course stands. Krans's own site and the press describe a 2012 self-published deck; no Kickstarter campaign was found. The Kickstarter line in `research/17-contemporary-tarot.txt` is unsupported (that file is a raw transcript, left as is). | kimkrans.com/the-wild-unknown |
| 18 | Applied: "and fought there until the war ended". Sources differ on whether he joined in late 1943 or 1944, so no length is given. | Encyclopedia entries disagree; the end date (April 1945) does not |
| 19 | Applied: "who directed the design of the Rider-Waite-Smith deck". | `research/people/a-e-waite.md`, `tarot-today.mdx:60` |
| 20 | Applied: `:35` "made in China". | `research/decks/madiao-money-cards.md` |
| 21 | Applied: "In most packs, for centuries, the numbered cards ..." (`:110`) and "abstract patterns in most packs for centuries, then, in the Sola Busca of 1491 and again from 1909, little figured scenes" (`:118`). | Sola Busca 1491; RWS 1909 |
| 22 | Applied after the section 3 check (below): RWS is the first known deck to print VIII Strength, XI Justice; Book T's 1912 printing keeps 11 and 8. The sentence now links `research/synthesis/strength-justice-numbering.md`. | See section 3 |
| 23 | Applied: "though no European cardmaker need ever have copied a Mamluk deck directly". | The Mamluk pack is a transmission, not a known model |
| 24 | Applied: "by the later 1400s in most packs". | Minchiate has forty trumps; the 1440s packs are incomplete |
| 25 | Applied: "northern Italian card game"; "the 1781 occult reframing that invented occult tarot divination". | Pratesi (1989); the Bologna sheet (item 14) |
| 26 | Applied: "were likely modelled in part on the 1491 Sola Busca", as `same-card-every-deck.mdx:55` hedges. | `research/decks/sola-busca-tarot.md` |
| 27 | Applied: Ma Diao "a deep documented root of the suited pack ... One of the oldest card games whose rules survive", the badge "A root"; "genuine open deck". | `research/decks/madiao-money-cards.md:24-32`; `docs/rights/IMAGE-LEDGER.md` |
| 28 | Applied: "*pathworking*: the name the Order's heirs gave to a contemplative practice" (`:13`) and "what the Order's heirs came to call **pathworking**" (`:49`). The description (`:4`) and `:65` are the course's own stance and stay. The Order's own visionary practice ("spirit vision") is left out: not checked in a primary source. | Book T (1912) has no pathworking |
| 29 | Applied: "printed in 1912 as 'A Method of Divination by the Tarot', now usually called the 'Opening of the Key'". | *The Equinox* I(8), 1912 |
| 30 | Applied: "set down, mainly by Mathers, ... circulated to initiates and unpublished until *The Equinox* printed it in 1912". | `research/people/macgregor-mathers.md` |
| 31 | Applied: confirmed that the sacred-texts link is Mathers's own 1888 booklet *The Tarot* (its chapters are "Symbolism of each of the Keys" and "Meanings of the Cards"). The reading list now points to the 1912 scan and a transcription for Book T, and names the 1888 booklet separately. The archive.org item `the-book-t-the-tarot` was dropped: it is a 2023 upload compiled from the online *Equinox* transcription, not an Order manuscript. | archive.org metadata; mr-kaplan.com transcription of the 1888 text |
| 32 | Applied: the quotation now has Linehan's words ("... It is almost always quiet. It has a certain peace."), checked against secondary sources that quote her 1993 skills manual (the manual itself not seen). `:71` now says "(in my reading of her skills, not her words)". | dbtselfhelp.com and others quoting Linehan (1993) |
| 33 | Dropped: the labels describe different things. Two epigraphs are paraphrases; the post-activism one is a phrase he uses. A single wording is a style choice for PlayfulProcess. | |
| 34 | Applied: "Vanessa Machado de Oliveira (who has also published as Vanessa Andreotti)" in the epigraph, then "Machado de Oliveira"; the same name in `intention-setting.mdx` and `viewers/voices.json`. | *Hospicing Modernity* (North Atlantic Books, 2021), by Vanessa Machado de Oliveira |
| 35 | Applied: one sentence under the heading, "(The phrase is Donna Haraway's, from her book *Staying with the Trouble*, 2016.)". | Haraway (2016), Duke University Press |
| 36 | Applied: "made with the recursive.eco MCP (run head-less in Claude Code; the same calls work from Claude Desktop)". | `research/build-logs/grammar-audit-mcp-2026-06-20.md:165` |
| 37 | Applied: the link pointed back to this same course through a stub. Now "read on: the rest of this course walks through each route." | `course/build-a-tarot-deck-with-claude.mdx` (the stub) |
| 38 | Applied: "scanned historical art, open to use (see the image ledger)", with a link. | `docs/rights/IMAGE-LEDGER.md` |

Section 3, decided:

- **Who swapped Strength and Justice:** settled from the printed sources; see below and
  `research/synthesis/strength-justice-numbering.md`. Corrected in `research/12-golden-dawn-book-t.mdx`,
  `research/people/golden-dawn.md`, `research/people/macgregor-mathers.md`,
  `research/decks/golden-dawn-book-t-tarot.md`, `research/cards/golden-dawn-book-t-tarot.md`, the Golden
  Dawn deck (its description, Strength and Justice notes, and "The 22 Keys"), and the course.
- **The history course's name:** applied, "The History of Tarot" in `tarot-and-the-crack.mdx` and
  `tarot-and-fiction.mdx` (and the anthology).
- **Cross-page counts:** dropped; each count is right for its own start date. A single form is a
  style choice for PlayfulProcess.
- **The Etteilla number cards:** still open. Giving them back Etteilla's own words needs a person to
  transcribe the card images or the *Troisième cahier*; not done here.

## 1. Claims to fix or hedge (a word or a clause, your wording)

| # | Where | Seam | Proposed fix |
|---|---|---|---|
| 1 | `kant-and-the-tarot.mdx:15` | "a few hundred miles away": Königsberg to Paris is about 950 miles. | "nearly a thousand miles away" |
| 2 | `kant-and-the-tarot.mdx:61` | Brazil "only began to rein in the bets in January 2024": the betting law (14.790) was signed on 30 Dec 2023; the licensed market opened 1 Jan 2025. | "passed its betting law at the end of 2023" |
| 3 | `kant-and-the-tarot.mdx:99` | "never short-changes an inexperienced child": Kant's shopkeeper does not *overcharge* an inexperienced customer, so that a child buys from him as cheaply as anyone (Groundwork 4:397). | "never overcharges an inexperienced customer, not even a child" |
| 4 | `kant-and-the-tarot.mdx:73`, `why-a-reading-feels-personal.mdx:19`, `how-tarot-works.mdx:35` | Forer: "In 1948", "In 1949", "first demonstrated in 1949". The class was run in 1948, the paper published in 1949. | One form everywhere, e.g. "in 1948 (published 1949)" |
| 5 | `how-tarot-works.mdx:25` | Brickman et al. 1978: winners and accident victims "drifted ... back toward roughly the happiness they started with". The study had no before-measure; it compared them with neighbours (winners not happier; victims somewhat less happy). | "both ended up far closer to their neighbours' happiness than anyone expected" |
| 6 | `how-tarot-works.mdx:47` and `what-a-reading-can-do.mdx:37` | Levitt's coin-flip study: "thousands" against "tens of thousands" (about 22,500 by the dossier). | "about twenty thousand" in both |
| 7 | `why-a-reading-feels-personal.mdx:39` | "Across the study's three experiments they did not", then the Markwick caveat. True of the 1983 analysis; reads as a contradiction. | "In the original analysis, across ..." |
| 8 | `why-a-reading-feels-personal.mdx:29` | Hyman "was disturbed to find his readings landing". Unverified: he believed in palmistry until a fellow performer had him read the opposite. | "was struck" |
| 9 | `intention-setting.mdx:63` | The Zeitlyn claim (declining questions like "will this person die?") is not in the repo's research. | A page reference to *Mambila Divination* (2020), or soften |
| 10 | `divination-traditions.mdx:17` | "three separate inventions ... none copying the others": Greek liver-reading is usually held to show Near Eastern influence. Koch (2015) as "the standard guide" to the second-millennium compendia: her volume covers the first millennium BCE (unverified). | "no evidence of China copying either"; "for the first-millennium corpus" |
| 11 | `divination-traditions.mdx:61` | "Lots and rune-marked staves": Tacitus says *notae*, marks; runes are attested only from about the 2nd century CE. | "marked staves (Tacitus does not say runes)" |
| 12 | `divination-traditions.mdx:65` | Oracle bones as "the oldest layer of Chinese divination": unwritten scapulimancy is older. | "the oldest written layer" |
| 13 | `divination-traditions.mdx:93` | "a Milanese card game of the 1440s": the earliest records are Ferrara and Milan both. | "an Italian court card game of the 1440s" |
| 14 | `tarot-today.mdx:15`, `:54` | "nobody used it to divine anything for another three hundred and fifty years"; "three and a half centuries before anyone thought to use it for divination". A Bolognese sheet of c. 1750 gives divinatory meanings for the trumps (Dummett, after Decker–Depaulis–Dummett). | "nobody is recorded using it to divine for about three hundred years" |
| 15 | `tarot-today.mdx:91` | Court de Gébelin "admitted he had no evidence": the repo says he *offered* none. | "who offered no evidence for" |
| 16 | `tarot-today.mdx:42` | Vinyl revenue "crossed a billion dollars for the first time since 1983": by RIAA's figures that was 2021, first since 1986 (unverified; no source in the repo). | Check the figure, or cut the year |
| 17 | `tarot-today.mdx:48`, `:123` | The Wild Unknown: "self-published in 2012", "often miscredited" as a Kickstarter; `research/17-contemporary-tarot.txt:25` says it had a 2012 Kickstarter (a raw AI transcript). | Check against the maker's own site before either stands |
| 18 | `tarot-and-fiction.mdx:21` | Calvino "fought the last two years of the war": he joined the partisans in 1944 (unverified). | "the last year of the war" |
| 19 | `history-of-tarot.mdx:13` | Waite as the man who "designed" the deck; the repo has Waite directing and Smith drawing, and `tarot-today.mdx:60` says "commissioned". | "who directed" |
| 20 | `history-of-tarot.mdx:31`, `:35` | Cards made "in Tang or Song China": the Ma Diao dossier says the Tang *yezi* was most likely not a card game, and the first unambiguous paper cards are later. `:31` already hedges; `:35` states it. | `:35` "made in China" |
| 21 | `history-of-tarot.mdx:110`, `:118` | Pips "abstract patterns for three centuries, then, from the Sola Busca of 1491 onward, little figured scenes": 1491 is fifty years in, and the Sola Busca had no run of successors before 1909. | "...then, in the Sola Busca of 1491 and again in 1909, little figured scenes" |
| 22 | `same-card-every-deck.mdx:43` | "the designers of what's now called the Rider-Waite-Smith deck ... swapped Strength and Justice", then "inherited wholesale". The repo's dossiers say the Golden Dawn made the swap. But the 1912 *Equinox* printing of Book T numbers Justice 8 and Fortitude 11 (`research/sources/book-t-equinox-1912.txt`), so who swapped is itself a question (see section 3). | Hold until section 3 is settled |
| 23 | `same-card-every-deck.mdx:23` | "without any European cardmaker ever touching a Mamluk deck directly": unknowable, and Mamluk cards did reach Italy. | "need never have copied one" |
| 24 | `same-card-every-deck.mdx:15` | Twenty-two trumps "fixed as a set ... by the 1440s": Minchiate has forty, the Cary-Yale is incomplete. | "by the mid-1400s, in most packs" |
| 25 | `index.html:193–194` | "the 1440s Milanese card game"; "the 1781 occult reframing that invented divination" (Etteilla's 1770 piquet manual already taught it). | "northern Italian"; "that invented occult tarot divination" |
| 26 | `index.html:291` | The RWS pips "borrow from the 1491 Sola Busca", stated as fact; `same-card-every-deck.mdx:55` hedges. | "were likely modelled on" |
| 27 | `pages/play.html:91`, `:79` | Ma Diao "The oldest card game you can still deal", "deepest documented root of every playing card" (the dossier corrected both); "a genuine public-domain deck" (the site's word is open). Site copy, not a course. | As in `history-of-tarot.mdx:49` now; "open deck" |

## 2. The Golden Dawn and voice courses

| # | Where | Seam | Proposed fix |
|---|---|---|---|
| 28 | `walking-the-golden-dawn-path.mdx:4`, `:13`, `:17`, `:49`, `:65` | Pathworking as "the Order's own contemplative practice", and the Order "used the deck two ways: to divine, and to walk". Book T has no pathworking; the word is later (the Order's heirs, Dion Fortune). The Order's nearest practice was scrying "in the spirit vision". `:17` already calls the gate reading "our turn". | "the practice the Order's heirs came to call pathworking" |
| 29 | `walking-the-golden-dawn-path.mdx:47` | The divination method as "the 'opening of the key'": the 1912 text titles it "A Method of Divination by the Tarot". | "(later called the 'Opening of the Key')" |
| 30 | `walking-the-golden-dawn-path.mdx:25`, `:100`, `:117` | Book T "set down by Mathers": the repo says written anonymously, "in the main by Mathers". `:25` "circulated to initiates rather than published": until *The Equinox* printed it in 1912. | "set down mainly by Mathers"; "... until *The Equinox* printed it in 1912" |
| 31 | `walking-the-golden-dawn-path.mdx:100` (also `reading-the-cards.mdx` via the chapter) | The sacred-texts link `/tarot/mathers/` may be Mathers's own 1888 booklet *The Tarot*, not Book T (the site blocks scripts, so not checked). | Open it; if it is the 1888 booklet, relabel it |
| 32 | `marsha-linehan-reads-the-tarot.mdx:21` | The quoted definition of wise mind ("that part of each person that can know and experience truth ... a certain peace") joins two clauses with an ellipsis; not checked against her skills manual. `:71` puts a stance in her voice without the "my reading" disclaimer `:65` carries. | Check the quote, or drop the marks; repeat the disclaimer at `:71` |
| 33 | `hospicing-modernity-reads-the-tarot.mdx:13–15`, `non-dual-tantra-reads-the-tarot.mdx:13`, `post-activism-reads-the-tarot.mdx` epigraph | Two epigraphs are labelled "faithful paraphrase" under a living person's name; the post-activism one is a direct quote. Three labels for one kind of thing. | One label on all three, e.g. "in the spirit of" |
| 34 | `hospicing-modernity-reads-the-tarot.mdx:13`, `:15` | "Vanessa Andreotti": *Hospicing Modernity* (2021) is published as Vanessa Machado de Oliveira. | "Vanessa Machado de Oliveira (formerly Andreotti)" |
| 35 | `hospicing-modernity-reads-the-tarot.mdx:31` | The heading "Staying with the trouble" is Donna Haraway's phrase (2016). | A small credit |
| 36 | `how-to-contribute.mdx:198` vs `:237` | The audit pass "with Claude Desktop" at `:198`; "head-less in Claude Code" at `:237`. | One of the two |
| 37 | `how-to-contribute.mdx:29` | The link "Contribute to the Commons — Five Ways" opens a stub that says the course has moved. | "Ways to Contribute", linked to that course |
| 38 | `how-to-contribute.mdx:192` | "the historical decks in this commons are scanned public-domain art": the site's word is open (`docs/rights/IMAGE-LEDGER.md`). | "scanned historical art, open to use (see the image ledger)" |

## 3. Questions beyond the courses

- **Who swapped Strength and Justice?** `research/12-golden-dawn-book-t.mdx:52–54`,
  `research/people/golden-dawn.md:58–61` and `research/people/macgregor-mathers.md:160–161` say the
  Golden Dawn swapped them and the Rider-Waite-Smith inherited the order. The Golden Dawn's
  attributions put Leo (Strength) on the eighth path and Libra (Justice) on the eleventh, which is
  the usual reading of "the Golden Dawn swap"; the 1912 printing nevertheless numbers Justice 8 and
  Fortitude 11. The Golden Dawn deck's "About the Keys" says "Strength at VIII (Leo), Justice at XI
  (Libra)". One sentence in the dossiers would settle the wording: the swap is in the
  attributions, and the 1909 deck was the first to print it.

  **Settled Oct 8 from the printed sources** (full table in
  `research/synthesis/strength-justice-numbering.md`):
  - Mathers, *The Tarot* (1888): Justice 8 (Cheth), Strength 11 (Kaph), on Lévi's letter scheme
    (Magician = Aleph, Fool = Shin). Read in two transcriptions; no page scan seen.
  - Book T, *The Equinox* I(8) (1912): Fortitude numbered 11 on Teth/Leo, Justice numbered 8 on
    Lamed/Libra, Fool on Aleph. Read in the archive.org scan's OCR and the repo's transcription.
  - Rider-Waite-Smith cards (1909): VIII Strength, XI Justice.
  - Waite, *Pictorial Key* (1911): Strength 8, with "For reasons which satisfy myself, this card has
    been interchanged with that of justice, which is usually numbered eight."
  - Regardie, *The Golden Dawn* (1937–40): reference only, in copyright, not checked.

  So the Golden Dawn moved the attributions; the 1909 deck is the first known to print the new
  numbers. Whether the Order's manuscripts renumbered the cards is not settled by any printed
  source checked here (Crowley edited the 1912 printing, and his Thoth deck keeps the same
  arrangement: old numbers, Golden Dawn letters).
- **Cross-page counts.** "Six centuries" (`index.html`, `_courses.json:7`, `pages/historian.html:63`),
  "six-hundred-year-old" (`tarot-and-the-crack.mdx:36`), "580-year-old" (`tarot-today.mdx:36`),
  "five and a half centuries" (`same-card-every-deck.mdx:13`), "four and a half"
  (`history-of-tarot.mdx:94`). All defensible for their start points; one form would read better.
- **The history course's name.** It is "The History of Tarot"; `tarot-and-the-crack.mdx:16` and
  `tarot-and-fiction.mdx:88` link it as "A History of Tarot".
- **The Etteilla number cards** now carry no meaning (their template lines were removed). Etteilla
  printed his upright and reversed words on each card; a transcription from the card images,
  checked by a person, or from his *Troisième cahier*, would give them back his own words.
  *Done on branch `sources/etteilla-own-words`:* all 78 cards on the three decks now carry his
  upright and reversed words from the *Dictionnaire synonimique du Livre de Thot* (1791), pp. 19-57
  (`research/sources/etteilla-dictionnaire-synonimique-1791.md`); the *Troisième cahier* is still
  unread.
