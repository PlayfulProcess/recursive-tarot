# The card table: requests for recursive.eco

*Written 2026-10-02 for the recursive.eco session PlayfulProcess is sending. This repo built the
static half; everything below needs the app (accounts, AI, the database, the MCP). Nothing here is
built yet. Read `docs/plan/PLAN-card-table-notation-2026-10-02.md` first.*

## What exists here, to build against

- **The notation**, as a pure parser with no DOM: `viewers/notation.js`
  (`parseTable(text) → { title, deck, columns, rows, notes, strips, errors }`, `parseCard`,
  `serializeTable`, `cardCode`, `cardName`). Tests: `node viewers/notation.test.js`. It can be
  copied into the app as is (works in node and the browser).
  - Majors `0`–`XXI`; minors rank (`A`/`1`, `2`–`10`, `P`, `Kn`, `Q`, `K`) + suit (`W` `C` `S` `P`;
    also `♥` cups, `⛤` pentacles, `+`/`†` swords).
  - `↓` (or `r`) reversed; `↑` optional upright; `( )` circled, the message.
  - `Area | cells…` rows, `[Heading]`, `> note`, `Label: cards` mini-rows, `deck:`, `columns:`, `title:`.
- **The table page**, `viewers/table.html` (tarot.recursive.eco/viewers/table.html once merged):
  editable rows and columns, **Lay the table**, per-card notes in localStorage, export `.md`/JSON,
  a share link `?t=<base64url notation>`.
  - It also publishes the current table as JSON in
    `<script type="application/json" id="card-table-state">`, with every card's code, name,
    orientation, circle and note: **the shape an assistant can read**.
- **Column and cell vocabulary**: columns default to `less | keep | more`; any names are allowed.

## Requests, roughly in the order they'd help

1. **Photo of real cards → the table.** *(PlayfulProcess, 2026-10-02: "a reader might just take a
   picture of any deck and the AI assistant may read [it], with cards instead of notation.")*
   - She photographs a spread laid on the floor or a table: any deck, real cards, not notation.
   - The assistant names each card and its position, and writes the result in the notation.
   - It **shows the result for her to confirm** before anything is saved: decks differ, reversed
     cards are easy to miss, and a misread card is a different reading.
   - The rows and columns come from the layout when it is a grid; otherwise the assistant asks.
   - This may partly work today (image upload to the assistant); the notation gives it a fixed
     output format and the confirm step makes it safe.
2. **Photo of a handwritten table → the table.** Same flow, from her paper notation. Handwriting
   is ambiguous (a `+` can be her sword glyph): the assistant asks rather than guesses.
3. **A table is a grammar.** *Half done here (2026-10-03):* `table.html` has **Export as grammar**, a
   `grammar.json` that recursive.eco's Create → Import JSON accepts (cards as items with `area`,
   `column`, `code`, `reversed`, `circled` and the deck cross-link; groups per area, per column and
   for the circled cards). What's left for the app is a one-tap **Save to recursive.eco** that does
   the same server-side, private by default. The shape:
   - items = the cards, each with metadata `row`, `column`, `circled`, `reversed`, `deck`, `code`;
   - sections = the deck's meaning for that card and **My note**;
   - one edition per row (an area) or per column (less · keep · more).
   These are existing primitives (`create_grammar`, `add_items`, `create_edition`).
4. **A table viewer** in the app for any grammar whose items carry row/column metadata: the same
   grid as `table.html`.
5. **"My meanings" across readings.** The same card's notes, gathered from every table she has
   saved, as a personal layer beside the deck's meaning.
6. **The assistant inside her frame.** "Help me read my table" asks for help within the frame she
   set: it may suggest; she decides. A case for the oracle-values eval lab: a preset where useful
   advice is the right answer, scored on who keeps the decision
   (`recursive-eco/docs/research/EVALS.md`).
7. **Cast a table** through the MCP `cast` tool, with the row labels as the questions.
8. **An MCP tool pair**: `parse_table_notation` (text → structure, no writes) and
   `save_table_reading` (structure → private grammar), so claude.ai and ChatGPT can do the photo
   flows too.
9. **Privacy defaults.** Tables name people and projects. Private by default; never public without
   her word; nothing from a table enters an eval or a post without her consent.

## Reflective-practice rules that carry over (from this repo's CLAUDE.md)

Practice words ("Lay the table", "Draw & reflect"), never "Get a Reading"; a visible re-draw count;
the evidence line at the moment of the draw; the deck never calls (no daily table, streak or
reminder); tarot stays off kids surfaces, and AI readings are adults-only.
