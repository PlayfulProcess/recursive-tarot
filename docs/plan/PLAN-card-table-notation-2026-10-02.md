# Plan: the card table and its notation (for a cloud session)

Written 2026-10-02 for a session that starts cold. Read `CLAUDE.md` first: the creed (gate, not fate), "Consolidate, don't multiply", the reflective-practice rules, `theme.css` as the one colour source, and the one cross-link pattern all apply here.

## What it is

PlayfulProcess keeps a **card table** to prioritise her life. Rows are areas (projects, practices, parts of life). Columns are **do less · keep · do more** (she writes them − · = · +). She lays one card per cell, sometimes two. Then she sits with the table and evaluates it, especially where major arcana fall. She circles the cards that carry the current message. A circled card is the one she feels is needed, not the "best" one. Under the table she may add short lines ("cards = possibilities") and a mini-row from another deck or oracle (Golden Dawn, the odùs).

Example of her use: an 8 of Swords under "keep" in one area read as a sign to keep restraining herself a little there. The table is hers; the cards land in it; she decides.

Her tables name private projects and people. **No real table goes into this public repo.** The examples below use made-up rows.

## Goal

1. A **typed notation** anyone can learn in five minutes, close to how she writes by hand.
2. A **static page** that renders a table from that notation with the card images of a chosen deck, highlights the majors, marks circled and reversed cards, opens each card's meaning, and lets the person add a note per card.
3. A **short course page** that teaches the practice and the notation, in the creed's voice.
4. A list of **recursive.eco ideas** for later (below). This repo builds none of them.

## The notation (v1)

```
deck: golden-dawn-book-t
columns: less | keep | more

Work      | 4C ↑      | 3W        | (XVIII)
Health    | 7C        | 8C        | QS
Writing   | (XVII)    | AS        | 6Wr
Family    | KnP       | (VIII)    | IV

> cards = possibilities
Golden Dawn: (6C) QS 11
```

**Cards**

| Kind | Write | Examples |
|---|---|---|
| Major arcana | Roman numerals 0–XXI (0 = the Fool) | `XVIII`, `0`, `XXI` |
| Minor arcana | rank + suit letter | `4C`, `10S`, `AW`, `KnP` |
| Ranks | `A` (or `1`), `2`–`10`, `P` page, `Kn` knight, `Q` queen, `K` king | `PW`, `KnC` |
| Suits | `W` wands, `C` cups, `S` swords, `P` pentacles | |
| Reversed | suffix `r` | `6Wr`, `XIIr` |
| Upright, explicit | suffix `↑` or `+`, optional | `4C↑` |
| Circled (the message) | parentheses | `(XVIII)`, `(6C)` |
| Two cards in one cell | a space | `8S 3P` |

**Her handwritten glyphs, which the page also accepts and draws as icons:** a **leaf** for wands, a **heart** for cups, a **sword with a cross-guard** for swords, a **pentagram** for pentacles. Typed equivalents: `♥` for cups, `⛤` for pentacles; leaf and sword have no common character, so letters stay the canonical form. Draw the four suit icons as small SVGs in `icons.js`, never emoji.

**Table lines:** `Row label | cell | cell | cell`. The number of cells follows `columns:` (default three: less · keep · more). The `deck:` line picks the images and meanings (any deck slug under `tarot/`); default `golden-dawn-book-t`. Lines starting with `>` are free notes. A line `Label: cards` with no pipes is a mini-row (another deck or oracle), rendered as a strip under the table.

**Open questions for her** (ask once; until answered use the defaults above):
1. In her handwriting, an arrow `↑` follows many cards and a `+` appears on some. Default here: both mean upright and are optional; `r` means reversed. Is that right?
2. Is the boxed "GOALS" row a heading over the rows below it? Default: a row label written in `[brackets]` renders as a section heading spanning the table.
3. The column labels: "less · keep · more", or her own words?

## Build (static, no AI, no accounts)

**S1. `viewers/notation.js`.** A pure parser, `parseTable(text) → {deck, columns, rows:[{label, cells:[[card…]]}], notes, strips}`. Each card is `{raw, major:bool, number, rank, suit, reversed, circled}`. Errors come back per line ("line 4: '9X' isn't a card"), never thrown. Tests run with node (`node viewers/notation.test.js`): every example above, her glyph variants, and bad input.

**S2. `viewers/table.html`.** Consolidate, don't multiply: reuse `grammar-loader.js` and `deck-picker.js` for decks, and the card modal of `cards.html` (or its `?item=` deep link) for meanings.
- Left: a textarea with the notation (prefilled with the example) and the deck picker. Right: the grid.
- Each cell shows the card image (the deck's image pattern, see "Image pattern" in `CLAUDE.md`) with its short name.
  - Majors get a highlight from `theme.css` tokens (add a token if needed; never a local colour).
  - Circled cards get a ring.
  - Reversed cards are turned 180°.
- Click a card: the deck's meaning (upright or reversed section) plus a **"My note"** box.
  - Notes live in `localStorage`, keyed by table and card, wrapped in try/catch.
  - **Export** gives the notation plus notes as a `.md` file, and also as JSON.
  - **Import** takes either back.
- `?src=<url>` loads a notation file. A **Print** view lays the table on one page.
- Works at 375 px: rows stack, three columns stay.

**S3. Cast into a table (optional).** Add a `table` entry to `viewers/spreads.json` whose positions are built from the row labels × columns, so `caster.html` can **draw** a table instead of only recording one. Keep the reflective-practice rules: practice words ("Lay the table", "Draw & reflect"), a visible re-cast count, the evidence line at the draw (`oracle-ribbon.js`).

**S4. `course/` page: "Your card table".** Follow `docs/HOW-TO-WRITE-A-COURSE.md`.
- The practice in her terms: areas, less · keep · more, sit with it, circle the message, decide yourself.
- The notation in five minutes.
- A worked example with made-up rows.
- A link to `table.html` through the one cross-link pattern.
- The creed line: relate to the card, never obey it.

**S5. Docs.** A row in `FUTURE_PLAN.md`, an entry in `docs/plan/CHANGELOG.md`, a line in `CLAUDE.md`'s scripts cheat-sheet if a script is added.

Work on a branch, open a PR, and don't merge: she checks first.

## recursive.eco ideas (later; Platform's call)

These need the app (AI, accounts, the database). Write them up as requests for the Platform chat; build none of them here.

1. **Photo → notation.** She uploads a photo of a handwritten table. The assistant transcribes it into the notation and **shows it for her to confirm** before anything is saved. Handwriting is ambiguous (a `+` can be a suit or an "upright"); the assistant asks rather than guesses.
2. **A table is a grammar.** Saving creates a private grammar:
   - items = the cards placed in the table, each with metadata row, column, circled, reversed and deck;
   - sections = the deck's meaning and **"My note"**;
   - editions = one per row (an area) or per column (less · keep · more).
   These are existing primitives: `create_grammar`, `add_items`, `create_edition`.
3. **A table viewer** for any grammar whose items carry row/column metadata: the same grid as `table.html`, inside the app.
4. **"My meanings" across readings.** The same card's notes, gathered from every table she has saved, as a personal layer next to the deck's meaning.
5. **The assistant inside her frame.** "Help me read my table" is a request for help within the frame she set; the assistant may suggest, but she decides. This is a case for the oracle-values eval lab: a preset where useful advice is the right answer, scored on who keeps the decision. (See `recursive-eco/docs/research/EVALS.md`.)
6. **Cast a table** through the MCP `cast` tool, with row labels as the questions, when someone asks to draw one.
7. **An MCP tool pair:** `parse_table_notation` (text → structure, no writes) and `save_table_reading` (structure → private grammar), so claude.ai and ChatGPT can do the photo flow too.
8. **Privacy:** tables name people and projects. Default private; never public without her word; nothing from a table ever enters an eval or a post without her consent.
