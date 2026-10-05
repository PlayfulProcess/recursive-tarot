# Rights audit, October 4 2026

PlayfulProcess asked for this after reading the home page line "A free, public-domain library of
historical tarot": some of what the library holds is not public domain, so the line should say
**open**. This audit checks what each part of the library is, and who holds which rights.

It builds on [`docs/AUDIT-2026-09-23.md`](../AUDIT-2026-09-23.md) (§3 proposals, §4 deck survey)
and on the five decks whose provenance was backfilled by `scripts/backfill_image_provenance.py`.
It is not legal advice; where the answer depends on a reading of the law, it says so.

## How it was checked

- **Every card image** (1,998 in 34 decks) was looked up on Wikimedia Commons by
  `scripts/audit_image_rights.py`: licence, credit line and artist, per card. The per-card rows
  are in [`image-ledger.json`](image-ledger.json), the per-deck summary in
  [`IMAGE-LEDGER.md`](IMAGE-LEDGER.md). A Commons "public domain" tag is the uploader's claim about
  the **work**; it is not a grant from whoever made the **scan**.
- **The contemporary decks' licence** was looked for on stolen-thyme.com (home, about, four deck
  pages, a guidebook page), in the page text and in the raw HTML.
- **Every "public domain" claim** on the site was searched for (`*.html`, `*.mdx`, `*.md`, JSON).
- **Text sources** were read from each deck's section headers and attribution.
- **Print listings** (`print-products.json`) were compared with the image sources, because a deck
  for sale is commercial use and the terms change.

## What this branch fixes

| # | Finding | Fix |
|---|---|---|
| 1 | **Song lyrics stored.** 74 cards of `anecdotes-tarot` carried Joanna Newsom lyric lines in "Song reference", and 74 rows of `research/yve-lepkowski/anecdotes-raw/` held the same lines. The deck's own note said the lyrics were not reproduced. They arrived with the Aug 10 2026 app sync (`c57aaa5`). | Each now names the song, album and year only. Lyrics are never stored, in any form. |
| 2 | **Blanket claims.** 35 lines said "public-domain library", "every image public domain", "public-domain JSON" or "public-domain code" (home, about, historian, contribute, play, shop, print page, course credits, the channel manifest, README, a course). The JSON and our text are CC BY-SA, the code is Apache-2.0, and not every image is free of terms. | "Open", "credited", or a sentence that says what is true. Your lede now reads "A free, **open** library of historical tarot…". |
| 3 | **README and NOTICE** said the card artwork is public domain and that each grammar records per-image provenance. Most decks record it per deck only. | Both now say the CC BY-SA covers our text and structure, never the card images, and list the third-party image groups below. |
| 4 | **Conver photographs mislabelled.** 24 card photographs by the Tarot World Project (CC BY-SA 4.0 on Commons, of a 2020 reprint) were labelled "Public Domain" per card (Sep 23 proposal P1). | Relabelled CC BY-SA 4.0, with the photographer credit. |
| 5 | **Mantegna credit wrong.** The deck-level credit named the British Museum and the Albertina; the images are the Cleveland Museum of Art impression (CC0), as the cards themselves say. | Credit corrected. |
| 5b | **Gallica credit missing.** Gallica's free non-commercial reuse asks for the credit "Source gallica.bnf.fr / Bibliothèque nationale de France". Six decks showing BnF scans did not carry it (Minchiate's said "Various collections"). | Added to the deck credit of Minchiate, Oswald Wirth, Papus, Charles VI, Noblet and Conver (Conver's also names the CC BY-SA photographer). |
| 6 | **Five print-listed decks had no rights record.** `minchiate-florence-tarot` and `oswald-wirth-tarot` are BnF scans (via Commons); the three Etteilla decks have no recorded source at all. All five were marked ready to print. | Each now has a `rights` block with a `sale_gate`, in the shape Viéville, Paris and Conver already use. Golden Dawn and Mantegna got a rights record too. Nothing was ever on sale (`product_url` is empty everywhere). |
| 7 | **No per-card evidence.** | `scripts/audit_image_rights.py` and the ledger in this folder. Re-run it after any image change. |

## What each deck's images are

From the ledger (Commons, Oct 4 2026). "BnF scan" means the Commons credit points at Gallica or
the BnF: free to reuse **non-commercially** with the credit; a deck for sale needs a BnF licence
(for playing cards, a negotiated percentage of sales).

| Status | Decks | What it means |
|---|---|---|
| ✔ Clean | Cary-Yale Visconti (Beinecke, 105), Cary Sheet (Beinecke), Este (Yale IIIF), Mantegna (Cleveland, CC0), Madiao (Skokloster), Ganjifa (LACMA) | Public-domain work; the holder asks for nothing, or only a credit. |
| ◆ BnF scan | Viéville (83), Paris anonymous (83), Minchiate (147), Oswald Wirth (22) and the same images in Papus (22), Charles VI (18), Noblet (1), Conver pips and courts (81) | Fine on this free site with the Gallica credit (now on every one of these decks). Not for sale without a BnF licence. |
| ◆ CC BY-SA photograph | Conver trumps (Tarot World Project, 37 images incl. aces), Tarocchino Bologna (6) | Credit the photographer, keep the licence. |
| ○ Scanned from a modern reproduction | Visconti-Sforza (87 scans by David Madore, 23 from the Dal Negro reproduction), Sola Busca (108, from waitesmith.org, 474 px) | A faithful copy of a flat old work adds no new copyright in the US or (since the 2019 DSM directive, art. 14) the EU. For print, the originals are in Italian public collections (Accademia Carrara, Brera), and Italian heritage law asks for a fee on commercial reproductions of works held there; an Italian court applied it to a foreign puzzle maker in 2022. Not print-listed. |
| ○ Weak provenance | Besançon (Pinterest, ezomania.ru, "self-scanned"), Mamluk (no credit on Commons), Belgian (trionfi.eu), Court de Gébelin (the 1781 plates; which library's copy is not named) | Public-domain work, but the scan's origin is thin. Replace when a better scan turns up. |
| ◆ Copied from a website | Tarocchino Bologna (77 images from pagat.com) | pagat.com is © John McLeod and states no image licence. Replace with Commons scans, or ask him. |
| ◇ Unrecorded | Etteilla I, II, III (282) | Uploaded through recursive.eco; nothing says which scan or printing. Gated for print. |
| ◇ Waite-Smith printing unrecorded | Golden Dawn, Rider-Waite-Smith (182, Commons credit muzendo.jp) | The work is public domain (US; UK/EU since 2022). Before a sale, confirm the printing, and keep RIDER-WAITE-SMITH (a U.S. Games trademark for printed tarot cards) off product names and boxes. |
| Contemporary decks | Yve Lepkowski's five decks (340); PlayfulProcess's Ontoject, Bus Passengers, 36 Tattvas | See decisions A and D. |

## Texts

- Translated here from public-domain originals: Wirth (1927 French; Wirth d. 1943, US public
  domain since 2023), Court de Gébelin (1781). Carried in old translations: Papus (A. P. Morton's
  1890s English), Waite (*Pictorial Key*, 1911). Book T meanings are labelled paraphrase
  (`scripts/label_book_t_divinatory_paraphrase.py`).
- Etteilla: our own rewriting, crediting Benebell Wen's reconstruction (2022). Spot check: no
  shared 8-word run with her Etteilla landing page; her per-card pages were not checked.
- Yve Lepkowski's guidebook text is carried verbatim in her five decks (decision A).

## Decisions waiting for PlayfulProcess

**A. Yve Lepkowski's five decks.** The repo labels them CC BY-SA 4.0 (`_grammar_commons`, the
NOTICE until today, the import plan). Her site states no licence anywhere I could find, only
"Stolen Thyme is created by Yve Lepkowski, 2020-2023". The label first appears as recursive.eco's
default `_grammar_commons` stamp (attribution dated 2026-01-22). If she granted it (an email, a
message, a licence inside her downloads), record the grant in `research/yve-lepkowski/`. If not,
the five decks (340 images and her verbatim guidebook text) are republished without a licence:
ask her (a short email, drafted for your approval), or take them off the site until she answers.

**B. Lyrics in git history.** The lyric lines are gone from the files but remain in this public
repository's history. Rewriting a public history breaks every fork and clone, so the usual answer
is to leave it; it is your call.

**C. recursive.eco's copy of Anecdotes Tarot** still carries the lyrics, and the app's items win
on a write-back ("Resolve all drifts"), which would bring them back here. Fix the app copy (MCP
`update_items`) after you say yes.

**D. Per-image provenance on every deck.** Only five decks carry `_image_provenance`. The ledger
has what is needed to write it for the other 17 record decks, the way
`backfill_image_provenance.py` did. It touches 17 grammars, so it waits for your word.

**E. Re-sourcing, later:** Tarocchino Bologna from Commons, Sola Busca from the British Museum or
Brera, Visconti-Sforza from the Morgan and Carrara, Etteilla's real source.
